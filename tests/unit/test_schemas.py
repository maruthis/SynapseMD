from synapsemd_platform.api.schemas import (
    AiAnalyzeRequest,
    AiChatRequest,
    AiPredictRequest,
    AiReportRequest,
    CommandExecuteRequest,
    CommandExecuteResponse,
    LoginRequest,
    MigrateRequest,
    ReviewDecisionRequest,
    TenantCreate,
    TokenResponse,
    UserRegister,
)


def test_schema_models() -> None:
    tenant = TenantCreate(name="Clinic", plan="starter")
    assert tenant.plan == "starter"

    user = UserRegister(email="a@b.com", password="securepass1", role="patient")
    assert user.role == "patient"

    cmd = CommandExecuteRequest(command="goal", context_text="test")
    assert cmd.payload == {}

    migrate = MigrateRequest(source_directory="/tmp/data")
    assert migrate.source_directory == "/tmp/data"

    review = ReviewDecisionRequest(action="approve", clinician_notes="ok")
    assert review.action == "approve"

    token = TokenResponse(access_token="abc")
    assert token.token_type == "bearer"

    response = CommandExecuteResponse(
        interaction_id="int-1",
        command="goal",
        response="ok",
        model_used="mock",
        confidence=0.9,
        human_review_required=False,
    )
    assert response.command == "goal"


def test_ai_schema_models() -> None:
    assert AiPredictRequest(risk_type="hypertension").risk_type == "hypertension"
    assert AiAnalyzeRequest().time_range == "last_quarter"
    assert AiChatRequest(query="hello").query == "hello"
    assert AiReportRequest().report_type == "comprehensive"
