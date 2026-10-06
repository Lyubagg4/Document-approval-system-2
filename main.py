"""Точка запуска приложения и основной сценарий взаимодействия.

Модуль main.py организует пользовательский интерфейс и работу с
коллекциями объектов Document, User и Approval. Здесь же реализованы
функции пользовательских сценариев: добавление документа, добавление
пользователя, создание и отмена согласования, вывод списков.
"""

import os
from datetime import date
from typing import List

from models import Approval, Document, User
from models.approvals import (
    can_approve_document,
    cancel_approval,
    create_approval,
    find_approval_by_id,
    get_approval_status,
    show_approvals,
)
from models.documents import (
    add_document,
    find_document,
    find_document_by_id,
    show_documents,
    sort_documents_by_deadline,
)
from models.users import (
    add_user,
    find_user,
    find_user_by_id,
    show_users,
)
from storage import (
    load_approvals,
    load_documents,
    load_users,
    save_approvals,
    save_documents,
    save_users,
)
from utils import input_date, input_int, input_str

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
DOCUMENTS_FILE = os.path.join(DATA_DIR, "documents.json")
USERS_FILE = os.path.join(DATA_DIR, "users.json")
APPROVALS_FILE = os.path.join(DATA_DIR, "approvals.json")


def main() -> None:
    """Точка запуска приложения: загрузка данных, меню, сохранение."""
    print("=== Система согласования документов ===")

    documents = load_documents(DOCUMENTS_FILE)
    users = load_users(USERS_FILE)
    approvals = load_approvals(APPROVALS_FILE, documents, users)

    menu_items = build_menu_items()

    while True:
        print("\n--- Главное меню ---")
        for index, (label, _) in enumerate(menu_items, start=1):
            print(f"{index}. {label}")
        print("0. Выход")

        choice = input_int("Выберите действие: ")
        if choice == 0:
            break
        if 1 <= choice <= len(menu_items):
            _, handler = menu_items[choice - 1]
            handler(documents, users, approvals)
        else:
            print("Ошибка: неверный номер действия.")

    save_documents(DOCUMENTS_FILE, documents)
    save_users(USERS_FILE, users)
    save_approvals(APPROVALS_FILE, approvals)
    print("\nДанные сохранены. До свидания!")


def build_menu_items() -> list:
    """Вернуть список пунктов меню (название, обработчик).

    Returns:
        Список кортежей (метка, функция-обработчик).
    """
    return [
        ("Показать документы", show_documents_menu),
        ("Найти документ по названию", find_document_menu),
        ("Отсортировать документы по сроку", sort_documents_menu),
        ("Показать пользователей", show_users_menu),
        ("Найти пользователя", find_user_menu),
        ("Добавить документ", add_document_menu),
        ("Добавить пользователя", add_user_menu),
        ("Проверить возможность согласования", check_approval_menu),
        ("Создать согласование", create_approval_menu),
        ("Отменить согласование", cancel_approval_menu),
        ("Показать согласования", show_approvals_menu),
        ("Показать статус документа", show_status_menu),
    ]


def show_documents_menu(
    documents: List[Document],
    users: List[User],
    approvals: List[Approval],
) -> None:
    """Вывести список всех документов."""
    show_documents(documents, approvals)


def find_document_menu(
    documents: List[Document],
    users: List[User],
    approvals: List[Approval],
) -> None:
    """Найти документы по подстроке названия."""
    query = input_str("Введите подстроку для поиска: ")
    found = find_document(documents, query)
    show_documents(found, approvals)


def sort_documents_menu(
    documents: List[Document],
    users: List[User],
    approvals: List[Approval],
) -> None:
    """Вывести документы, отсортированные по сроку."""
    sorted_documents = sort_documents_by_deadline(documents)
    show_documents(sorted_documents, approvals)


def show_users_menu(
    documents: List[Document],
    users: List[User],
    approvals: List[Approval],
) -> None:
    """Вывести список пользователей."""
    show_users(users)


def find_user_menu(
    documents: List[Document],
    users: List[User],
    approvals: List[Approval],
) -> None:
    """Найти пользователя по подстроке ФИО или email."""
    query = input_str("Введите подстроку для поиска: ")
    found = find_user(users, query)
    show_users(found)


