"""Модуль работы с документами (ПР2 — функциональная модель).

На этапе ПР2 данные документа хранятся в словарях, а работа с коллекцией
выполняется отдельными функциями. В ПР3 сущность Document станет классом,
а функции работы с коллекцией сохранятся.
"""

from datetime import date
from typing import Dict, List


def add_document(
    documents: Dict[int, dict],
    title: str,
    doc_type: str,
    author_id: int,
    deadline: date,
) -> dict:
    """Добавить документ в словарь documents.

    Args:
        documents: словарь документов (id → данные);
        title: название документа;
        doc_type: тип документа;
        author_id: идентификатор автора;
        deadline: срок согласования.

    Returns:
        Созданный словарь документа.
    """
    next_id = _next_id(list(documents.keys()))
    document = {
        "id": next_id,
        "title": title,
        "doc_type": doc_type,
        "author_id": author_id,
        "deadline": deadline.isoformat(),
    }
    documents[next_id] = document
    return document


def find_document(documents: Dict[int, dict], query: str) -> List[dict]:
    """Найти документы по подстроке названия."""
    query_lower = query.lower()
    return [
        document
        for document in documents.values()
        if query_lower in document["title"].lower()
    ]


def find_document_by_id(
    documents: Dict[int, dict],
    doc_id: int,
) -> dict:
    """Найти документ по идентификатору."""
    return documents.get(doc_id)


def sort_documents_by_deadline(
    documents: Dict[int, dict],
) -> List[dict]:
    """Отсортировать документы по сроку согласования.

    Используется lambda-функция в качестве ключа сортировки.
    """
    return sorted(
        documents.values(),
        key=lambda document: document["deadline"],
    )


def show_documents(
    documents: Dict[int, dict],
    approvals: List[dict],
) -> None:
    """Вывести список документов с их статусами."""
    if not documents:
        print("Список документов пуст.")
        return
    print("\n--- Документы ---")
    for document in documents.values():
        status_label = get_document_status_label(
            approvals,
            document["id"],
        )
        print(
            f"#{document['id']}: {document['title']} "
            f"({document['doc_type']}) | Статус: {status_label}"
        )


def get_document_status_label(
    approvals: List[dict],
    document_id: int,
) -> str:
    """Вернуть текстовое представление статуса документа."""
    status = get_document_status(approvals, document_id)
    if status == "approved":
        return "Согласован"
    if status == "rejected":
        return "Отклонён"
    return "На согласовании"


def get_document_status(
    approvals: List[dict],
    document_id: int,
) -> str:
    """Определить статус документа по его согласованиям."""
    for approval in approvals:
        if approval["document_id"] != document_id:
            continue
        if approval.get("is_cancelled"):
            continue
        if approval["decision"] == "approved":
            return "approved"
        if approval["decision"] == "rejected":
            return "rejected"
    return "pending"


def is_overdue(document: dict, current_date: date) -> bool:
    """Проверить, истёк ли срок согласования документа."""
    deadline = date.fromisoformat(document["deadline"])
    return current_date > deadline


def _next_id(existing_ids: List[int]) -> int:
    """Вычислить следующий идентификатор."""
    if not existing_ids:
        return 1
    return max(existing_ids) + 1
