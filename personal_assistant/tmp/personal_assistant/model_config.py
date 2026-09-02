import os

from dotenv import load_dotenv
from google.adk.models.lite_llm import LiteLlm


load_dotenv()

if not os.getenv("GEMINI_API_KEY"):
    google_api_key = os.getenv("GOOGLE_API_KEY") or os.getenv(
        "GOOGLE_GENERATIVE_AI_API_KEY"
    )
    if google_api_key:
        os.environ["GEMINI_API_KEY"] = google_api_key

MODEL_ALIASES = {
    "gemini": "gemini/gemini-2.5-flash",
    "claude": "anthropic/claude-sonnet-4-20250514",
    "openai": "openai/gpt-5.4-mini",
}


def get_model(model_name: str | None = None) -> LiteLlm:
    """Build a LiteLLM model from an alias or provider-qualified model ID."""
    configured_model = model_name or os.getenv("ASSISTANT_MODEL", "gemini")
    model_name = MODEL_ALIASES.get(configured_model.lower(), configured_model)

    if "/" not in model_name:
        supported_models = ", ".join(sorted(MODEL_ALIASES))
        raise ValueError(
            f"ASSISTANT_MODEL must be a provider/model ID or one of: {supported_models}"
        )

    return LiteLlm(model=model_name)