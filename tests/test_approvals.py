"""Автоматизированные тесты pytest для ПР2 — функциональная модель."""

from datetime import date

from documents import add_document, find_document, get_document_status_label
from users import add_user, find_user
from approvals import can_approve_document, create_approval, cancel_approval


def test_add_document():
    """Добавление документа в словарь."""
    documents: dict = {}
    document = add_document(
        documents,
        title="Договор",
        doc_type="Договор",
        author_id=1,
        deadline=date(2026, 10, 15),
    )
    assert len(documents) == 1
    assert documents[1] is document
    assert document["id"] == 1


def test_find_document():
    """Поиск документа по подстроке названия."""
    documents: dict = {}
    add_document(
        documents,
        title="Договор поставки",
        doc_type="Договор",
        author_id=1,
        deadline=date(2026, 10, 15),
    )
    found = find_document(documents, "договор")
    assert len(found) == 1
    assert found[0]["title"] == "Договор поставки"


def test_document_status_label():
    """Текстовое представление статуса документа."""
    approvals = [
        {
            "id": 1,
            "document_id": 1,
            "user_id": 2,
            "decision": "approved",
            "comment": "",
            "approval_date": "2026-10-06",
            "is_cancelled": False,
        }
    ]
    label = get_document_status_label(approvals, 1)
    assert label == "Согласован"


def test_add_user():
    """Добавление пользователя."""
    users: dict = {}
    user = add_user(
        users,
        name="Иванов Иван",
        department="Юридический отдел",
        role="Юрист",
        email="ivanov@example.com",
    )
    assert len(users) == 1
    assert user["id"] == 1


def test_find_user():
    """Поиск пользователя по подстроке."""
    users: dict = {}
    add_user(
        users,
        name="Иванов Иван",
        department="Юридический отдел",
        role="Юрист",
        email="ivanov@example.com",
    )
    found = find_user(users, "иванов")
    assert len(found) == 1


def test_author_cannot_approve_own_document():
    """Автор не может согласовать свой документ."""
    documents: dict = {}
    document = add_document(
        documents,
        title="Договор",
        doc_type="Договор",
        author_id=1,
        deadline=date(2026, 10, 15),
    )
    users: dict = {}
    user = add_user(
        users,
        name="Иванов Иван",
        department="Юридический отдел",
        role="Юрист",
        email="ivanov@example.com",
    )
    approvals: list = []
    allowed, _ = can_approve_document(
        approvals, document, user, date(2026, 10, 6)
    )
    assert allowed is False


def test_create_and_cancel_approval():
    """Создание согласования и его отмена."""
    documents: dict = {}
    document = add_document(
        documents,
        title="Договор",
        doc_type="Договор",
        author_id=1,
        deadline=date(2026, 10, 15),
    )
    users: dict = {}
    add_user(
        users,
        name="Иванов Иван",
        department="Юридический отдел",
        role="Юрист",
        email="ivanov@example.com",
    )
    user2 = add_user(
        users,
        name="Петров Пётр",
        department="Отдел закупок",
        role="Руководитель",
        email="petrov@example.com",
    )
    approvals: list = []
    approval = create_approval(
        approvals,
        document,
        user2,
        "approved",
        "Ок",
        date(2026, 10, 6),
    )
    assert approval is not None
    assert approval["id"] == 1
    result = cancel_approval(approvals, 1)
    assert result is True
    assert approval["is_cancelled"] is True
