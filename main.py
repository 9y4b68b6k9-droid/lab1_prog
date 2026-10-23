import json
import xml.etree.ElementTree as ET
from pathlib import Path

from exceptions import (
    DataFormatError, EmptyNameError, InvalidAgeLimitError,
    InvalidPriceError, InvalidSkillLimitError, SportSectionError
)
from models import Fight_Section, Team_Section

class Administration:
    """Сервис управления спортивным комплексом."""
    def __init__(self) -> None:
        self.fight_sections: list[Fight_Section] = []
        self.team_sections: list[Team_Section] = []

    def add_fight_section(self, section: Fight_Section) -> None:
        self.fight_sections.append(section)

    def add_team_section(self, section: Team_Section) -> None:
        self.team_sections.append(section)

    def save_fight_sections_json(self, path: str) -> None:
        data = [section.to_dict() for section in self.fight_sections]
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except OSError as exc:
            raise DataFormatError(f"Не удалось записать {path}: {exc}") from exc

    def load_fight_sections_json(self, path: str) -> None:
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, json.JSONDecodeError) as exc:
            raise DataFormatError(f"Не удалось прочитать {path}: {exc}") from exc
        self.fight_sections = [Fight_Section.from_dict(item) for item in data]

    def save_team_sections_xml(self, path: str) -> None:
        root = ET.Element("team_sections")
        for section in self.team_sections:
            root.append(section.to_xml())
        tree = ET.ElementTree(root)
        ET.indent(tree, space="  ")
        try:
            tree.write(path, encoding="utf-8", xml_declaration=True)
        except OSError as exc:
            raise DataFormatError(f"Не удалось записать XML {path}: {exc}") from exc

    def load_team_sections_xml(self, path: str) -> None:
        try:
            tree = ET.parse(path)
        except (OSError, ET.ParseError) as exc:
            raise DataFormatError(f"Не удалось прочитать XML {path}: {exc}") from exc
        root = tree.getroot()
        if root.tag != "team_sections":
            raise DataFormatError(f"Корневой тег должен быть <team_sections>, найден <{root.tag}>")
        self.team_sections = [Team_Section.from_xml(elem) for elem in root.findall("Team_Section")]

    def show_all(self) -> None:
        print("=" * 60)
        print("Секции единоборств (JSON):")
        for s in self.fight_sections:
            print("  -", s)
        print("Командные секции (XML):")
        for s in self.team_sections:
            print("  -", s)
        print("=" * 60)

def demo_exceptions() -> None:
    print("\n--- Демонстрация исключений ---")
    try:
        Fight_Section("", "Иванов", 1000, "middle", 18)
    except EmptyNameError as exc:
        print(f"EmptyNameError: {exc}")
    try:
        Fight_Section("Бокс", "Иванов", -100, "middle", 18)
    except InvalidPriceError as exc:
        print(f"InvalidPriceError: {exc}")
    try:
        Fight_Section("Бокс", "Иванов", 1000, "low", 18)
    except InvalidSkillLimitError as exc:
        print(f"InvalidSkillLimitError: {exc}")
    try:
        Fight_Section("Бокс", "Иванов", 1000, "middle", 10)
    except InvalidAgeLimitError as exc:
        print(f"InvalidAgeLimitError: {exc}")
    try:
        _ = 100 / 0
    except ZeroDivisionError as exc:
        print(f"ZeroDivisionError: {exc}")
    try:
        Team_Section("Футбол", "Петров", 2000, 0, "мяч")
    except ValueError as exc:
        print(f"ValueError: {exc}")
    try:
        adm = Administration()
        adm.load_fight_sections_json("no_such.json")
    except DataFormatError as exc:
        print(f"DataFormatError: {exc}")
    try:
        x = int("42")
    except ValueError:
        print("Это не число")
    else:
        print(f"else: успешное преобразование, x = {x}")
    finally:
        print("finally: выполняется всегда")

def main() -> None:
    demo_exceptions()
    adm = Administration()
    try:
        adm.add_fight_section(Fight_Section("Бокс", "Петров П.П.", 5000, "middle", 18))
        adm.add_fight_section(Fight_Section("Дзюдо", "Сидоров С.С.", 8000, "hard", 20))
        adm.add_team_section(Team_Section("Футбол", "Иванов И.И.", 2000, 11, "мяч"))
        adm.add_team_section(Team_Section("Волейбол", "Кузнецова А.А.", 3500, 6, "мяч"))
        print("Секции успешно созданы")
    except SportSectionError as exc:
        print(f"Ошибка при создании секций: {exc}")
        return
    try:
        adm.save_fight_sections_json("data_combats.json")
        adm.save_team_sections_xml("data_teams.xml")
        print("Файлы успешно созданы")
    except DataFormatError as exc:
        print(f"Ошибка создания файла: {exc}")
        return

    print("\n--- Сохранено в JSON ---")
    for s in adm.fight_sections:
        print(s)
    print("\n--- Сохранено в XML ---")
    for s in adm.team_sections:
        print(s)

    print("\n--- Проверка загрузки ---")
    adm2 = Administration()
    adm2.load_fight_sections_json("data_combats.json")
    adm2.load_team_sections_xml("data_teams.xml")
    adm2.show_all()

if __name__ == "__main__":
    main()
    