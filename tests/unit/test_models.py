def test_models_package_exports() -> None:
    from synapsemd_platform.models import (
        AIInteraction,
        AllergyRecord,
        AuditEvent,
        BreakGlassGrant,
        Consent,
        DsrRequest,
        GoutFlare,
        Identity,
        PatientProfile,
        ReviewQueueItem,
        Session,
        Tenant,
        User,
    )

    assert Tenant.__tablename__ == "tenants"
    assert User.__tablename__ == "users"
    assert Identity.__tablename__ == "identities"
    assert Session.__tablename__ == "sessions"
    assert BreakGlassGrant.__tablename__ == "break_glass_grants"
    assert AuditEvent.__tablename__ == "audit_events"
    assert AIInteraction.__tablename__ == "ai_interactions"
    assert ReviewQueueItem.__tablename__ == "review_queue"
    assert PatientProfile.__tablename__ == "patient_profiles"
    assert AllergyRecord.__tablename__ == "allergies"
    assert GoutFlare.__tablename__ == "gout_flares"
    assert Consent.__tablename__ == "consents"
    assert DsrRequest.__tablename__ == "dsr_requests"
    from synapsemd_platform.models import CommandCatalogEntry, StoredObject

    assert CommandCatalogEntry.__tablename__ == "command_catalog"
    assert StoredObject.__tablename__ == "stored_objects"
    assert "body" not in StoredObject.__table__.columns.keys()
    from synapsemd_platform.models import (
        AppendOnlyError,
        BaaRecord,
        DsrRequest,
        LegalHold,
        ModelCatalogEntry,
        TenantModelPolicy,
    )

    assert issubclass(AppendOnlyError, RuntimeError)
    assert BaaRecord.__tablename__ == "baa_records"
    assert DsrRequest.__tablename__ == "dsr_requests"
    assert LegalHold.__tablename__ == "legal_holds"
    assert ModelCatalogEntry.__tablename__ == "model_catalog"
    assert TenantModelPolicy.__tablename__ == "tenant_model_policies"


def test_schema_package_reexports() -> None:
    from synapsemd_platform.models.ai import AIInteraction, ReviewQueueItem
    from synapsemd_platform.models.iam import BreakGlassGrant, Identity, Session, Tenant, User

    assert Tenant.__tablename__ == "tenants"
    assert User.__tablename__ == "users"
    assert Identity.__tablename__ == "identities"
    assert Session.__tablename__ == "sessions"
    assert BreakGlassGrant.__tablename__ == "break_glass_grants"
    assert AIInteraction.__tablename__ == "ai_interactions"
    assert ReviewQueueItem.__tablename__ == "review_queue"
