"""Covenant extraction Pydantic schemas and schema router."""

from typing import List, Optional, Union

from pydantic import BaseModel, Field

from covenant_pipeline.schemas.nodes import SubLimitNode, UnifiedExceptions


class LeverageStepDown(BaseModel):
    start_date: Optional[str] = Field(None)
    end_date: Optional[str] = Field(None)
    ratio_limit: Union[float, str] = Field(...)
    triggering_event: Optional[str] = Field(None, description="e.g., 'Prior to the Acceptable PPA Date'")


class TotalLeverageIntermediate(BaseModel):
    is_false_flag: bool = Field(...)
    false_flag_reason: Optional[str] = Field(None)
    is_applicable: bool = Field(...)
    static_ratio_limit: Optional[Union[float, str]] = Field(None)
    step_downs: Optional[List[LeverageStepDown]] = Field(None)


class FixedChargeStep(BaseModel):
    start_date: Optional[str] = Field(None)
    end_date: Optional[str] = Field(None)
    ratio_limit: Union[float, str] = Field(...)


class FixedChargeIntermediate(BaseModel):
    is_false_flag: bool = Field(...)
    false_flag_reason: Optional[str] = Field(None)
    is_applicable: bool = Field(...)
    static_ratio_limit: Optional[Union[float, str]] = Field(None)
    step_ups: Optional[List[FixedChargeStep]] = Field(
        None, description="Step-ups or step-downs for the fixed charge ratio."
    )
    test_period: Optional[str] = Field(None)


class CapExIntermediate(BaseModel):
    is_false_flag: bool = Field(...)
    false_flag_reason: Optional[str] = Field(None)
    is_applicable: bool = Field(...)
    annual_limit_amount: Optional[Union[float, str]] = Field(
        None, description="The maximum dollar amount permitted for CapEx per year."
    )
    carry_forward_permitted: Optional[bool] = Field(
        None, description="True if unused CapEx can be carried forward to the next year."
    )


class RestrictedPaymentsIntermediate(BaseModel):
    is_false_flag: bool = Field(...)
    false_flag_reason: Optional[str] = Field(None)
    is_applicable: bool = Field(...)
    general_basket_limit: Optional[Union[float, str]] = Field(
        None, description="The general dollar basket limit for restricted payments."
    )
    conditional_payments: Optional[List[SubLimitNode]] = Field(
        None,
        description="Extract any restricted payments that are only permitted if specific financial conditions or ratios are met.",
    )


class InvestmentsIntermediate(BaseModel):
    is_false_flag: bool = Field(...)
    false_flag_reason: Optional[str] = Field(None)
    is_applicable: bool = Field(...)
    specific_carve_outs: Optional[List[SubLimitNode]] = Field(
        None, description="Extract EVERY distinct sub-limit category and dollar amount found in the section."
    )


class DebtIntermediate(BaseModel):
    is_false_flag: bool = Field(...)
    false_flag_reason: Optional[str] = Field(None)
    is_applicable: bool = Field(...)
    specific_carve_outs: Optional[List[SubLimitNode]] = Field(
        None,
        description="Extract EVERY distinct debt sub-limit category (e.g., Capital Leases, Subordinated Debt) and its dollar amount.",
    )


class ReportingIntermediate(BaseModel):
    is_false_flag: bool = Field(...)
    false_flag_reason: Optional[str] = Field(None)
    is_applicable: bool = Field(...)
    annual_financials_days: Optional[int] = Field(
        None, description="Extract ONLY the integer representing the number of days."
    )
    quarterly_financials_days: Optional[int] = Field(
        None, description="Extract ONLY the integer representing the number of days."
    )


class LiensIntermediate(BaseModel):
    """Phase 1 Extraction schema for Limitation on Liens."""

    is_false_flag: bool = Field(
        ..., description="Set to True ONLY IF the text is a cross-reference or lacks the actual covenant definition."
    )
    false_flag_reason: Optional[str] = Field(None)
    is_applicable: bool = Field(..., description="True if the text contains a valid restriction on liens.")
    exceptions: Optional[UnifiedExceptions] = Field(None)


class MergersIntermediate(BaseModel):
    """Phase 1 Extraction schema for Mergers and Consolidations."""

    is_false_flag: bool = Field(...)
    false_flag_reason: Optional[str] = Field(None)
    is_applicable: bool = Field(
        ..., description="True if the text restricts mergers, consolidations, or liquidations."
    )
    exceptions: Optional[UnifiedExceptions] = Field(None)


class CovenantIntermediate(BaseModel):
    is_false_flag: bool = Field(...)
    is_applicable: bool = Field(...)
    exceptions: Optional[UnifiedExceptions] = Field(None)


SCHEMA_ROUTER = {
    "TotalLeverageRatio": TotalLeverageIntermediate,
    "FixedChargeCoverageRatio": FixedChargeIntermediate,
    "CapitalExpenditures": CapExIntermediate,
    "RestrictedPayments": RestrictedPaymentsIntermediate,
    "InvestmentsAndAcquisitions": InvestmentsIntermediate,
    "DebtIncurrence": DebtIntermediate,
    "ReportingRequirements": ReportingIntermediate,
    "LimitationOnLiens": LiensIntermediate,
    "MergersAndConsolidations": MergersIntermediate,
}
