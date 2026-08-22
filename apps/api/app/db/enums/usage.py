from enum import StrEnum


class UsageResource(StrEnum):
    """Supported subscription usage resources."""

    USERS = "users"
    STORAGE = "storage"
    API_CALLS = "api_calls"
    RECORDS = "records"
    TRANSACTIONS = "transactions"
    MODULES = "modules"
    AUTOMATION_EXECUTIONS = "automation_executions"
