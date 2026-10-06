"""Точка запуска приложения и основной сценарий взаимодействия.

Модуль main.py организует пользовательский интерфейс и работу с
коллекциями объектов Document, User и Approval. Меню построено по принципу
CRUD: для каждой сущности доступны операции создания, поиска,
обновления и удаления, а также вывод списка.
"""

import os
from datetime import date
from typing import List

from models import Approval, Document, User
from models.approvals import (
    add_approval,
    delete_approval,
    find_approval,
    show_approvals,
    update_approval,
)
from models.documents import (
    add_document,
    delete_document,
    find_document,
    show_documents,
    update_document,
)
from models.users import (
    add_user,
    delete_user,
    find_user,
    show_users,
    update_user,
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

    while True:
        print("\n--- Главное меню ---")
        print("1. Показать документы")
        print("2. Добавить документ")
        print("3. Найти документ по ID")
        print("4. Обновить документ")
        print("5. Удалить документ")
        print("6. Показать пользователей")
        print("7. Добавить пользователя")
        print("8. Найти пользователя по ID")
        print("9. Обновить пользователя")
        print("10. Удалить пользователя")
        print("11. Показать согласования")
        print("12. Добавить согласование")
        print("13. Найти согласование по ID")
        print("14. Обновить согласование")
        print("15. Удалить согласование")
        print("0. Выход")

        choice = input_int("Выберите действие: ")
        if choice == 0:
            break
        elif choice == 1:
            show_documents(documents)
        elif choice == 2:
            create_document_menu(documents, users)
        elif choice == 3:
            find_document_menu(documents)
        elif choice == 4:
            update_document_menu(documents)
        elif choice == 5:
            delete_document_menu(documents)
        elif choice == 6:
            show_users(users)
        elif choice == 7:
            create_user_menu(users)
        elif choice == 8:
            find_user_menu(users)
        elif choice == 9:
            update_user_menu(users)
        elif choice == 10:
            delete_user_menu(users)
        elif choice == 11:
            show_approvals(approvals, documents, users)
        elif choice == 12:
            create_approval_menu(approvals, documents, users)
        elif choice == 13:
            find_approval_menu(approvals, documents, users)
        elif choice == 14:
            update_approval_menu(approvals)
        elif choice == 15:
            delete_approval_menu(approvals)
        else:
            print("Ошибка: неверный номер действия.")

    save_documents(DOCUMENTS_FILE, documents)
    save_users(USERS_FILE, users)
    save_approvals(APPROVALS_FILE, approvals)
    print("\nДанные сохранены. До свидания!")


def create_document_menu(
    documents: List[Document],
    users: List[User],
) -> None:
    """Добавить новый документ."""
    if not users:
        print("Сначала добавьте хотя бы одного пользователя.")
        return
    show_users(users)
    author_id = input_int("Введите ID автора документа: ")
    if find_user(users, author_id) is None:
        print("Ошибка: пользователь не найден.")
        return
    title = input_str("Введите название документа: ")
    doc_type = input_str("Введите тип документа: ")
    deadline = input_date("Введите срок согласования (ДД.ММ.ГГГГ): ")
    document = add_document(
        documents, title, doc_type, author_id, deadline
    )
    print(f"Документ добавлен: {document}")


def find_document_menu(documents: List[Document]) -> None:
    """Найти документ по идентификатору."""
    doc_id = input_int("Введите ID документа: ")
    document = find_document(documents, doc_id)
    if document is None:
        print("Документ не найден.")
    else:
        print(document)


def update_document_menu(documents: List[Document]) -> None:
    """Обновить данные документа."""
    doc_id = input_int("Введите ID документа: ")
    if find_document(documents, doc_id) is None:
        print("Документ не найден.")
        return
    print("Оставьте поле пустым, чтобы не менять значение.")
    title = input("Новое название: ").strip() or None
    doc_type = input("Новый тип: ").strip() or None
    deadline_raw = input("Новый срок (ДД.ММ.ГГГГ): ").strip()
    deadline = (
        input_date("Новый срок (ДД.ММ.ГГГГ): ")
        if deadline_raw
        else None
    )
    if update_document(
        documents, doc_id, title=title,
        doc_type=doc_type, deadline=deadline,
    ):
        print("Документ обновлён.")
    else:
        print("Ошибка: документ не найден.")


def delete_document_menu(documents: List[Document]) -> None:
    """Удалить документ."""
    doc_id = input_int("Введите ID документа: ")
    if delete_document(documents, doc_id):
        print(f"Документ #{doc_id} удалён.")
    else:
        print("Документ не найден.")


def create_user_menu(users: List[User]) -> None:
    """Добавить нового пользователя."""
    name = input_str("Введите ФИО пользователя: ")
    department = input_str("Введите подразделение: ")
    role = input_str("Введите должность: ")
    email = input_str("Введите email: ")
    user = add_user(users, name, department, role, email)
    print(f"Пользователь добавлен: {user}")


def find_user_menu(users: List[User]) -> None:
    """Найти пользователя по идентификатору."""
    user_id = input_int("Введите ID пользователя: ")
    user = find_user(users, user_id)
    if user is None:
        print("Пользователь не найден.")
    else:
        print(user)


def update_user_menu(users: List[User]) -> None:
    """Обновить данные пользователя."""
    user_id = input_int("Введите ID пользователя: ")
    if find_user(users, user_id) is None:
        print("Пользователь не найден.")
        return
    print("Оставьте поле пустым, чтобы не менять значение.")
    name = input("Новое ФИО: ").strip() or None
    department = input("Новое подразделение: ").strip() or None
    role = input("Новая должность: ").strip() or None
    email = input("Новый email: ").strip() or None
    if update_user(
        users, user_id, name=name,
        department=department, role=role, email=email,
    ):
        print("Пользователь обновлён.")
    else:
        print("Ошибка: пользователь не найден.")


def delete_user_menu(users: List[User]) -> None:
    """Удалить пользователя."""
    user_id = input_int("Введите ID пользователя: ")
    if delete_user(users, user_id):
        print(f"Пользователь #{user_id} удалён.")
    else:
        print("Пользователь не найден.")


def create_approval_menu(
    approvals: List[Approval],
    documents: List[Document],
    users: List[User],
) -> None:
    """Добавить новое согласование."""
    show_documents(documents)
    document_id = input_int("Введите ID документа: ")
    show_users(users)
    user_id = input_int("Введите ID согласующего: ")
    print("1 — Согласовать, 2 — Отклонить")
    code = input_int("Введите номер решения: ")
    if code == 1:
        decision = "approved"
    elif code == 2:
        decision = "rejected"
    else:
        print("Ошибка: необходимо выбрать 1 или 2.")
        return
    comment = input_str("Введите комментарий: ")
    approval, message = add_approval(
        approvals,
        documents,
        document_id,
        user_id,
        decision,
        comment,
        date.today(),
    )
    if approval is None:
        print(message)
    else:
        print(f"Согласование #{approval.id} создано.")


def find_approval_menu(
    approvals: List[Approval],
    documents: List[Document],
    users: List[User],
) -> None:
    """Найти согласование по идентификатору."""
    approval_id = input_int("Введите ID согласования: ")
    approval = find_approval(approvals, approval_id)
    if approval is None:
        print("Согласование не найдено.")
    else:
        show_approvals([approval], documents, users)


def update_approval_menu(approvals: List[Approval]) -> None:
    """Обновить данные согласования."""
    approval_id = input_int("Введите ID согласования: ")
    if find_approval(approvals, approval_id) is None:
        print("Согласование не найдено.")
        return
    print("Оставьте поле пустым, чтобы не менять значение.")
    decision_raw = input(
        "Новое решение (approved/rejected/pending): "
    ).strip()
    decision = decision_raw or None
    comment = input("Новый комментарий: ").strip() or None
    cancel_raw = input("Отменить? (y/n): ").strip().lower()
    is_cancelled = (
        True if cancel_raw == "y"
        else False if cancel_raw == "n"
        else None
    )
    if update_approval(
        approvals, approval_id, decision=decision,
        comment=comment, is_cancelled=is_cancelled,
    ):
        print("Согласование обновлено.")
    else:
        print("Ошибка: согласование не найдено.")


def delete_approval_menu(approvals: List[Approval]) -> None:
    """Удалить согласование."""
    approval_id = input_int("Введите ID согласования: ")
    if delete_approval(approvals, approval_id):
        print(f"Согласование #{approval_id} удалено.")
    else:
        print("Согласование не найдено.")


if __name__ == "__main__":
    main()
