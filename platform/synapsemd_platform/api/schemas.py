from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class TenantCreate(BaseModel):
    name: str
    plan: str = "starter"


class TenantResponse(BaseModel):
    id: UUID
    name: str
    plan: str


class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    role: str = "patient"


class UserResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    role: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int | None = None
    refresh_token: str | None = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    tenant_id: UUID


class RefreshRequest(BaseModel):
    refresh_token: str


class OidcLoginRequest(BaseModel):
    tenant_id: UUID
    redirect_uri: str | None = None


class OidcCallbackRequest(BaseModel):
    code: str
    state: str


class OidcTokenRequest(BaseModel):
    id_token: str
    tenant_id: UUID


class ConsentUpdateRequest(BaseModel):
    purpose: str = "llm_processing"
    granted: bool


class BreakGlassRequest(BaseModel):
    reason: str = Field(min_length=3)
    minutes: int = Field(default=15, ge=1, le=60)


class CommandExecuteRequest(BaseModel):
    command: str
    payload: dict = Field(default_factory=dict)
    context_text: str = ""


class CommandExecuteResponse(BaseModel):
    interaction_id: str
    command: str
    response: str
    model_used: str
    confidence: float
    human_review_required: bool
    disclaimer: str | None = None


class ReviewDecisionRequest(BaseModel):
    action: str  # approve | modify | reject
    clinician_notes: str | None = None
    modified_response: str | None = None


class MigrateRequest(BaseModel):
    source_directory: str


class AiAnalyzeRequest(BaseModel):
    time_range: str = "last_quarter"


class AiPredictRequest(BaseModel):
    risk_type: str = Field(description="hypertension, diabetes, cardiovascular, nutritional_deficiency, sleep_disorder, or all")


class AiChatRequest(BaseModel):
    query: str = Field(min_length=1)


class AiReportRequest(BaseModel):
    report_type: str = "comprehensive"
    time_range: str = "last_quarter"


class AiActionResponse(BaseModel):
    action: str
    result: dict
    disclaimer: str | None = None
    human_review_required: bool = False


class TenantModelPolicyRequest(BaseModel):
    allowlist: list[str] | None = None
    residency: str | None = None
    baa_required: bool = False
    budget_tokens_per_day: int | None = None
    pinned_commands: dict[str, str] = Field(default_factory=dict)


class DsrCreateRequest(BaseModel):
    subject_user_id: UUID
    request_type: str = Field(pattern="^(access|erase|correct)$")
    correction: dict = Field(default_factory=dict)


class LegalHoldRequest(BaseModel):
    reason: str = Field(min_length=3)
    user_id: UUID | None = None
    active: bool = True