def add_document_menu(
    documents: List[Document],
    users: List[User],
    approvals: List[Approval],
) -> None:
    """Добавить новый документ."""
    if not users:
        print("Сначала добавьте хотя бы одного пользователя.")
        return
    show_users(users)
    author_id = input_int("Введите ID автора документа: ")
    author = find_user_by_id(users, author_id)
    if author is None:
        print("Ошибка: пользователь не найден.")
        return
    title = input_str("Введите название документа: ")
    doc_type = input_str("Введите тип документа: ")
    deadline = input_date("Введите срок согласования (ДД.ММ.ГГГГ): ")
    document = add_document(documents, title, doc_type, author_id, deadline)
    print(f"Документ добавлен: {document}")


def add_user_menu(
    documents: List[Document],
    users: List[User],
    approvals: List[Approval],
) -> None:
    """Добавить нового пользователя."""
    name = input_str("Введите ФИО пользователя: ")
    department = input_str("Введите подразделение: ")
    role = input_str("Введите должность: ")
    email = input_str("Введите email: ")
    user = add_user(users, name, department, role, email)
    print(f"Пользователь добавлен: {user}")


def check_approval_menu(
    documents: List[Document],
    users: List[User],
    approvals: List[Approval],
) -> None:
    """Проверить возможность согласования документа."""
    show_documents(documents, approvals)
    doc_id = input_int("Введите ID документа: ")
    document = find_document_by_id(documents, doc_id)
    if document is None:
        print("Ошибка: документ не найден.")
        return
    show_users(users)
    user_id = input_int("Введите ID согласующего: ")
    user = find_user_by_id(users, user_id)
    if user is None:
        print("Ошибка: пользователь не найден.")
        return
    allowed, message = can_approve_document(
        approvals, document, user, date.today()
    )
    print(message)


def create_approval_menu(
    documents: List[Document],
    users: List[User],
    approvals: List[Approval],
) -> None:
    """Создать согласование документа."""
    show_documents(documents, approvals)
    doc_id = input_int("Введите ID документа: ")
    document = find_document_by_id(documents, doc_id)
    if document is None:
        print("Ошибка: документ не найден.")
        return
    show_users(users)
    user_id = input_int("Введите ID согласующего: ")
    user = find_user_by_id(users, user_id)
    if user is None:
        print("Ошибка: пользователь не найден.")
        return
    print("1 — Согласовать")
    print("2 — Отклонить")
    decision_code = input_int("Введите номер решения: ")
    if decision_code == 1:
        decision = "approved"
    elif decision_code == 2:
        decision = "rejected"
    else:
        print("Ошибка: необходимо выбрать 1 или 2.")
        return
    comment = input_str("Введите комментарий: ")
    approval = create_approval(
        approvals,
        document,
        user,
        decision,
        comment,
        date.today(),
    )
    if approval is None:
        print("Согласование не создано: нарушены правила согласования.")
    else:
        print(f"Согласование создано: {approval}")


def cancel_approval_menu(
    documents: List[Document],
    users: List[User],
    approvals: List[Approval],
) -> None:
    """Отменить согласование."""
    show_approvals(approvals, documents, users)
    approval_id = input_int("Введите ID согласования: ")
    approval = find_approval_by_id(approvals, approval_id)
    if approval is None:
        print("Ошибка: согласование не найдено.")
        return
    cancel_approval(approvals, approval_id)
    print(f"Согласование #{approval_id} отменено.")


def show_approvals_menu(
    documents: List[Document],
    users: List[User],
    approvals: List[Approval],
) -> None:
    """Вывести список согласований."""
    show_approvals(approvals, documents, users)


def show_status_menu(
    documents: List[Document],
    users: List[User],
    approvals: List[Approval],
) -> None:
    """Вывести текущий статус документа."""
    show_documents(documents, approvals)
    doc_id = input_int("Введите ID документа: ")
    document = find_document_by_id(documents, doc_id)
    if document is None:
        print("Ошибка: документ не найден.")
        return
    status = get_approval_status(approvals, document)
    print(f"Статус документа: {status}")


if __name__ == "__main__":
    main()
