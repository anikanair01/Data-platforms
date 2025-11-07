from functools import wraps
import logging
class Apperror(Exception):
    """Custom application error class."""
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.status_code = status_code
        self.message = message

def handle_errors(logger=None):
    """Decorator to handle errors in functions."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Apperror as ae:
                if logger:
                    logger.error(f"Application error: {ae.message} (Status code: {ae.status_code})")
                return {"error": ae.message, "status_code": ae.status_code}
            except Exception as e:
                if logger:
                    logger.error(f"Unexpected error: {str(e)}")
                return {"error": "An unexpected error occurred.", "status_code": 500}
        return wrapper
    return decorator

# Example usage:
if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.ERROR)
    logger = logging.getLogger(__name__)

    @handle_errors(logger)
    def divide(a, b):
        if b == 0:
            raise Apperror("Division by zero is not allowed.")
        return a / b

    # Test the function
    print(divide(10, 5))  # Should print 5.0
    print(divide(308, 0))  # Should log an error and return an error message