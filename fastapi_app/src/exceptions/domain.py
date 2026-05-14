class DomainError(Exception):
    def __init__(self, message: str, code: str = None):
        self.message = message
        self.code = code
        super().__init__(message)


class ValidationError(DomainError):
    def __init__(self, field: str, message: str, value: any = None):
        self.field = field
        self.value = value
        super().__init__(message, code="VALIDATION_ERROR")


class BusinessRuleError(DomainError):
    def __init__(self, rule_name: str, message: str):
        self.rule_name = rule_name
        super().__init__(message, code="BUSINESS_RULE_VIOLATION")


class PermissionError(DomainError):
    def __init__(self, action: str, entity: str):
        self.action = action
        self.entity = entity
        super().__init__(f"Permission denied: {action} on {entity}", code="PERMISSION_DENIED")
