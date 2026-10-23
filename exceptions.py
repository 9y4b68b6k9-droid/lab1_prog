class SportSectionError(Exception):
    """Базовое собственное исключение для спортивного комплекса."""

class EmptyNameError(SportSectionError):
    """Название секции не может быть пустым."""

class InvalidPriceError(SportSectionError):
    """Стоимость абонемента вне допустимого диапазона."""

class InvalidSkillLimitError(SportSectionError):
    """Неподходящий уровень подготовки."""

class InvalidAgeLimitError(SportSectionError):
    """Некорректное возрастное ограничение."""

class DataFormatError(SportSectionError):
    """Ошибка формата данных при чтении/записи файла."""
    