"""Автоматизированные тесты функций и класса Document.

Проверяются:
    * создание объекта Document и значения его атрибутов;
    * метод is_suitable_for() через проверку срока;
    * статусы документа (approved, rejected, pending);
    * строковое представление __str__;
    * добавление документа в коллекцию;
    * поиск документа по подстроке;
    * сортировка документов по сроку;
    * статический метод validate_title;
    * метод класса from_data и to_dict.
"""

from datetime import date

from models import Approval, Document
from models.documents import (
    add_document,
    find_document,
    find_document_by_id,
    sort_documents_by_deadline,
)


def test_document_creation():
    """Создание объекта Document и проверка атрибутов."""
    document = Document(
        doc_id=1,
        title="Договор поставки № 45",
        doc_type="Договор",
        author_id=2,
        deadline=date(2026, 10, 15),
    )
    assert document.id == 1
    assert document.title == "Договор поставки № 45"
    assert document.doc_type == "Договор"
    assert document.author_id == 2
    assert document.deadline == date(2026, 10, 15)


def test_document_is_overdue():
    """Проверка истечения срока согласования."""
    document = Document(
        doc_id=1,
        title="Договор",
        doc_type="Договор",
        author_id=2,
        deadline=date(2026, 9, 1),
    )
    assert document.is_overdue(date(2026, 9, 2))
    assert not document.is_overdue(date(2026, 9, 1))


def test_document_status_pending():
    """Статус документа без согласований — pending."""
    document = Document(
        doc_id=1,
        title="Договор",
        doc_type="Договор",
        author_id=2,
        deadline=date(2026, 10, 15),
    )
    assert document.get_status([]) == "pending"
    assert document.get_status_label([]) == "На согласовании"


def test_document_status_approved():
    """Статус документа с согласованием approved — approved."""
    document = Document(
        doc_id=1,
        title="Договор",
        doc_type="Договор",
        author_id=2,
        deadline=date(2026, 10, 15),
    )
    approval = Approval(
        approval_id=1,
        document_id=1,
        user_id=3,
        decision="approved",
        comment="Ок",
        approval_date=date(2026, 10, 6),
    )
    assert document.get_status([approval]) == "approved"
    assert document.get_status_label([approval]) == "Согласован"


def test_document_status_cancelled_approval():
    """Отменённое согласование не влияет на статус документа."""
    document = Document(
        doc_id=1,
        title="Договор",
        doc_type="Договор",
        author_id=2,
        deadline=date(2026, 10, 15),
    )
    approval = Approval(
        approval_id=1,
        document_id=1,
        user_id=3,
        decision="approved",
        comment="Ок",
        approval_date=date(2026, 10, 6),
        is_cancelled=True,
    )
    assert document.get_status([approval]) == "pending"


def test_document_str():
    """Строковое представление объекта документа."""
    document = Document(
        doc_id=1,
        title="Договор",
        doc_type="Договор",
        author_id=2,
        deadline=date(2026, 10, 15),
    )
    text = str(document)
    assert "Договор" in text
    assert "15.10.2026" in text


def test_add_document():
    """Добавление документа в коллекцию."""
    documents: list = []
    document = add_document(
        documents,
        title="Договор",
        doc_type="Договор",
        author_id=2,
        deadline=date(2026, 10, 15),
    )
    assert len(documents) == 1
    assert documents[0] is document
    assert document.id == 1


def test_find_document():
    """Поиск документа по подстроке названия (без учёта регистра)."""
    documents: list = []
    add_document(
        documents,
        title="Договор поставки",
        doc_type="Договор",
        author_id=1,
        deadline=date(2026, 10, 15),
    )
    add_document(
        documents,
        title="Акт приёма",
        doc_type="Акт",
        author_id=1,
        deadline=date(2026, 10, 15),
    )
    found = find_document(documents, "договор")
    assert len(found) == 1
    assert found[0].title == "Договор поставки"


def test_find_document_by_id():
    """Поиск документа по идентификатору."""
    documents: list = []
    add_document(
        documents,
        title="Договор",
        doc_type="Договор",
        author_id=1,
        deadline=date(2026, 10, 15),
    )
    document = find_document_by_id(documents, 1)
    assert document is not None
    assert document.id == 1
    assert find_document_by_id(documents, 999) is None


def test_sort_documents_by_deadline():
    """Сортировка документов по сроку согласования."""
    documents: list = []
    add_document(
        documents,
        title="Поздний",
        doc_type="Договор",
        author_id=1,
        deadline=date(2026, 12, 31),
    )
    add_document(
        documents,
        title="Ранний",
        doc_type="Договор",
        author_id=1,
        deadline=date(2026, 1, 1),
    )
    sorted_documents = sort_documents_by_deadline(documents)
    assert sorted_documents[0].title == "Ранний"
    assert sorted_documents[1].title == "Поздний"


def test_validate_title():
    """Проверка корректности названия документа."""
    assert Document.validate_title("Договор")
    assert not Document.validate_title("")
    assert not Document.validate_title("   ")


def test_document_to_dict_and_from_data():
    """Преобразование объекта в словарь и обратно."""
    document = Document(
        doc_id=1,
        title="Договор",
        doc_type="Договор",
        author_id=2,
        deadline=date(2026, 10, 15),
    )
    data = document.to_dict()
    assert data["id"] == 1
    assert data["title"] == "Договор"
    assert data["deadline"] == "2026-10-15"
    restored = Document.from_data(data)
    assert restored.id == 1
    assert restored.title == "Договор"
    assert restored.deadline == date(2026, 10, 15)
