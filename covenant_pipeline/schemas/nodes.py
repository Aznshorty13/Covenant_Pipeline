"""Foundational Pydantic nodes for covenant schemas."""

from typing import List, Optional, Union

from pydantic import BaseModel, Field


class ConditionNode(BaseModel):
    condition_description: str = Field(
        ..., description="The logic or trigger required, e.g., 'Total Leverage Ratio <= 2.00 to 1.00'"
    )
    reference_tags: Optional[List[str]] = Field(
        None, description="Any defined terms within the condition, e.g., ['[$REF: Total Leverage Ratio]']"
    )


class SubLimitNode(BaseModel):
    category_name: str = Field(
        ..., description="The specific category or carve-out, e.g., 'ERAS SPVs' or 'Subordinated Debt'"
    )
    limit_amount: Union[float, str] = Field(
        ..., description="The maximum dollar limit for this specific category."
    )
    conditions: Optional[List[ConditionNode]] = Field(None, description="Any conditions that must be met.")


class CarveOutNode(BaseModel):
    description: str = Field(..., description="The summary of the exception.")
    quantitative_limit: Optional[float] = Field(
        None,
        description="Extract any specific dollar or ratio limits mentioned within this exception. Output ONLY the float.",
    )
    reference_tags: Optional[List[str]] = Field(
        None,
        description="Any defined terms within this specific exception, e.g., ['[$REF: Permitted Acquisition]']",
    )


class UnifiedExceptions(BaseModel):
    """A dynamic schema that handles both inline lists and external references."""

    defined_term_refs: Optional[List[str]] = Field(
        None,
        description="If the covenant permits exceptions using a capitalized defined term, extract them here formatted exactly as [$REF: Exact Term Name].",
    )
    inline_list_summaries: Optional[List[CarveOutNode]] = Field(
        None,
        description="If the covenant explicitly lists exceptions directly in the text, extract each one as a separate object.",
    )
