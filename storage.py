"""Модуль сохранения и загрузки данных проекта.

Чтение и запись JSON-файлов выполняются через контекстный менеджер with,
ошибки обрабатываются исключениями FileNotFoundError и JSONDecodeError.
"""

import json
import os

from typing import Dict, List


def load_documents(filename: str) -> Dict[int, dict]:
    """Загрузить документы из JSON-файла."""
    data = _load_json(filename)
    return {item["id"]: item for item in data}


def save_documents(filename: str, documents: Dict[int, dict]) -> None:
    """Сохранить документы в JSON-файл."""
    _save_json(filename, list(documents.values()))


def load_users(filename: str) -> Dict[int, dict]:
    """Загрузить пользователей из JSON-файла."""
    data = _load_json(filename)
    return {item["id"]: item for item in data}


def save_users(filename: str, users: Dict[int, dict]) -> None:
    """Сохранить пользователей в JSON-файл."""
    _save_json(filename, list(users.values()))


def load_approvals(filename: str) -> List[dict]:
    """Загрузить согласования из JSON-файла."""
    return _load_json(filename)


def save_approvals(filename: str, approvals: List[dict]) -> None:
    """Сохранить согласования в JSON-файл."""
    _save_json(filename, approvals)


def _load_json(filename: str) -> list:
    """Прочитать JSON-файл и вернуть список данных."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Файл {filename} не найден. Создана пустая коллекция.")
        return []
    except json.JSONDecodeError:
        print(f"Файл {filename} повреждён. Создана пустая коллекция.")
        return []


def _save_json(filename: str, data: list) -> None:
    """Записать данные в JSON-файл через контекстный менеджер."""
    directory = os.path.dirname(filename)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4,
        )
