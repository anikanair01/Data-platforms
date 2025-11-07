from jsonschema import validate, ValidationError

class SchemaValidator(Exception):
    def __init__(self, schema):
        self.schema = schema

    def validate(self, data):
        try:
            validate(instance=data, schema=self.schema)
            return True
        except ValidationError as e:
            print(f"Validation error: {e.message}")
            return False


# Example usage:
if __name__ == "__main__":
    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer", "minimum": 0}
        },
        "required": ["name", "age"]
    }
    validator = SchemaValidator(schema)

    valid_data = {"name": "Alice", "age": 30}
    invalid_data = {"name": "Bob", "age": -5}

    print("Valid data test:", validator.validate(valid_data))  # Should print: True
    print("Invalid data test:", validator.validate(invalid_data))  # Should print: Validation error and False