"""Validation audit schema."""

from typing import List, Optional

from pydantic import BaseModel, Field


class ValidationAudit(BaseModel):
    """Schema for the Node L LLM-as-a-Judge output."""

    is_verified: bool = Field(
        ...,
        description="True ONLY if every numerical value and [$REF] tag perfectly matches the source text.",
    )
    confidence_score: float = Field(
        ...,
        description="A DATA FIDELITY SCORE from 0.0 to 1.0.",
    )
    requires_human_context: bool = Field(
        ...,
        description="True if the source text is inherently ambiguous, contradictory, or relies on an external schedule not present in the text.",
    )
    flagged_discrepancies: Optional[List[str]] = Field(
        None,
        description="If is_verified is False, provide a detailed list explaining exactly which keys failed and why.",
    )
