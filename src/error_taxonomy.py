"""Error taxonomy for LLM inference pipeline.

Classifies errors into structured categories for detailed analysis:

Category Hierarchy:
├── INFRASTRUCTURE — Transient issues unrelated to the model itself
│   ├── network_error         — Connection lost, DNS failure, socket timeout
│   ├── service_unavailable   — Provider 5xx, server overloaded
│   └── authentication_error  — Invalid/expired API key, permission denied
│
├── PROVIDER_LIMIT — Provider-side rate/quota limits
│   ├── rate_limit            — Too many requests (429)
│   ├── quota_exceeded        — Billing quota / credit limit reached (key limit)
│   └── context_length        — Input too long for model's context window
│
├── PROVIDER_CONFIG — Configuration or availability issues on the provider/router
│   ├── model_not_found       — Model ID does not exist / no endpoints found
│   ├── model_unavailable     — No allowed providers available for model
│   └── invalid_request_params — Bad request params (e.g. reasoning mandatory)
│
├── MODEL_OUTPUT — Model returned a response but it's unusable
│   ├── parse_error           — Response doesn't match expected schema
│   ├── content_filter        — Response blocked by safety filter
│   ├── empty_response        — Model returned empty/null content
│   └── length_exceeded       — Output truncated (max_tokens hit)
│
└── UNKNOWN — Cannot classify the error
    └── unknown               — Catch-all for unrecognized exceptions
"""

from __future__ import annotations

from enum import Enum

import openai


class ErrorCategory(str, Enum):
    INFRASTRUCTURE = "infrastructure"
    PROVIDER_LIMIT = "provider_limit"
    PROVIDER_CONFIG = "provider_config"
    MODEL_OUTPUT = "model_output"
    UNKNOWN = "unknown"


class ErrorType(str, Enum):
    # Infrastructure
    NETWORK_ERROR = "network_error"
    SERVICE_UNAVAILABLE = "service_unavailable"
    AUTHENTICATION_ERROR = "authentication_error"

    # Provider limits
    RATE_LIMIT = "rate_limit"
    QUOTA_EXCEEDED = "quota_exceeded"
    CONTEXT_LENGTH = "context_length"

    # Provider config / availability
    MODEL_NOT_FOUND = "model_not_found"
    MODEL_UNAVAILABLE = "model_unavailable"
    INVALID_REQUEST_PARAMS = "invalid_request_params"

    # Model output issues
    PARSE_ERROR = "parse_error"
    CONTENT_FILTER = "content_filter"
    EMPTY_RESPONSE = "empty_response"
    LENGTH_EXCEEDED = "length_exceeded"

    # Unknown
    UNKNOWN = "unknown"


ERROR_TYPE_TO_CATEGORY: dict[ErrorType, ErrorCategory] = {
    ErrorType.NETWORK_ERROR: ErrorCategory.INFRASTRUCTURE,
    ErrorType.SERVICE_UNAVAILABLE: ErrorCategory.INFRASTRUCTURE,
    ErrorType.AUTHENTICATION_ERROR: ErrorCategory.INFRASTRUCTURE,
    ErrorType.RATE_LIMIT: ErrorCategory.PROVIDER_LIMIT,
    ErrorType.QUOTA_EXCEEDED: ErrorCategory.PROVIDER_LIMIT,
    ErrorType.CONTEXT_LENGTH: ErrorCategory.PROVIDER_LIMIT,
    ErrorType.MODEL_NOT_FOUND: ErrorCategory.PROVIDER_CONFIG,
    ErrorType.MODEL_UNAVAILABLE: ErrorCategory.PROVIDER_CONFIG,
    ErrorType.INVALID_REQUEST_PARAMS: ErrorCategory.PROVIDER_CONFIG,
    ErrorType.PARSE_ERROR: ErrorCategory.MODEL_OUTPUT,
    ErrorType.CONTENT_FILTER: ErrorCategory.MODEL_OUTPUT,
    ErrorType.EMPTY_RESPONSE: ErrorCategory.MODEL_OUTPUT,
    ErrorType.LENGTH_EXCEEDED: ErrorCategory.MODEL_OUTPUT,
    ErrorType.UNKNOWN: ErrorCategory.UNKNOWN,
}

# Whether a retry is meaningful for this error type
RETRYABLE_ERROR_TYPES: set[ErrorType] = {
    ErrorType.NETWORK_ERROR,
    ErrorType.SERVICE_UNAVAILABLE,
    ErrorType.RATE_LIMIT,
    ErrorType.MODEL_UNAVAILABLE,  # providers can come back online
}


