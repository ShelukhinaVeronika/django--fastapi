class DatabaseError(Exception):
    def __init__(self, message: str, original_error: Exception = None):
        self.message = message
        self.original_error = original_error
        super().__init__(message)


class NotFoundError(DatabaseError):
    def __init__(self, entity_name: str, entity_id: int):
        self.entity_name = entity_name
        self.entity_id = entity_id
        super().__init__(f"{entity_name} with id {entity_id} not found")


class UniqueConstraintError(DatabaseError):
    def __init__(self, entity_name: str, field: str, value: str):
        self.entity_name = entity_name
        self.field = field
        self.value = value
        super().__init__(f"{entity_name} with {field} '{value}' already exists")


class ForeignKeyError(DatabaseError):
    def __init__(self, entity_name: str, field: str, foreign_id: int):
        self.entity_name = entity_name
        self.field = field
        self.foreign_id = foreign_id
        super().__init__(
            f"Related {entity_name} with id {foreign_id} not found for field {field}"
        )
