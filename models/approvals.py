"""Модуль класса Approval и CRUD-функций работы с согласованиями.

Согласование — действие согласующего по отношению к документу. У каждого
согласования есть документ, согласующий, решение, комментарий и дата.

Для коллекции согласований реализован базовый набор операций: создание,
поиск по идентификатору, обновление, удаление и вывод списка. При создании
выполняется проверка правил предметной области: автор не может
согласовать собственный документ, и на один документ не может быть двух
активных согласований.
"""

from datetime import date
from typing import List, Optional

from .documents import Document, find_document
from .users import User, find_user


class Approval:
    """Согласование документа пользователем.

    Атрибуты:
        id (int): идентификатор согласования;
        document_id (int): идентификатор документа;
        user_id (int): идентификатор согласующего;
        decision (str): решение — «approved», «rejected» или «pending»;
        comment (str): комментарий согласующего;
        approval_date (date): дата согласования;
        is_cancelled (bool): признак отмены согласования.
    """

    def __init__(
        self,
        approval_id: int,
        document_id: int,
        user_id: int,
        decision: str = "pending",
        comment: str = "",
        approval_date: Optional[date] = None,
        is_cancelled: bool = False,
    ) -> None:
        """Создать объект согласования."""
        self.id = approval_id
        self.document_id = document_id
        self.user_id = user_id
        self.decision = decision
        self.comment = comment
        self.approval_date = approval_date
        self.is_cancelled = is_cancelled

    def __str__(self) -> str:
        """Вернуть строковое представление согласования."""
        date_str = (
            self.approval_date.strftime("%d.%m.%Y")
            if self.approval_date
            else "—"
        )
        state = "отменено" if self.is_cancelled else "активно"
        return (
            f"Согласование #{self.id} | Документ #{self.document_id} | "
            f"Согласующий #{self.user_id} | "
            f"Решение: {self.decision} | {date_str} | {state}"
        )

    @classmethod
    def from_data(cls, data: dict) -> "Approval":
        """Создать согласование из словаря данных JSON."""
        raw_date = data.get("approval_date")
        if isinstance(raw_date, date):
            approval_date_value = raw_date
        elif raw_date:
            approval_date_value = date.fromisoformat(raw_date)
        else:
            approval_date_value = None
        return cls(
            approval_id=data["id"],
            document_id=data["document_id"],
            user_id=data["user_id"],
            decision=data.get("decision", "pending"),
            comment=data.get("comment", ""),
            approval_date=approval_date_value,
            is_cancelled=data.get("is_cancelled", False),
        )

    def to_dict(self) -> dict:
        """Преобразовать согласование в словарь для JSON."""
        return {
            "id": self.id,
            "document_id": self.document_id,
            "user_id": self.user_id,
            "decision": self.decision,
            "comment": self.comment,
            "approval_date": (
                self.approval_date.isoformat()
                if self.approval_date
                else None
            ),
            "is_cancelled": self.is_cancelled,
        }


def add_approval(
    approvals: List[Approval],
    documents: List[Document],
    document_id: int,
    user_id: int,
    decision: str,
    comment: str,
    current_date: date,
) -> tuple[Optional[Approval], str]:
    """Создать согласование и добавить его в коллекцию.

    Перед созданием выполняется проверка правил:
        * автор документа не может согласовать собственный документ;
        * на один документ не может быть двух активных согласований.

    Args:
        approvals: коллекция согласований;
        documents: коллекция документов (для проверки автора);
        document_id: идентификатор документа;
        user_id: идентификатор согласующего;
        decision: код решения;
        comment: комментарий согласующего;
        current_date: текущая дата.

    Returns:
        Кортеж (созданное согласование или None, пояснение).
    """
    document = find_document(documents, document_id)
    if document is None:
        return None, "Ошибка: документ не найден."
    if document.author_id == user_id:
        return (
            None,
            "Ошибка: автор не может согласовать "
            "собственный документ.",
        )
    if _has_active_approval(approvals, document_id):
        return None, "Ошибка: у документа уже есть активное согласование."
    next_id = _next_id(approvals)
    approval = Approval(
        approval_id=next_id,
        document_id=document_id,
        user_id=user_id,
        decision=decision,
        comment=comment,
        approval_date=current_date,
    )
    approvals.append(approval)
    return approval, "Согласование создано."


def find_approval(
    approvals: List[Approval],
    approval_id: int,
) -> Optional[Approval]:
    """Найти согласование по идентификатору.

    Args:
        approvals: коллекция согласований;
        approval_id: идентификатор согласования.

    Returns:
        Найденное согласование или None.
    """
    for approval in approvals:
        if approval.id == approval_id:
            return approval
    return None


def update_approval(
    approvals: List[Approval],
    approval_id: int,
    decision: Optional[str] = None,
    comment: Optional[str] = None,
    is_cancelled: Optional[bool] = None,
) -> bool:
    """Обновить данные согласования.

    Обновляются только переданные поля. Идентификаторы документа и
    согласующего не меняются: они задаются при создании.

    Args:
        approvals: коллекция согласований;
        approval_id: идентификатор согласования;
        decision: новое решение (если передано);
        comment: новый комментарий (если передано);
        is_cancelled: новый признак отмены (если передано).

    Returns:
        True, если согласование найдено и обновлено.
    """
    approval = find_approval(approvals, approval_id)
    if approval is None:
        return False
    if decision is not None:
        approval.decision = decision
    if comment is not None:
        approval.comment = comment
    if is_cancelled is not None:
        approval.is_cancelled = is_cancelled
    return True


def delete_approval(
    approvals: List[Approval],
    approval_id: int,
) -> bool:
    """Удалить согласование из коллекции.

    Args:
        approvals: коллекция согласований;
        approval_id: идентификатор согласования.

    Returns:
        True, если согласование найдено и удалено.
    """
    approval = find_approval(approvals, approval_id)
    if approval is None:
        return False
    approvals.remove(approval)
    return True


def show_approvals(
    approvals: List[Approval],
    documents: List[Document],
    users: List[User],
) -> None:
    """Вывести список согласований.

    Args:
        approvals: коллекция согласований;
        documents: коллекция документов (для отображения названий);
        users: коллекция пользователей (для отображения ФИО).
    """
    if not approvals:
        print("Список согласований пуст.")
        return
    print("\n--- Согласования ---")
    for approval in approvals:
        document = find_document(documents, approval.document_id)
        user = find_user(users, approval.user_id)
        doc_title = document.title if document else "—"
        user_name = user.name if user else "—"
        state = "отменено" if approval.is_cancelled else "активно"
        print(
            f"#{approval.id} | {doc_title} | "
            f"Согласующий: {user_name} | "
            f"Решение: {approval.decision} | {state}"
        )


def _has_active_approval(
    approvals: List[Approval],
    document_id: int,
) -> bool:
    """Проверить, есть ли активное согласование у документа."""
    for approval in approvals:
        if approval.document_id != document_id:
            continue
        if not approval.is_cancelled:
            return True
    return False


def _next_id(approvals: List[Approval]) -> int:
    """Вычислить следующий идентификатор согласования."""
    if not approvals:
        return 1
    return max(approval.id for approval in approvals) + 1
