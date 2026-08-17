from uuid import uuid4

from synapsemd_platform.auth.policy import (
    AuthzContext,
    Resource,
    Subject,
    authorize,
)
from synapsemd_platform.auth.roles import map_idp_groups_to_roles, scopes_for_roles


def test_map_idp_groups_to_roles() -> None:
    assert map_idp_groups_to_roles(["synapsemd-clinicians"]) == ["clinician"]
    assert map_idp_groups_to_roles(["/realms/synapsemd/synapsemd-admins"]) == ["admin"]
    assert map_idp_groups_to_roles([]) == ["patient"]
    assert "tenant_admin" in map_idp_groups_to_roles(["synapsemd-tenant-admins", "patient"])


def test_scopes_include_new_roles() -> None:
    assert "admin" in scopes_for_roles(["tenant_admin"])
    assert "privacy" in scopes_for_roles(["privacy_officer"])
    assert "break_glass" in scopes_for_roles(["break_glass"])


def _subject(*roles: str, tenant=None, scopes=None) -> Subject:
    tid = tenant or uuid4()
    return Subject(
        user_id=uuid4(),
        tenant_id=tid,
        roles=tuple(roles),
        scopes=tuple(scopes or ["read:own", "write:own"]),
    )


def test_pdp_llm_consent_required() -> None:
    tenant = uuid4()
    decision = authorize(
        _subject("patient", tenant=tenant),
        "execute",
        Resource(type="command", id="consult", tenant_id=tenant),
        AuthzContext(llm_processing=False),
    )
    assert decision.allowed is False
    assert decision.reason == "llm_processing_consent_required"


def test_pdp_health_command_without_llm_consent() -> None:
    tenant = uuid4()
    decision = authorize(
        _subject("patient", tenant=tenant),
        "execute",
        Resource(type="command", id="gout", tenant_id=tenant),
        AuthzContext(llm_processing=False),
    )
    assert decision.allowed is True


def test_pdp_cross_tenant_denied() -> None:
    decision = authorize(
        _subject("clinician"),
        "execute",
        Resource(type="command", id="profile", tenant_id=uuid4()),
        AuthzContext(),
    )
    assert decision.allowed is False
    assert decision.reason == "cross_tenant_denied"


def test_pdp_break_glass_cross_tenant() -> None:
    other = uuid4()
    subject = Subject(
        user_id=uuid4(),
        tenant_id=uuid4(),
        roles=("clinician", "break_glass"),
        scopes=("read:org", "break_glass"),
        break_glass=True,
    )
    decision = authorize(
        subject,
        "execute",
        Resource(type="command", id="profile", tenant_id=other),
        AuthzContext(),
    )
    assert decision.allowed is True


def test_pdp_admin_and_audit_and_scim() -> None:
    tenant = uuid4()
    admin = _subject("admin", tenant=tenant, scopes=["admin"])
    patient = _subject("patient", tenant=tenant)
    assert authorize(admin, "read", Resource(type="admin", tenant_id=tenant), AuthzContext()).allowed
    assert not authorize(patient, "read", Resource(type="admin", tenant_id=tenant), AuthzContext()).allowed
    auditor = _subject("auditor", tenant=tenant, scopes=["audit"])
    assert authorize(auditor, "read", Resource(type="audit", tenant_id=tenant), AuthzContext()).allowed
    assert authorize(admin, "read", Resource(type="scim", tenant_id=tenant), AuthzContext()).allowed
    assert not authorize(patient, "read", Resource(type="scim", tenant_id=tenant), AuthzContext()).allowed
    officer = _subject("privacy_officer", tenant=tenant, scopes=["privacy"])
    assert authorize(officer, "write", Resource(type="privacy", tenant_id=tenant), AuthzContext()).allowed
    assert not authorize(patient, "write", Resource(type="privacy", tenant_id=tenant), AuthzContext()).allowed


def test_pdp_consent_and_unknown_resource() -> None:
    tenant = uuid4()
    patient = _subject("patient", tenant=tenant)
    assert authorize(patient, "write", Resource(type="consent", tenant_id=tenant), AuthzContext()).allowed
    assert not authorize(patient, "read", Resource(type="unknown", tenant_id=tenant), AuthzContext()).allowed


def test_pdp_break_glass_activate() -> None:
    tenant = uuid4()
    clinician = _subject("clinician", tenant=tenant)
    patient = _subject("patient", tenant=tenant)
    assert authorize(
        clinician, "activate", Resource(type="break_glass", tenant_id=tenant), AuthzContext()
    ).allowed
    assert not authorize(
        patient, "activate", Resource(type="break_glass", tenant_id=tenant), AuthzContext()
    ).allowed
