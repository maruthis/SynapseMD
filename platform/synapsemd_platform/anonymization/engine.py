import hashlib
import re
import uuid
from dataclasses import dataclass, field

from synapsemd_platform.core.config import get_settings

EMAIL_PATTERN = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")
PHONE_PATTERN = re.compile(r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b")
SSN_PATTERN = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
DATE_PATTERN = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
NAME_PATTERN = re.compile(r"\b(?:Mr|Mrs|Ms|Dr)\.?\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b")


@dataclass
class AnonymizationResult:
    anonymized_text: str
    token_map: dict[str, str] = field(default_factory=dict)
    phi_detected: bool = False


class TokenVault:
    """In-memory vault; swap for HashiCorp Vault in production."""

    def __init__(self) -> None:
        self._store: dict[str, str] = {}

    def store_tokens(self, user_id: str, token_map: dict[str, str]) -> None:
        for token, value in token_map.items():
            self._store[f"{user_id}:{token}"] = value

    def resolve(self, user_id: str, token: str) -> str | None:
        return self._store.get(f"{user_id}:{token}")

    def deanonymize(self, user_id: str, text: str, token_map: dict[str, str]) -> str:
        result = text
        for token, _ in token_map.items():
            real = self.resolve(user_id, token)
            if real:
                result = result.replace(token, real)
        return result


class AnonymizationEngine:
    def __init__(self, vault: TokenVault | None = None) -> None:
        self.settings = get_settings()
        self.vault = vault or self._create_token_vault()
        self._presidio = None
        if self.settings.presidio_enabled:
            self._init_presidio()

    def _create_token_vault(self) -> TokenVault:
        if (
            self.settings.vault_enabled
            and self.settings.vault_url
            and self.settings.vault_token
        ):
            from synapsemd_platform.anonymization.vault_store import VaultTokenVault

            return VaultTokenVault(self.settings.vault_url, self.settings.vault_token)
        return TokenVault()

    def _init_presidio(self) -> None:
        try:
            from presidio_analyzer import AnalyzerEngine
            from presidio_anonymizer import AnonymizerEngine

            self._presidio = (AnalyzerEngine(), AnonymizerEngine())
        except ImportError:
            self._presidio = None

    def anonymize_for_llm(self, text: str, user_id: str) -> AnonymizationResult:
        if self._presidio:
            return self._anonymize_presidio(text, user_id)
        return self._anonymize_regex(text, user_id)

    def _anonymize_regex(self, text: str, user_id: str) -> AnonymizationResult:
        token_map: dict[str, str] = {}
        anonymized = text

        patterns = [
            ("EMAIL", EMAIL_PATTERN),
            ("PHONE", PHONE_PATTERN),
            ("SSN", SSN_PATTERN),
            ("DATE", DATE_PATTERN),
            ("NAME", NAME_PATTERN),
        ]

        for entity_type, pattern in patterns:
            for match in pattern.finditer(anonymized):
                original = match.group()
                token = f"TOKEN_{entity_type}_{uuid.uuid4().hex[:8]}"
                token_map[token] = original
                anonymized = anonymized.replace(original, token, 1)

        self.vault.store_tokens(user_id, token_map)
        validation = self.validate_no_phi(anonymized)
        if not validation and self.settings.phi_block_on_failure:
            raise ValueError("PHI detected after anonymization — blocking LLM call")

        return AnonymizationResult(
            anonymized_text=anonymized,
            token_map=token_map,
            phi_detected=bool(token_map),
        )

    def _anonymize_presidio(self, text: str, user_id: str) -> AnonymizationResult:
        analyzer, anonymizer = self._presidio  # type: ignore[misc]
        results = analyzer.analyze(
            text=text,
            entities=["PERSON", "DATE_TIME", "LOCATION", "PHONE_NUMBER", "EMAIL_ADDRESS", "US_SSN"],
            language="en",
        )
        token_map: dict[str, str] = {}
        operators: dict = {}
        from presidio_anonymizer.entities import OperatorConfig

        for result in results:
            original = text[result.start : result.end]
            token = f"TOKEN_{result.entity_type}_{uuid.uuid4().hex[:8]}"
            token_map[token] = original
            operators[result.entity_type] = OperatorConfig("replace", {"new_value": token})

        anonymized = anonymizer.anonymize(text=text, analyzer_results=results, operators=operators)
        self.vault.store_tokens(user_id, token_map)
        if not self.validate_no_phi(anonymized.text) and self.settings.phi_block_on_failure:
            raise ValueError("PHI detected after anonymization — blocking LLM call")
        return AnonymizationResult(
            anonymized_text=anonymized.text,
            token_map=token_map,
            phi_detected=bool(token_map),
        )

    def validate_no_phi(self, text: str) -> bool:
        checks = [EMAIL_PATTERN, PHONE_PATTERN, SSN_PATTERN, NAME_PATTERN]
        return not any(p.search(text) for p in checks)

    def deanonymize_response(self, text: str, user_id: str, token_map: dict[str, str]) -> str:
        return self.vault.deanonymize(user_id, text, token_map)


def hash_content(content: str) -> str:
    return hashlib.sha256(content.encode()).hexdigest()
