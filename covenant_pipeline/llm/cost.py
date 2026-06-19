"""API cost calculation for Gemini models."""

from covenant_pipeline.config import INPUT_PRICE_PER_MILLION, OUTPUT_PRICE_PER_MILLION


def calculate_api_cost(usage_metadata) -> dict:
    """Calculate cost based on Gemini 3.1 Flash-Lite rates."""
    input_tokens = usage_metadata.prompt_token_count
    output_tokens = usage_metadata.candidates_token_count
    total_tokens = usage_metadata.total_token_count

    input_cost = (input_tokens / 1_000_000) * INPUT_PRICE_PER_MILLION
    output_cost = (output_tokens / 1_000_000) * OUTPUT_PRICE_PER_MILLION
    total_cost = input_cost + output_cost

    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
        "input_cost_usd": input_cost,
        "output_cost_usd": output_cost,
        "total_cost_usd": total_cost,
    }
