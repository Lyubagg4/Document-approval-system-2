"""Модуль класса Document и функций работы с коллекцией документов.

Документ — основная сущность системы согласования. У каждого документа
есть название, тип, автор, срок согласования и текущий статус. Статус
вычисляется на основе списка согласований: если есть согласование с
решением «approved» — документ согласован, если «rejected» — отклонён,
иначе — на согласовании.

Модуль также содержит функции работы с коллекцией документов:
добавление, поиск, фильтрация и сортировка. Эти функции остаются
обычными функциями, так как они оперируют коллекцией, а не отдельным
документом.
"""

from __future__ import annotations

from datetime import date
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .approvals import Approval


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
        """Создать объект документа.

        Args:
            doc_id: идентификатор документа;
            title: название документа;
            doc_type: тип документа;
            author_id: идентификатор автора документа;
            deadline: крайний срок согласования.
        """
        self.id = doc_id
        self.title = title
        self.doc_type = doc_type
        self.author_id = author_id
        self.deadline = deadline

    def is_overdue(self, current_date: date) -> bool:
        """Проверить, истёк ли срок согласования документа.

        Args:
            current_date: текущая дата для сравнения.

        Returns:
            True, если срок согласования истёк.
        """
        return current_date > self.deadline

    def get_status(self, approvals: List[Approval]) -> str:
        """Определить статус документа по списку согласований.

        Статусы: «approved» — согласован, «rejected» — отклонён,
        «pending» — на согласовании.

        Args:
            approvals: коллекция согласований документа.

        Returns:
            Код статуса документа.
        """
        for approval in approvals:
            if approval.document_id != self.id:
                continue
            if approval.is_cancelled:
                continue
            if approval.decision == "approved":
                return "approved"
            if approval.decision == "rejected":
                return "rejected"
        return "pending"

    def get_status_label(self, approvals: List[Approval]) -> str:
        """Вернуть текстовое представление статуса документа.

        Args:
            approvals: коллекция согласований документа.

        Returns:
            Одно из значений: «Согласован», «Отклонён», «На согласовании».
        """
        status = self.get_status(approvals)
        if status == "approved":
            return "Согласован"
        if status == "rejected":
            return "Отклонён"
        return "На согласовании"

    def __str__(self) -> str:
        """Вернуть строковое представление документа."""
        return (
            f"Документ #{self.id}: {self.title} "
            f"({self.doc_type}), срок {self.deadline.strftime('%d.%m.%Y')}"
        )

    @staticmethod
    def validate_title(title: str) -> bool:
        """Проверить корректность названия документа.

        Args:
            title: название документа.

        Returns:
            True, если название не пустое после обрезки пробелов.
        """
        return bool(title and title.strip())

    @classmethod
    def from_data(cls, data: dict) -> "Document":
        """Создать объект документа из словаря данных JSON.

        Args:
            data: словарь с ключами id, title, doc_type,
                author_id, deadline.

        Returns:
            Объект Document.
        """
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
        """Преобразовать объект документа в словарь для JSON.

        Returns:
            Словарь с ключами id, title, doc_type, author_id, deadline.
        """
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
    """Добавить документ в коллекцию.

    Args:
        documents: коллекция документов;
        title: название документа;
        doc_type: тип документа;
        author_id: идентификатор автора;
        deadline: срок согласования.

    Returns:
        Созданный объект Document.
    """
    next_id = _next_document_id(documents)
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
    query: str,
) -> List[Document]:
    """Найти документы по подстроке названия.

    Поиск регистронезависимый.

    Args:
        documents: коллекция документов;
        query: подстрока для поиска.

    Returns:
        Список документов, в названии которых встречается query.
    """
    query_lower = query.lower()
    return [
        document
        for document in documents
        if query_lower in document.title.lower()
    ]


def find_document_by_id(
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


def filter_documents_by_type(
    documents: List[Document],
    doc_type: str,
) -> List[Document]:
    """Отобрать документы указанного типа.

    Args:
        documents: коллекция документов;
        doc_type: тип документа.

    Returns:
        Список документов выбранного типа.
    """
    return [
        document
        for document in documents
        if document.doc_type == doc_type
    ]


def sort_documents_by_deadline(
    documents: List[Document],
) -> List[Document]:
    """Отсортировать документы по сроку согласования.

    Сортировка выполняется по возрастанию даты. Используется
    lambda-функция в качестве ключа сортировки.

    Args:
        documents: коллекция документов.

    Returns:
        Новый список документов, упорядоченный по сроку.
    """
    return sorted(documents, key=lambda document: document.deadline)


def show_documents(
    documents: List[Document],
    approvals: List[Approval],
) -> None:
    """Вывести список документов с их статусами.

    Args:
        documents: коллекция документов;
        approvals: коллекция согласований.
    """
    if not documents:
        print("Список документов пуст.")
        return
    print("\n--- Документы ---")
    for document in documents:
        status_label = document.get_status_label(approvals)
        print(f"{document} | Статус: {status_label}")


def _next_document_id(documents: List[Document]) -> int:
    """Вычислить следующий идентификатор документа.

    Args:
        documents: коллекция документов.

    Returns:
        Значение на единицу больше максимального существующего id.
    """
    if not documents:
        return 1
    return max(document.id for document in documents) + 1
