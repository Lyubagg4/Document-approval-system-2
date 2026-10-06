"""Автоматизированные тесты класса Approval и функций согласований.

Проверяются:
    * создание объекта Approval и атрибуты;
    * метод cancel() и флаг is_cancelled;
    * строковое представление __str__;
    * правило «автор не может согласовать собственный документ»;
    * правило «нельзя создать два активных согласования одного документа»;
    * отмена согласования разблокирует документ;
    * правило «срок согласования не должен быть истёк»;
    * отмена согласования по идентификатору.
"""

from datetime import date

from models import Approval, Document, User
from models.approvals import (
    can_approve_document,
    cancel_approval,
    create_approval,
    find_approval_by_id,
    is_document_open_for_approval,
)


def make_document(author_id: int = 1) -> Document:
    """Создать тестовый документ.

    Args:
        author_id: идентификатор автора.

    Returns:
        Объект Document.
    """
    return Document(
        doc_id=1,
        title="Договор поставки № 45",
        doc_type="Договор",
        author_id=author_id,
        deadline=date(2026, 12, 31),
    )


def make_user(user_id: int = 2) -> User:
    """Создать тестового пользователя.

    Args:
        user_id: идентификатор пользователя.

    Returns:
        Объект User.
    """
    return User(
        user_id=user_id,
        name="Петров Пётр",
        department="Отдел закупок",
        role="Руководитель",
        email="petrov@example.com",
    )


def test_approval_creation():
    """Создание объекта Approval и проверка атрибутов."""
    approval = Approval(
        approval_id=1,
        document_id=1,
        user_id=2,
        decision="approved",
        comment="Ок",
        approval_date=date(2026, 10, 6),
    )
    assert approval.id == 1
    assert approval.document_id == 1
    assert approval.user_id == 2
    assert approval.decision == "approved"
    assert approval.comment == "Ок"
    assert approval.approval_date == date(2026, 10, 6)
    assert approval.is_cancelled is False


def test_approval_cancel():
    """Метод cancel() меняет состояние согласования."""
    approval = Approval(
        approval_id=1,
        document_id=1,
        user_id=2,
        decision="approved",
        comment="Ок",
        approval_date=date(2026, 10, 6),
    )
    assert approval.is_cancelled is False
    approval.cancel()
    assert approval.is_cancelled is True


def test_approval_str():
    """Строковое представление согласования."""
    approval = Approval(
        approval_id=1,
        document_id=1,
        user_id=2,
        decision="approved",
        comment="Ок",
        approval_date=date(2026, 10, 6),
    )
    text = str(approval)
    assert "Согласование #1" in text
    assert "06.10.2026" in text


def test_approval_str_cancelled():
    """Строковое представление отменённого согласования."""
    approval = Approval(
        approval_id=1,
        document_id=1,
        user_id=2,
        decision="approved",
        comment="Ок",
        approval_date=date(2026, 10, 6),
        is_cancelled=True,
    )
    text = str(approval)
    assert "отменено" in text


def test_author_cannot_approve_own_document():
    """Автор не может согласовать собственный документ."""
    document = make_document(author_id=1)
    user = User(
        user_id=1,
        name="Иванов Иван",
        department="Юридический отдел",
        role="Юрист",
        email="ivanov@example.com",
    )
    approvals: list = []
    allowed, message = can_approve_document(
        approvals, document, user, date(2026, 10, 6)
    )
    assert allowed is False
    assert "автор" in message.lower()


def test_overdue_document_cannot_be_approved():
    """Документ с истёкшим сроком нельзя согласовать."""
    document = Document(
        doc_id=1,
        title="Договор",
        doc_type="Договор",
        author_id=1,
        deadline=date(2026, 9, 1),
    )
    user = make_user(user_id=2)
    approvals: list = []
    allowed, message = can_approve_document(
        approvals, document, user, date(2026, 10, 6)
    )
    assert allowed is False
    assert "срок" in message.lower()


def test_create_approval_success():
    """Создание согласования при выполнении всех правил."""
    document = make_document(author_id=1)
    user = make_user(user_id=2)
    approvals: list = []
    approval = create_approval(
        approvals,
        document,
        user,
        "approved",
        "Ок",
        date(2026, 10, 6),
    )
    assert approval is not None
    assert approval.id == 1
    assert approval.decision == "approved"
    assert len(approvals) == 1


def test_duplicate_approval_forbidden():
    """Нельзя создать два активных согласования одного документа."""
    document = make_document(author_id=1)
    user = make_user(user_id=2)
    approvals: list = []
    first = create_approval(
        approvals,
        document,
        user,
        "approved",
        "Ок",
        date(2026, 10, 6),
    )
    assert first is not None
    second = create_approval(
        approvals,
        document,
        user,
        "rejected",
        "Не ок",
        date(2026, 10, 6),
    )
    assert second is None
    assert len(approvals) == 1


def test_cancelled_approval_unblocks_document():
    """Отмена согласования разблокирует документ."""
    document = make_document(author_id=1)
    user = make_user(user_id=2)
    approvals: list = []
    first = create_approval(
        approvals,
        document,
        user,
        "approved",
        "Ок",
        date(2026, 10, 6),
    )
    assert first is not None
    assert not is_document_open_for_approval(approvals, document.id)
    first.cancel()
    assert is_document_open_for_approval(approvals, document.id)
    second = create_approval(
        approvals,
        document,
        user,
        "rejected",
        "Не ок",
        date(2026, 10, 6),
    )
    assert second is not None
    assert len(approvals) == 2


def test_cancel_approval_by_id():
    """Отмена согласования по идентификатору."""
    document = make_document(author_id=1)
    user = make_user(user_id=2)
    approvals: list = []
    approval = create_approval(
        approvals,
        document,
        user,
        "approved",
        "Ок",
        date(2026, 10, 6),
    )
    assert approval is not None
    result = cancel_approval(approvals, approval.id)
    assert result is True
    assert approval.is_cancelled is True


def test_cancel_unknown_approval():
    """Отмена несуществующего согласования возвращает False."""
    approvals: list = []
    result = cancel_approval(approvals, 999)
    assert result is False


def test_find_approval_by_id():
    """Поиск согласования по идентификатору."""
    document = make_document(author_id=1)
    user = make_user(user_id=2)
    approvals: list = []
    approval = create_approval(
        approvals,
        document,
        user,
        "approved",
        "Ок",
        date(2026, 10, 6),
    )
    assert approval is not None
    found = find_approval_by_id(approvals, approval.id)
    assert found is not None
    assert found.id == approval.id
    assert find_approval_by_id(approvals, 999) is None
