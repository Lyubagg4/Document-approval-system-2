"""Система согласования документов.

Начальная версия приложения из ПР1. Реализован один законченный
сценарий предметной области: проверка возможности согласования
документа и вынесение решения. Используются только базовые конструкции
Python: простые типы данных, операции, преобразование типов, ветвления,
функции и импорт модулей.

В ПР2 этот сценарий будет переработан: данные документа перейдут в
коллекции, функции — в модули, добавится хранение в JSON. В ПР3 —
преобразуется в объектную модель на классах Document, User и Approval.
"""

from datetime import date


def get_status_label(status):
    """Возвращает название статуса документа."""
    if status == "approved":
        return "Согласован"
    elif status == "rejected":
        return "Отклонён"
    return "На согласовании"


def check_document_data(title, author, approver):
    """Проверяет, заполнены ли основные данные документа."""
    if title == "":
        return "Ошибка: не указано название документа."
    elif author == "":
        return "Ошибка: не указан автор документа."
    elif approver == "":
        return "Ошибка: не указан согласующий."
    return "Данные документа заполнены."


def check_deadline(current_date, deadline):
    """Проверяет, не истёк ли срок согласования."""
    if current_date > deadline:
        return "Срок согласования истёк."
    return "Срок согласования не истёк."


def can_approve_document(author, approver):
    """Проверяет, может ли пользователь согласовать документ."""
    if author == approver:
        return "Ошибка: автор не может согласовать собственный документ."
    return "Согласующий может принять решение."


def make_decision(decision_code, comment):
    """Формирует результат согласования документа."""
    if decision_code == 1:
        return "Документ согласован."
    elif decision_code == 2:
        return "Документ отклонён. Комментарий: " + comment
    return "Ошибка: необходимо выбрать 1 или 2."


print("=== Система согласования документов ===")

doc_title = "Договор поставки оборудования № 45"
doc_type = "Договор"

author_name = "Иванов Иван"
author_department = "Юридический отдел"

approver_name = "Петров Пётр"
approver_role = "Руководитель отдела закупок"

comment_text = "Документ соответствует требованиям."

deadline = date(2026, 10, 15)

print("\n--- Проверка документа ---")

data_result = check_document_data(
    doc_title,
    author_name,
    approver_name
)
print(data_result)

deadline_result = check_deadline(date.today(), deadline)
print(deadline_result)

approval_result = can_approve_document(
    author_name,
    approver_name
)
print(approval_result)

if (
    data_result == "Данные документа заполнены."
    and deadline_result == "Срок согласования не истёк."
    and approval_result == "Согласующий может принять решение."
):
    print("\n--- Согласование документа ---")
    print("1 — Согласовать")
    print("2 — Отклонить")

    decision = int(input("Введите номер решения: "))

    result = make_decision(decision, comment_text)

    print("\n--- Результат ---")
    print(f"Документ: {doc_title}")
    print(f"Тип: {doc_type}")
    print(f"Автор: {author_name}")
    print(f"Согласующий: {approver_name}")
    print(
        "Статус: "
        + get_status_label(
            "approved" if decision == 1 else "rejected"
        )
    )
    print(f"Решение: {result}")

else:
    print("\nДокумент не может быть отправлен на согласование.")
