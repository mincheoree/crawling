from typing import Callable


class SpiderException(Exception):
    exception = Exception
    message = ''
    error_code = 'error'

    def __init__(self, message: str, exception) -> None:
        self.message = message
        self.exception = exception

        super().__init__(self.message)

    @staticmethod
    def __get_error_code(exception: Exception) -> str:
        # TODO implement like browser.exceptions
        raise NotImplementedError


class FailedWorkException(SpiderException):
    def __init__(self, spider_class, method: Callable = None) -> None:
        if method:
            self.message = f"failed {spider_class.__name__}.{method}()"
        else:
            self.message = f"failed {spider_class.__name__}."
        super().__init__(self.message, FailedWorkException)
