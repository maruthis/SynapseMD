def test_models_package_exports() -> None:
    from synapsemd_platform.models import AIInteraction, AuditEvent, ReviewQueueItem, Tenant, User

    assert Tenant.__tablename__ == "tenants"
    assert User.__tablename__ == "users"
    assert AuditEvent.__tablename__ == "audit_events"
    assert AIInteraction.__tablename__ == "ai_interactions"
    assert ReviewQueueItem.__tablename__ == "review_queue"
