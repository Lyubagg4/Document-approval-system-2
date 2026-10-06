"""Модуль класса Document и CRUD-функций работы с документами.

Документ — основная сущность системы согласования. У каждого документа
есть название, тип, автор и срок согласования.

Для коллекции документов реализован базовый набор операций: создание,
поиск по идентификатору, обновление, удаление и вывод списка.
"""

from __future__ import annotations

from datetime import date
from typing import List, Optional


class Document:
    """Документ, проходящий согласование.

    Атрибуты:
        id (int): идентификатор документа;
        title (str): название документа;
        doc_type (str): тип документа (например, «Договор»);
        author_id (int): идентификатор автора документа;
        deadline (date): срок согласования документа.
    """

    def __init__(
        self,
        doc_id: int,
        title: str,
        doc_type: str,
        author_id: int,
        deadline: date,
    ) -> None:
        """Создать объект документа."""
        self.id = doc_id
        self.title = title
        self.doc_type = doc_type
        self.author_id = author_id
        self.deadline = deadline

    def __str__(self) -> str:
        """Вернуть строковое представление документа."""
        return (
            f"Документ #{self.id}: {self.title} "
            f"({self.doc_type}), срок "
            f"{self.deadline.strftime('%d.%m.%Y')}"
        )

    @classmethod
    def from_data(cls, data: dict) -> "Document":
        """Создать объект документа из словаря данных JSON."""
        deadline_str = data["deadline"]
        if isinstance(deadline_str, date):
            deadline_value = deadline_str
        else:
            deadline_value = date.fromisoformat(deadline_str)
        return cls(
            doc_id=data["id"],
            title=data["title"],
            doc_type=data["doc_type"],
            author_id=data["author_id"],
            deadline=deadline_value,
        )

    def to_dict(self) -> dict:
        """Преобразовать объект документа в словарь для JSON."""
        return {
            "id": self.id,
            "title": self.title,
            "doc_type": self.doc_type,
            "author_id": self.author_id,
            "deadline": self.deadline.isoformat(),
        }


def add_document(
    documents: List[Document],
    title: str,
    doc_type: str,
    author_id: int,
    deadline: date,
) -> Document:
    """Создать документ и добавить его в коллекцию.

    Args:
        documents: коллекция документов;
        title: название документа;
        doc_type: тип документа;
        author_id: идентификатор автора;
        deadline: срок согласования.

    Returns:
        Созданный объект Document.
    """
    next_id = _next_id(documents)
    document = Document(
        doc_id=next_id,
        title=title,
        doc_type=doc_type,
        author_id=author_id,
        deadline=deadline,
    )
    documents.append(document)
    return document


def find_document(
    documents: List[Document],
    doc_id: int,
) -> Optional[Document]:
    """Найти документ по идентификатору.

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


def update_document(
    documents: List[Document],
    doc_id: int,
    title: Optional[str] = None,
    doc_type: Optional[str] = None,
    deadline: Optional[date] = None,
) -> bool:
    """Обновить данные документа.

    Обновляются только переданные поля. Идентификаторы документа и автора
    не меняются: автор задаётся при создании и остаётся неизменным.

    Args:
        documents: коллекция документов;
        doc_id: идентификатор документа;
        title: новое название (если передано);
        doc_type: новый тип (если передано);
        deadline: новый срок (если передано).

    Returns:
        True, если документ найден и обновлён.
    """
    document = find_document(documents, doc_id)
    if document is None:
        return False
    if title is not None:
        document.title = title
    if doc_type is not None:
        document.doc_type = doc_type
    if deadline is not None:
        document.deadline = deadline
    return True


def delete_document(
    documents: List[Document],
    doc_id: int,
) -> bool:
    """Удалить документ из коллекции.

    Args:
        documents: коллекция документов;
        doc_id: идентификатор документа.

    Returns:
        True, если документ найден и удалён.
    """
    document = find_document(documents, doc_id)
    if document is None:
        return False
    documents.remove(document)
    return True


def show_documents(documents: List[Document]) -> None:
    """Вывести список документов.

    Args:
        documents: коллекция документов.
    """
    if not documents:
        print("Список документов пуст.")
        return
    print("\n--- Документы ---")
    for document in documents:
        print(document)


def _next_id(documents: List[Document]) -> int:
    """Вычислить следующий идентификатор документа."""
    if not documents:
        return 1
    return max(document.id for document in documents) + 1
