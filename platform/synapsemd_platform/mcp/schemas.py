from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class McpAuthContext(BaseModel):
    user_id: UUID
    tenant_id: UUID
    roles: list[str] = Field(default_factory=list)
    scopes: list[str] = Field(default_factory=list)


class ListCommandsResult(BaseModel):
    commands: list[str]
    count: int


class ExecuteCommandInput(BaseModel):
    command: str
    context_text: str = ""
    payload: dict[str, Any] = Field(default_factory=dict)


class ExecuteCommandResult(BaseModel):
    interaction_id: str
    command: str
    response: str
    model_used: str
    confidence: float
    human_review_required: bool
    blocked: bool
    disclaimer: str | None = None


class ProfileSummaryResult(BaseModel):
    patient_id: str
    gender: str | None = None
    birth_date: str | None = None
    resource_count: int


class QueryFhirInput(BaseModel):
    resource_type: str | None = None
    limit: int = Field(default=20, ge=1, le=100)


class QueryFhirResult(BaseModel):
    resources: list[dict[str, Any]]
    count: int


class SearchKnowledgeInput(BaseModel):
    query: str
    top_k: int = Field(default=3, ge=1, le=10)
    include_org_intelligence: bool = False


class KnowledgeHit(BaseModel):
    id: str
    source: str
    text: str
    score: float | None = None


class SearchKnowledgeResult(BaseModel):
    hits: list[KnowledgeHit]
    count: int


class AuditSummaryResult(BaseModel):
    events: list[dict[str, Any]]
    count: int


class AiAnalyzeInput(BaseModel):
    time_range: str = "last_quarter"


class AiPredictInput(BaseModel):
    risk_type: str = "hypertension"


class AiChatInput(BaseModel):
    query: str = Field(min_length=1)


class AiReportInput(BaseModel):
    report_type: str = "comprehensive"
    time_range: str = "last_quarter"


class AiActionResult(BaseModel):
    action: str
    result: dict[str, Any]
    disclaimer: str | None = None
    human_review_required: bool = False
