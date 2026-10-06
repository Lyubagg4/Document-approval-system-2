"""Модуль работы с согласованиями (ПР2 — функциональная модель).

Функция get_booking_status() перенесена из ПР1 и адаптирована под
функциональную модель. В ПР3 она останется в составе модуля, но будет
работать с объектами Document и Approval.
"""

from datetime import date
from typing import Dict, List, Optional, Tuple


def can_approve_document(
    approvals: List[dict],
    document: dict,
    user: dict,
    current_date: date,
) -> Tuple[bool, str]:
    """Проверить возможность согласования документа пользователем."""
    if document["author_id"] == user["id"]:
        return False, (
            "Ошибка: автор не может согласовать "
            "собственный документ."
        )
    if _is_overdue(document, current_date):
        return False, "Срок согласования истёк."
    if not _is_open_for_approval(approvals, document["id"]):
        return False, "Документ уже имеет активное согласование."
    return True, "Согласующий может принять решение."


def _is_overdue(document: dict, current_date: date) -> bool:
    """Проверить истечение срока согласования."""
    deadline = date.fromisoformat(document["deadline"])
    return current_date > deadline


def _is_open_for_approval(
    approvals: List[dict],
    document_id: int,
) -> bool:
    """Проверить, доступен ли документ для согласования."""
    for approval in approvals:
        if approval["document_id"] != document_id:
            continue
        if approval.get("is_cancelled"):
            continue
        return False
    return True


def create_approval(
    approvals: List[dict],
    document: dict,
    user: dict,
    decision: str,
    comment: str,
    current_date: date,
) -> Optional[dict]:
    """Создать согласование документа."""
    allowed, _ = can_approve_document(
        approvals, document, user, current_date
    )
    if not allowed:
        return None
    next_id = _next_id([approval["id"] for approval in approvals])
    approval = {
        "id": next_id,
        "document_id": document["id"],
        "user_id": user["id"],
        "decision": decision,
        "comment": comment,
        "approval_date": current_date.isoformat(),
        "is_cancelled": False,
    }
    approvals.append(approval)
    return approval


def cancel_approval(
    approvals: List[dict],
    approval_id: int,
) -> bool:
    """Отменить согласование по идентификатору."""
    for approval in approvals:
        if approval["id"] == approval_id:
            approval["is_cancelled"] = True
            return True
    return False


def find_approval_by_id(
    approvals: List[dict],
    approval_id: int,
) -> Optional[dict]:
    """Найти согласование по идентификатору."""
    for approval in approvals:
        if approval["id"] == approval_id:
            return approval
    return None


def get_approval_status(
    approvals: List[dict],
    document: dict,
) -> str:
    """Вернуть текстовый статус документа по его согласованиям."""
    from documents import get_document_status_label
    return get_document_status_label(approvals, document["id"])


def show_approvals(
    approvals: List[dict],
    documents: Dict[int, dict],
    users: Dict[int, dict],
) -> None:
    """Вывести список согласований."""
    if not approvals:
        print("Список согласований пуст.")
        return
    print("\n--- Согласования ---")
    for approval in approvals:
        document = documents.get(approval["document_id"])
        user = users.get(approval["user_id"])
        doc_title = document["title"] if document else "—"
        user_name = user["name"] if user else "—"
        print(
            f"#{approval['id']} | {doc_title} | "
            f"Согласующий: {user_name} | "
            f"Решение: {approval['decision']} | "
            f"Отменено: {'да' if approval.get('is_cancelled') else 'нет'}"
        )


def _next_id(existing_ids: List[int]) -> int:
    """Вычислить следующий идентификатор."""
    if not existing_ids:
        return 1
    return max(existing_ids) + 1