def classify_error(exception: Exception) -> tuple[ErrorType, ErrorCategory]:
    """Classify an exception into an ErrorType and ErrorCategory.

    Args:
        exception: The exception raised during LLM inference.

    Returns:
        Tuple of (ErrorType, ErrorCategory).

    """
    # OpenAI-specific exceptions
    if isinstance(exception, openai.RateLimitError):
        msg = str(exception).lower()
        if "quota" in msg or "billing" in msg or "credit" in msg or "insufficient" in msg or "key limit" in msg:
            return ErrorType.QUOTA_EXCEEDED, ErrorCategory.PROVIDER_LIMIT
        return ErrorType.RATE_LIMIT, ErrorCategory.PROVIDER_LIMIT

    if isinstance(exception, openai.APIConnectionError):
        return ErrorType.NETWORK_ERROR, ErrorCategory.INFRASTRUCTURE

    if isinstance(exception, openai.APITimeoutError):
        return ErrorType.NETWORK_ERROR, ErrorCategory.INFRASTRUCTURE

    if isinstance(exception, openai.AuthenticationError):
        return ErrorType.AUTHENTICATION_ERROR, ErrorCategory.INFRASTRUCTURE

    if isinstance(exception, openai.PermissionDeniedError):
        msg = str(exception).lower()
        if "key limit" in msg or "quota" in msg or "billing" in msg:
            return ErrorType.QUOTA_EXCEEDED, ErrorCategory.PROVIDER_LIMIT
        return ErrorType.AUTHENTICATION_ERROR, ErrorCategory.INFRASTRUCTURE

    if isinstance(exception, openai.InternalServerError):
        return ErrorType.SERVICE_UNAVAILABLE, ErrorCategory.INFRASTRUCTURE

    if isinstance(exception, openai.BadRequestError):
        msg = str(exception).lower()
        if "context" in msg or "token" in msg and "max" in msg or "too long" in msg:
            return ErrorType.CONTEXT_LENGTH, ErrorCategory.PROVIDER_LIMIT
        if "content" in msg and "filter" in msg or "safety" in msg:
            return ErrorType.CONTENT_FILTER, ErrorCategory.MODEL_OUTPUT
        if "reasoning" in msg and ("mandatory" in msg or "cannot be disabled" in msg):
            return ErrorType.INVALID_REQUEST_PARAMS, ErrorCategory.PROVIDER_CONFIG
        if "structured" in msg and "not supported" in msg:
            return ErrorType.INVALID_REQUEST_PARAMS, ErrorCategory.PROVIDER_CONFIG
        return ErrorType.INVALID_REQUEST_PARAMS, ErrorCategory.PROVIDER_CONFIG

    if isinstance(exception, openai.NotFoundError):
        msg = str(exception).lower()
        if "no allowed providers" in msg or "not available" in msg:
            return ErrorType.MODEL_UNAVAILABLE, ErrorCategory.PROVIDER_CONFIG
        if "no endpoints" in msg or "not found" in msg:
            return ErrorType.MODEL_NOT_FOUND, ErrorCategory.PROVIDER_CONFIG
        return ErrorType.MODEL_NOT_FOUND, ErrorCategory.PROVIDER_CONFIG

    if isinstance(exception, openai.ContentFilterFinishReasonError):
        return ErrorType.CONTENT_FILTER, ErrorCategory.MODEL_OUTPUT

    if isinstance(exception, openai.LengthFinishReasonError):
        return ErrorType.LENGTH_EXCEEDED, ErrorCategory.MODEL_OUTPUT

    if isinstance(exception, openai.APIStatusError):
        status = getattr(exception, "status_code", 0)
        if status == 429:
            return ErrorType.RATE_LIMIT, ErrorCategory.PROVIDER_LIMIT
        if status >= 500:
            return ErrorType.SERVICE_UNAVAILABLE, ErrorCategory.INFRASTRUCTURE
        return ErrorType.UNKNOWN, ErrorCategory.UNKNOWN

    # Generic exceptions
    msg = str(exception).lower()

    if any(w in msg for w in ("connection", "network", "dns", "socket", "timeout", "timed out")):
        return ErrorType.NETWORK_ERROR, ErrorCategory.INFRASTRUCTURE

    if any(w in msg for w in ("rate limit", "429", "too many requests")):
        return ErrorType.RATE_LIMIT, ErrorCategory.PROVIDER_LIMIT

    if any(w in msg for w in ("key limit exceeded", "quota", "billing", "credit", "insufficient_quota")):
        return ErrorType.QUOTA_EXCEEDED, ErrorCategory.PROVIDER_LIMIT

    if any(w in msg for w in ("context length", "maximum context", "too long", "token limit")):
        return ErrorType.CONTEXT_LENGTH, ErrorCategory.PROVIDER_LIMIT

    if any(w in msg for w in ("no endpoints found", "model not found", "model_not_found")):
        return ErrorType.MODEL_NOT_FOUND, ErrorCategory.PROVIDER_CONFIG

    if any(w in msg for w in ("no allowed providers", "model unavailable", "not available for the selected")):
        return ErrorType.MODEL_UNAVAILABLE, ErrorCategory.PROVIDER_CONFIG

    if any(w in msg for w in ("reasoning is mandatory", "cannot be disabled", "structured output")):
        return ErrorType.INVALID_REQUEST_PARAMS, ErrorCategory.PROVIDER_CONFIG

    if any(w in msg for w in ("parse", "json", "schema", "validation", "pydantic")):
        return ErrorType.PARSE_ERROR, ErrorCategory.MODEL_OUTPUT

    if any(w in msg for w in ("content_filter", "content filter", "safety", "moderation")):
        return ErrorType.CONTENT_FILTER, ErrorCategory.MODEL_OUTPUT

    if any(w in msg for w in ("empty", "none", "null")) and "response" in msg:
        return ErrorType.EMPTY_RESPONSE, ErrorCategory.MODEL_OUTPUT

    return ErrorType.UNKNOWN, ErrorCategory.UNKNOWN


# Column names for error-related fields in CSV output
ERROR_COLUMNS = ["error_type", "error_category"]

# Columns tracking retry counts per error type
RETRY_COUNT_COLUMNS = [f"retries_{et.value}" for et in ErrorType] + ["retries_total"]
