"""Автоматизированные тесты класса Approval и CRUD-функций.

Проверяются:
    * создание объекта Approval и значения его атрибутов;
    * строковое представление __str__;
    * метод класса from_data и to_dict (преобразование в/из JSON);
    * добавление согласования в коллекцию (Create) с проверкой правил;
    * поиск согласования по идентификатору (Read);
    * обновление данных согласования (Update);
    * удаление согласования из коллекции (Delete);
    * бизнес-правила: автор не может согласовать свой документ,
      на один документ — не более одного активного согласования.
"""

from datetime import date

from models import Approval, Document
from models.approvals import (
    add_approval,
    delete_approval,
    find_approval,
    update_approval,
)


def make_document(doc_id: int = 1, author_id: int = 1) -> Document:
    """Создать тестовый документ."""
    return Document(
        doc_id=doc_id,
        title="Договор поставки № 45",
        doc_type="Договор",
        author_id=author_id,
        deadline=date(2026, 12, 31),
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


def test_approval_from_data_and_to_dict():
    """Преобразование согласования в словарь и обратно."""
    approval = Approval(
        approval_id=1,
        document_id=1,
        user_id=2,
        decision="approved",
        comment="Ок",
        approval_date=date(2026, 10, 6),
    )
    data = approval.to_dict()
    assert data["id"] == 1
    assert data["document_id"] == 1
    assert data["user_id"] == 2
    assert data["approval_date"] == "2026-10-06"
    restored = Approval.from_data(data)
    assert restored.id == 1
    assert restored.decision == "approved"


def test_add_approval_success():
    """Создание согласования при выполнении всех правил."""
    document = make_document(author_id=1)
    documents = [document]
    approvals: list = []
    approval, message = add_approval(
        approvals,
        documents,
        document_id=1,
        user_id=2,
        decision="approved",
        comment="Ок",
        current_date=date(2026, 10, 6),
    )
    assert approval is not None
    assert approval.id == 1
    assert approval.decision == "approved"
    assert len(approvals) == 1


def test_add_approval_unknown_document():
    """Создание согласования для несуществующего документа."""
    documents: list = []
    approvals: list = []
    approval, message = add_approval(
        approvals,
        documents,
        document_id=999,
        user_id=2,
        decision="approved",
        comment="",
        current_date=date(2026, 10, 6),
    )
    assert approval is None
    assert "документ" in message.lower()


def test_add_approval_author_cannot_approve_own_document():
    """Автор не может согласовать собственный документ."""
    document = make_document(author_id=1)
    documents = [document]
    approvals: list = []
    approval, message = add_approval(
        approvals,
        documents,
        document_id=1,
        user_id=1,
        decision="approved",
        comment="",
        current_date=date(2026, 10, 6),
    )
    assert approval is None
    assert "автор" in message.lower()


def test_add_approval_duplicate_forbidden():
    """Нельзя создать два активных согласования одного документа."""
    document = make_document(author_id=1)
    documents = [document]
    approvals: list = []
    first, _ = add_approval(
        approvals,
        documents,
        document_id=1,
        user_id=2,
        decision="approved",
        comment="Ок",
        current_date=date(2026, 10, 6),
    )
    second, message = add_approval(
        approvals,
        documents,
        document_id=1,
        user_id=3,
        decision="rejected",
        comment="Не ок",
        current_date=date(2026, 10, 6),
    )
    assert first is not None
    assert second is None
    assert "уже" in message.lower()
    assert len(approvals) == 1


def test_find_approval():
    """Поиск согласования по идентификатору (Read)."""
    document = make_document(author_id=1)
    documents = [document]
    approvals: list = []
    approval, _ = add_approval(
        approvals,
        documents,
        document_id=1,
        user_id=2,
        decision="approved",
        comment="Ок",
        current_date=date(2026, 10, 6),
    )
    found = find_approval(approvals, approval.id)
    assert found is not None
    assert found.id == approval.id
    assert find_approval(approvals, 999) is None


def test_update_approval():
    """Обновление данных согласования (Update)."""
    document = make_document(author_id=1)
    documents = [document]
    approvals: list = []
    approval, _ = add_approval(
        approvals,
        documents,
        document_id=1,
        user_id=2,
        decision="approved",
        comment="Ок",
        current_date=date(2026, 10, 6),
    )
    result = update_approval(
        approvals,
        approval.id,
        decision="rejected",
        comment="Не подходит",
        is_cancelled=True,
    )
    assert result is True
    assert approval.decision == "rejected"
    assert approval.comment == "Не подходит"
    assert approval.is_cancelled is True


def test_update_unknown_approval():
    """Обновление несуществующего согласования возвращает False."""
    approvals: list = []
    result = update_approval(approvals, 999, decision="approved")
    assert result is False


def test_delete_approval():
    """Удаление согласования из коллекции (Delete)."""
    document = make_document(author_id=1)
    documents = [document]
    approvals: list = []
    approval, _ = add_approval(
        approvals,
        documents,
        document_id=1,
        user_id=2,
        decision="approved",
        comment="Ок",
        current_date=date(2026, 10, 6),
    )
    result = delete_approval(approvals, approval.id)
    assert result is True
    assert len(approvals) == 0
    assert find_approval(approvals, approval.id) is None


def test_delete_unknown_approval():
    """Удаление несуществующего согласования возвращает False."""
    approvals: list = []
    result = delete_approval(approvals, 999)
    assert result is False
