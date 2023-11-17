import logging
import os
from typing import Callable, Any

class Logger:
    """
    A decorator class for logging function calls and exceptions.
    """
    _logger = logging.getLogger("Logger laundry")
    _logger.setLevel(logging.INFO)
    _log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logfile.log")
    _file_handler = logging.FileHandler(_log_file_path)
    _formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    _file_handler.setFormatter(_formatter)
    _logger.addHandler(_file_handler)
    @staticmethod
    def log_record(func: Callable[..., Any]) -> Callable[..., Any]:
        """
        Decorator function for logging function calls and exceptions.

        Args:
            func: The function to be decorated.

        Returns:
            The decorated function.
        """
        def wrapper(*args, **kwargs) -> Any:
            """
            Wrapper function that logs the function call and exceptions.

            Args:
                *args: Variable length argument list.
                **kwargs: Arbitrary keyword arguments.

            Returns:
                The result of the decorated function.

            Raises:
                Any exception raised by the decorated function.
            """
            class_name = func.__qualname__.split(".")[0]  # Get the class name
            arg_names = list(args)
            arg_values = ", ".join(f"{name}={repr(value)}" for name, value in zip(arg_names, args))  # Format argument values
            kwargs_values = ", ".join(f"{name}={repr(value)}" for name, value in kwargs.items())  # Format keyword argument values
            all_args = ", ".join(filter(None, [arg_values, kwargs_values]))  # Combine all argument values
            Logger._logger.info(f"Calling function: {class_name}.{func.__name__}({all_args})")
            try:
                result = func(*args, **kwargs)
                Logger._logger.info(f"Function {func.__name__} completed successfully")
                return result
            except Exception as e:
                Logger._logger.error(f"Function {func.__name__} failed: {str(e)}")
                raise
        return wrapper




if __name__ == "__main__":
    import sys
    @Logger.log_record
    def my_function():
        print("This is my function")

    @Logger.log_record
    def another_function():
        print("This is another function")

    my_function()
    another_function()