from loader import logger


class BaseError(Exception):
    """
    Базовый класс для обработки ошибок
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
        logger.error(message)

    def __str__(self) -> str:
        return self.message

class UserAlreadyExist(BaseError):
    """
    Класс для обработки ошибок связанных с уже созданным именем под пользователя
    """
    ...

class UserInvalidPassword(BaseError):
    """
    Класс для обработки ошибок связанных с неправильным паролем для пользователя
    """
    ...

class ErrorWithOutLog(Exception):
    """
    Класс для обработки ошибок без создания лога    
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

    def __str__(self) -> str:
        return self.message
    
class AddURLError(ErrorWithOutLog):
    """
    Класс для обработки ошибок связанных с добавлением URL в отслеживаемые
    """
    ...

class NoURL(ErrorWithOutLog):
    """
    Класс для обработки ошибок связанных с попыткой взаимодействия
    с неотслеживаемыми URL
    """
    ...