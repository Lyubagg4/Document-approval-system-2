"""Модуль сохранения и загрузки данных проекта.

Все данные проекта хранятся в JSON-файлах каталога data/. Модуль выполняет
преобразование между JSON-структурами и объектами классов Document, User
и Approval. Чтение и запись файлов выполняются через контекстный менеджер
with, ошибки обрабатываются исключениями.
"""

import json
import os
from typing import List

from models import Approval, Document, User
from models.approvals import find_document_in_list, find_user_in_list


def load_documents(filename: str) -> List[Document]:
    """Загрузить документы из JSON-файла.

    Args:
        filename: путь к JSON-файлу.

    Returns:
        Список объектов Document. При отсутствии файла возвращается [].
    """
    data = _load_json(filename)
    return [Document.from_data(item) for item in data]


def save_documents(filename: str, documents: List[Document]) -> None:
    """Сохранить коллекцию документов в JSON-файл.

    Args:
        filename: путь к JSON-файлу;
        documents: коллекция объектов Document.
    """
    data = [document.to_dict() for document in documents]
    _save_json(filename, data)


def load_users(filename: str) -> List[User]:
    """Загрузить пользователей из JSON-файла.

    Args:
        filename: путь к JSON-файлу.

    Returns:
        Список объектов User.
    """
    data = _load_json(filename)
    return [User.from_data(item) for item in data]


def save_users(filename: str, users: List[User]) -> None:
    """Сохранить коллекцию пользователей в JSON-файл.

    Args:
        filename: путь к JSON-файлу;
        users: коллекция объектов User.
    """
    data = [user.to_dict() for user in users]
    _save_json(filename, data)


def load_approvals(
    filename: str,
    documents: List[Document],
    users: List[User],
) -> List[Approval]:
    """Загрузить согласования из JSON-файла.

    Восстанавливаются связи согласований с документами и пользователями
    по их идентификаторам. Если документ или пользователь не найдены,
    согласование пропускается.

    Args:
        filename: путь к JSON-файлу;
        documents: коллекция документов для восстановления связей;
        users: коллекция пользователей для восстановления связей.

    Returns:
        Список объектов Approval.
    """
    data = _load_json(filename)
    approvals: List[Approval] = []
    for item in data:
        document = find_document_in_list(documents, item["document_id"])
        user = find_user_in_list(users, item["user_id"])
        if document is None or user is None:
            continue
        approval = Approval.from_data(item)
        approvals.append(approval)
    return approvals


def save_approvals(filename: str, approvals: List[Approval]) -> None:
    """Сохранить коллекцию согласований в JSON-файл.

    Args:
        filename: путь к JSON-файлу;
        approvals: коллекция объектов Approval.
    """
    data = [approval.to_dict() for approval in approvals]
    _save_json(filename, data)


def _load_json(filename: str) -> list:
    """Прочитать JSON-файл и вернуть список данных.

    Обрабатывает отсутствие файла и некорректный JSON. При ошибке
    возвращается пустой список — приложение продолжает работу с пустыми
    данными, а не завершается аварийно.

    Args:
        filename: путь к JSON-файлу.

    Returns:
        Список словарей с данными.
    """
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
    """Записать данные в JSON-файл через контекстный менеджер.

    Args:
        filename: путь к JSON-файлу;
        data: список словарей.
    """
    directory = os.path.dirname(filename)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4,
            sort_keys=False,
        )
