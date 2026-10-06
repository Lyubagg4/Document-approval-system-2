"""Пакет объектной модели предметной области.

Содержит классы основных сущностей системы согласования документов:
Document, User и Approval. Классы импортируются из пакета models.

Пример использования:
    from models import Document, User, Approval
"""

from .documents import Document
from .users import User
from .approvals import Approval

__all__ = ["Document", "User", "Approval"]
