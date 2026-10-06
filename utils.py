"""Вспомогательные функции безопасного ввода."""

from datetime import date


def input_int(prompt: str) -> int:
    """Запросить у пользователя целое число."""
    while True:
        raw = input(prompt)
        try:
            return int(raw)
        except ValueError:
            print("Ошибка: необходимо ввести целое число.")


def input_date(prompt: str) -> date:
    """Запросить у пользователя дату в формате ДД.ММ.ГГГГ."""
    while True:
        raw = input(prompt)
        try:
            day, month, year = raw.split(".")
            return date(int(year), int(month), int(day))
        except ValueError:
            print(
                "Ошибка: неверный формат даты. "
                "Используйте ДД.ММ.ГГГГ, например 15.10.2026."
            )


def input_str(prompt: str) -> str:
    """Запросить у пользователя непустую строку."""
    while True:
        raw = input(prompt).strip()
        if raw:
            return raw
        print("Ошибка: значение не может быть пустым.")
