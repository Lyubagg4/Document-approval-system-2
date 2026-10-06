"""Точка запуска приложения (ПР2 — функциональная модель).

Меню приложения и вызов функций работы с документами, пользователями и
согласованиями. Данные хранятся в словарях и списках, сохраняются в JSON.
"""

import os
from datetime import date

from approvals import (
    can_approve_document,
    cancel_approval,
    create_approval,
    get_approval_status,
    show_approvals,
)
from documents import (
    add_document,
    find_document,
    find_document_by_id,
    show_documents,
    sort_documents_by_deadline,
)
from storage import (
    load_approvals,
    load_documents,
    load_users,
    save_approvals,
    save_documents,
    save_users,
)
from users import (
    add_user,
    find_user,
    find_user_by_id,
    show_users,
)
from utils import input_date, input_int, input_str

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
DOCUMENTS_FILE = os.path.join(DATA_DIR, "documents.json")
USERS_FILE = os.path.join(DATA_DIR, "users.json")
APPROVALS_FILE = os.path.join(DATA_DIR, "approvals.json")


def main() -> None:
    """Точка запуска приложения."""
    print("=== Система согласования документов ===")

    documents = load_documents(DOCUMENTS_FILE)
    users = load_users(USERS_FILE)
    approvals = load_approvals(APPROVALS_FILE)

    while True:
        print("\n--- Главное меню ---")
        print("1. Показать документы")
        print("2. Найти документ по названию")
        print("3. Отсортировать документы по сроку")
        print("4. Показать пользователей")
        print("5. Найти пользователя")
        print("6. Добавить документ")
        print("7. Добавить пользователя")
        print("8. Проверить возможность согласования")
        print("9. Создать согласование")
        print("10. Отменить согласование")
        print("11. Показать согласования")
        print("12. Показать статус документа")
        print("0. Выход")

        choice = input_int("Выберите действие: ")
        if choice == 0:
            break
        if choice == 1:
            show_documents(documents, approvals)
        elif choice == 2:
            query = input_str("Введите подстроку: ")
            found = find_document(documents, query)
            found_dict = {d["id"]: d for d in found}
            show_documents(found_dict, approvals)
        elif choice == 3:
            sorted_docs = sort_documents_by_deadline(documents)
            found_dict = {d["id"]: d for d in sorted_docs}
            show_documents(found_dict, approvals)
        elif choice == 4:
            show_users(users)
        elif choice == 5:
            query = input_str("Введите подстроку: ")
            found = find_user(users, query)
            found_dict = {u["id"]: u for u in found}
            show_users(found_dict)
        elif choice == 6:
            show_users(users)
            author_id = input_int("ID автора: ")
            author = find_user_by_id(users, author_id)
            if not author:
                print("Ошибка: пользователь не найден.")
                continue
            title = input_str("Название документа: ")
            doc_type = input_str("Тип документа: ")
            deadline = input_date("Срок (ДД.ММ.ГГГГ): ")
            add_document(documents, title, doc_type, author_id, deadline)
            print("Документ добавлен.")
        elif choice == 7:
            name = input_str("ФИО: ")
            department = input_str("Подразделение: ")
            role = input_str("Должность: ")
            email = input_str("Email: ")
            add_user(users, name, department, role, email)
            print("Пользователь добавлен.")
        elif choice == 8:
            show_documents(documents, approvals)
            doc_id = input_int("ID документа: ")
            document = find_document_by_id(documents, doc_id)
            if not document:
                print("Ошибка: документ не найден.")
                continue
            show_users(users)
            user_id = input_int("ID согласующего: ")
            user = find_user_by_id(users, user_id)
            if not user:
                print("Ошибка: пользователь не найден.")
                continue
            allowed, message = can_approve_document(
                approvals, document, user, date.today()
            )
            print(message)
        elif choice == 9:
            show_documents(documents, approvals)
            doc_id = input_int("ID документа: ")
            document = find_document_by_id(documents, doc_id)
            if not document:
                print("Ошибка: документ не найден.")
                continue
            show_users(users)
            user_id = input_int("ID согласующего: ")
            user = find_user_by_id(users, user_id)
            if not user:
                print("Ошибка: пользователь не найден.")
                continue
            print("1 — Согласовать, 2 — Отклонить")
            code = input_int("Решение: ")
            decision = "approved" if code == 1 else "rejected"
            comment = input_str("Комментарий: ")
            approval = create_approval(
                approvals, document, user, decision,
                comment, date.today()
            )
            if approval:
                print(f"Согласование #{approval['id']} создано.")
            else:
                print("Согласование не создано: нарушены правила.")
        elif choice == 10:
            show_approvals(approvals, documents, users)
            approval_id = input_int("ID согласования: ")
            if cancel_approval(approvals, approval_id):
                print(f"Согласование #{approval_id} отменено.")
            else:
                print("Ошибка: согласование не найдено.")
        elif choice == 11:
            show_approvals(approvals, documents, users)
        elif choice == 12:
            show_documents(documents, approvals)
            doc_id = input_int("ID документа: ")
            document = find_document_by_id(documents, doc_id)
            if not document:
                print("Ошибка: документ не найден.")
                continue
            status = get_approval_status(approvals, document)
            print(f"Статус документа: {status}")
        else:
            print("Ошибка: неверный номер действия.")

    save_documents(DOCUMENTS_FILE, documents)
    save_users(USERS_FILE, users)
    save_approvals(APPROVALS_FILE, approvals)
    print("\nДанные сохранены. До свидания!")


if __name__ == "__main__":
    main()
