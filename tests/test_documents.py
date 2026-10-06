"""Автоматизированные тесты класса Document и CRUD-функций.

Проверяются:
    * создание объекта Document и значения его атрибутов;
    * строковое представление __str__;
    * метод класса from_data и to_dict (преобразование в/из JSON);
    * добавление документа в коллекцию (Create);
    * поиск документа по идентификатору (Read);
    * обновление данных документа (Update);
    * удаление документа из коллекции (Delete).
"""

from datetime import date

from models import Document
from models.documents import (
    add_document,
    delete_document,
    find_document,
    update_document,
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


def test_document_from_data_and_to_dict():
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


def test_add_document():
    """Добавление документа в коллекцию (Create)."""
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
    """Поиск документа по идентификатору (Read)."""
    documents: list = []
    add_document(
        documents,
        title="Договор",
        doc_type="Договор",
        author_id=1,
        deadline=date(2026, 10, 15),
    )
    document = find_document(documents, 1)
    assert document is not None
    assert document.id == 1
    assert find_document(documents, 999) is None


def test_update_document():
    """Обновление данных документа (Update)."""
    documents: list = []
    add_document(
        documents,
        title="Договор",
        doc_type="Договор",
        author_id=1,
        deadline=date(2026, 10, 15),
    )
    result = update_document(
        documents,
        1,
        title="Новый договор",
        deadline=date(2026, 11, 1),
    )
    assert result is True
    document = find_document(documents, 1)
    assert document.title == "Новый договор"
    assert document.deadline == date(2026, 11, 1)
    assert document.doc_type == "Договор"  # не менялось


def test_update_unknown_document():
    """Обновление несуществующего документа возвращает False."""
    documents: list = []
    result = update_document(documents, 999, title="X")
    assert result is False


def test_delete_document():
    """Удаление документа из коллекции (Delete)."""
    documents: list = []
    add_document(
        documents,
        title="Договор",
        doc_type="Договор",
        author_id=1,
        deadline=date(2026, 10, 15),
    )
    result = delete_document(documents, 1)
    assert result is True
    assert len(documents) == 0
    assert find_document(documents, 1) is None


def test_delete_unknown_document():
    """Удаление несуществующего документа возвращает False."""
    documents: list = []
    result = delete_document(documents, 999)
    assert result is False
