from abc import ABC, abstractmethod
import xml.etree.ElementTree as ET
from exceptions import (
    EmptyNameError, InvalidPriceError, InvalidSkillLimitError,
    InvalidAgeLimitError, DataFormatError )
class SportSection(ABC):
    """Абстрактная спортивная секция."""
    def __init__(self, name: str, coach: str, price: int) -> None:
        if not name or not name.strip():
            raise EmptyNameError("Название секции не может быть пустым")
        if price < 0 or price > 100000:
            raise InvalidPriceError(f"Стоимость {price} руб. невозможна")
        self.name = name.strip()
        self.coach = coach.strip()
        self.price = price
    @abstractmethod
    def get_info(self) -> str:
        pass
    def __str__(self) -> str:
        return self.get_info()
class Fight_Section(SportSection):
    """Секция единоборств."""
    def __init__(self, name: str, coach: str, price: int, skill: str, age: int) -> None:
        super().__init__(name, coach, price)
        if skill == "low":
            raise InvalidSkillLimitError("Слишком низкий уровень подготовки")
        if skill == "champion":
            raise InvalidSkillLimitError("Слишком высокий уровень подготовки")
        if age < 14 or age > 25:
            raise InvalidAgeLimitError("Неподходящий возраст")
        self.skill = skill.strip()
        self.age = age
    def get_info(self) -> str:
        return (f"Секция: {self.name}\nТренер: {self.coach}\nЦена: {self.price}\nУровень: {self.skill}\nВозраст: {self.age}\n")
    def to_dict(self) -> dict:
        return {"name": self.name, "coach": self.coach, "price": self.price, "skill": self.skill, "age": self.age}
    @classmethod
    def from_dict(cls, data: dict) -> "Fight_Section":
        try:
            return cls(name=data["name"], coach=data["coach"], price=int(data["price"]), skill=data["skill"], age=int(data["age"]))
        except (KeyError, TypeError, ValueError) as exc:
            raise DataFormatError(f"Некорректные данные секции: {exc}") from exc
class Team_Section(SportSection):
    """Командная секция."""
    def __init__(self, name: str, coach: str, price: int, team_size: int, inventory: str) -> None:
        super().__init__(name, coach, price)
        if team_size <= 0:
            raise ValueError("Количество игроков в команде меньше 1")
        self.team_size = team_size
        self.inventory = inventory
    def get_info(self) -> str:
        return (f"Секция: {self.name}\nТренер: {self.coach}\nЦена: {self.price}\nКоличество игроков: {self.team_size}\nИнвентарь: {self.inventory}\n")
    def to_xml(self) -> ET.Element:
        elem = ET.Element("Team_Section")
        ET.SubElement(elem, "name").text = self.name
        ET.SubElement(elem, "coach").text = self.coach
        ET.SubElement(elem, "price").text = str(self.price)
        ET.SubElement(elem, "team_size").text = str(self.team_size)
        ET.SubElement(elem, "inventory").text = self.inventory
        return elem
    @classmethod
    def from_xml(cls, element: ET.Element) -> "Team_Section":
        try:
            return cls(name=element.findtext("name", ""), coach=element.findtext("coach", ""), price=int(element.findtext("price", "0")), team_size=int(element.findtext("team_size", "0")), inventory=element.findtext("inventory", ""))
        except (TypeError, ValueError) as exc:
            raise DataFormatError(f"Некорректные данные командной секции: {exc}") from exc