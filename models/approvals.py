"""Модуль класса Approval и функций работы с согласованиями.

Согласование — действие согласующего по отношению к документу. У каждого
согласования есть идентификатор, документ, согласующий, решение
(approved/rejected), комментарий и признак отмены.

Класс Approval хранит данные одного согласования и умеет отменять себя
через метод cancel(). Функции модуля работают с коллекцией согласований:
проверка возможности согласования, создание, отмена и вывод списка.
"""

from datetime import date
from typing import List, Optional

from .documents import Document
from .users import User


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
        """Создать объект согласования.

        Args:
            approval_id: идентификатор согласования;
            document_id: идентификатор документа;
            user_id: идентификатор согласующего;
            decision: код решения;
            comment: текст комментария;
            approval_date: дата согласования;
            is_cancelled: признак отмены.
        """
        self.id = approval_id
        self.document_id = document_id
        self.user_id = user_id
        self.decision = decision
        self.comment = comment
        self.approval_date = approval_date
        self.is_cancelled = is_cancelled

    def cancel(self) -> None:
        """Отменить согласование.

        Отмена не удаляет объект из коллекции: меняется только признак
        is_cancelled. Это позволяет сохранить историю согласований и
        разблокировать документ для нового решения.
        """
        self.is_cancelled = True

    def __str__(self) -> str:
        """Вернуть строковое представление согласования."""
        labels = {
            "approved": "Согласован",
            "rejected": "Отклонён",
            "pending": "На согласовании",
        }
        decision_label = labels.get(self.decision, self.decision)
        if self.is_cancelled:
            decision_label = f"{decision_label} (отменено)"
        date_str = (
            self.approval_date.strftime("%d.%m.%Y")
            if self.approval_date
            else "—"
        )
        return (
            f"Согласование #{self.id} | Документ #{self.document_id} | "
            f"Согласующий #{self.user_id} | {decision_label} | {date_str}"
        )

    @classmethod
    def from_data(cls, data: dict) -> "Approval":
        """Создать согласование из словаря данных JSON.

        Args:
            data: словарь с полями согласования.

        Returns:
            Объект Approval.
        """
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
        """Преобразовать согласование в словарь для JSON.

        Returns:
            Словарь с полями согласования.
        """
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


def can_approve_document(
    approvals: List[Approval],
    document: Document,
    user: User,
    current_date: date,
) -> tuple[bool, str]:
    """Проверить возможность согласования документа пользователем.

    Правила проверки:
        * автор документа не может согласовать собственный документ;
        * срок согласования не должен быть истёк;
        * документ не должен иметь уже активного согласования.

    Args:
        approvals: коллекция согласований;
        document: объект документа;
        user: объект согласующего;
        current_date: текущая дата.

    Returns:
        Кортеж (можно ли согласовать, пояснение).
    """
    if document.author_id == user.id:
        return (
            False,
            "Ошибка: автор не может согласовать "
            "собственный документ.",
        )
    if document.is_overdue(current_date):
        return False, "Срок согласования истёк."
    if not is_document_open_for_approval(approvals, document.id):
        return False, "Документ уже имеет активное согласование."
    return True, "Согласующий может принять решение."


def is_document_open_for_approval(
    approvals: List[Approval],
    document_id: int,
) -> bool:
    """Проверить, доступен ли документ для нового согласования.

    Документ недоступен, если уже имеет активное согласование.

    Args:
        approvals: коллекция согласований;
        document_id: идентификатор документа.

    Returns:
        True, если документ можно согласовать.
    """
    for approval in approvals:
        if approval.document_id != document_id:
            continue
        if approval.is_cancelled:
            continue
        return False
    return True


def create_approval(
    approvals: List[Approval],
    document: Document,
    user: User,
    decision: str,
    comment: str,
    current_date: date,
) -> Optional[Approval]:
    """Создать согласование документа.

    Перед созданием выполняется проверка возможности согласования.
    При нарушении правил согласование не создаётся.

    Args:
        approvals: коллекция согласований;
        document: объект документа;
        user: объект согласующего;
        decision: код решения;
        comment: комментарий согласующего;
        current_date: текущая дата.

    Returns:
        Созданный объект Approval или None.
    """
    allowed, _ = can_approve_document(
        approvals, document, user, current_date
    )
    if not allowed:
        return None
    next_id = _next_approval_id(approvals)
    approval = Approval(
        approval_id=next_id,
        document_id=document.id,
        user_id=user.id,
        decision=decision,
        comment=comment,
        approval_date=current_date,
    )
    approvals.append(approval)
    return approval


def cancel_approval(
    approvals: List[Approval],
    approval_id: int,
) -> bool:
    """Отменить согласование по идентификатору.

    Отмена не удаляет объект из коллекции: вызывается метод cancel().

    Args:
        approvals: коллекция согласований;
        approval_id: идентификатор согласования.

    Returns:
        True, если согласование найдено и отменено.
    """
    for approval in approvals:
        if approval.id == approval_id:
            approval.cancel()
            return True
    return False


def find_approval_by_id(
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


def get_approval_status(
    approvals: List[Approval],
    document: Document,
) -> str:
    """Вернуть текстовый статус документа по его согласованиям.

    Функция перенесена из ПР1 и адаптирована под объектную модель:
    использует метод документа get_status_label().

    Args:
        approvals: коллекция согласований;
        document: объект документа.

    Returns:
        Строка со статусом документа.
    """
    return document.get_status_label(approvals)


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
        document = find_document_in_list(documents, approval.document_id)
        user = find_user_in_list(users, approval.user_id)
        doc_title = document.title if document else "—"
        user_name = user.name if user else "—"
        print(
            f"#{approval.id} | {doc_title} | "
            f"Согласующий: {user_name} | "
            f"Решение: {approval.decision} | "
            f"Отменено: {'да' if approval.is_cancelled else 'нет'}"
        )


def find_document_in_list(
    documents: List[Document],
    doc_id: int,
) -> Optional[Document]:
    """Найти документ в коллекции по идентификатору.

    Args:
        documents: коллекция документов;
        doc_id: идентификатор документа.

    Returns:
        Найденный документ или None.
    """
    for document in documents:
        if document.id == doc_id:
            return document
    return None


def find_user_in_list(
    users: List[User],
    user_id: int,
) -> Optional[User]:
    """Найти пользователя в коллекции по идентификатору.

    Args:
        users: коллекция пользователей;
        user_id: идентификатор пользователя.

    Returns:
        Найденный пользователь или None.
    """
    for user in users:
        if user.id == user_id:
            return user
    return None


def _next_approval_id(approvals: List[Approval]) -> int:
    """Вычислить следующий идентификатор согласования.

    Args:
        approvals: коллекция согласований.

    Returns:
        Значение на единицу больше максимального существующего id.
    """
    if not approvals:
        return 1
    return max(approval.id for approval in approvals) + 1
