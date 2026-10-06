"""Модуль класса User и функций работы с пользователями.

Пользователь — сотрудник организации, который может выступать как автором
документа, так и согласующим. Класс User описывает данные пользователя и
базовое строковое представление; функции модуля работают с коллекцией
пользователей: добавление, поиск и вывод списка.
"""

from typing import List


class User:
    """Пользователь системы согласования документов.

    Атрибуты:
        id (int): идентификатор пользователя;
        name (str): ФИО пользователя;
        department (str): подразделение пользователя;
        role (str): должность пользователя;
        email (str): адрес электронной почты.
    """

    def __init__(
        self,
        user_id: int,
        name: str,
        department: str,
        role: str,
        email: str,
    ) -> None:
        """Создать объект пользователя.

        Args:
            user_id: идентификатор пользователя;
            name: ФИО пользователя;
            department: подразделение;
            role: должность;
            email: адрес электронной почты.
        """
        self.id = user_id
        self.name = name
        self.department = department
        self.role = role
        self.email = email

    def __str__(self) -> str:
        """Вернуть строковое представление пользователя."""
        return (
            f"#{self.id} {self.name} "
            f"({self.department}, {self.role})"
        )

    @classmethod
    def from_data(cls, data: dict) -> "User":
        """Создать пользователя из словаря данных JSON.

        Args:
            data: словарь с ключами id, name, department, role, email.

        Returns:
            Объект User.
        """
        return cls(
            user_id=data["id"],
            name=data["name"],
            department=data["department"],
            role=data["role"],
            email=data["email"],
        )

    def to_dict(self) -> dict:
        """Преобразовать пользователя в словарь для JSON.

        Returns:
            Словарь с полями пользователя.
        """
        return {
            "id": self.id,
            "name": self.name,
            "department": self.department,
            "role": self.role,
            "email": self.email,
        }


def add_user(
    users: List[User],
    name: str,
    department: str,
    role: str,
    email: str,
) -> User:
    """Добавить пользователя в коллекцию.

    Args:
        users: коллекция пользователей;
        name: ФИО пользователя;
        department: подразделение;
        role: должность;
        email: адрес электронной почты.

    Returns:
        Созданный объект User.
    """
    next_id = _next_user_id(users)
    user = User(
        user_id=next_id,
        name=name,
        department=department,
        role=role,
        email=email,
    )
    users.append(user)
    return user


def find_user(
    users: List[User],
    query: str,
) -> List[User]:
    """Найти пользователей по подстроке ФИО или email.

    Args:
        users: коллекция пользователей;
        query: подстрока поиска.

    Returns:
        Список найденных пользователей.
    """
    query_lower = query.lower()
    return [
        user
        for user in users
        if query_lower in user.name.lower()
        or query_lower in user.email.lower()
    ]


def find_user_by_id(users: List[User], user_id: int) -> User | None:
    """Найти пользователя по идентификатору.

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


def show_users(users: List[User]) -> None:
    """Вывести список пользователей.

    Args:
        users: коллекция пользователей.
    """
    if not users:
        print("Список пользователей пуст.")
        return
    print("\n--- Пользователи ---")
    for user in users:
        print(user)


def _next_user_id(users: List[User]) -> int:
    """Вычислить следующий идентификатор пользователя.

    Args:
        users: коллекция пользователей.

    Returns:
        Значение на единицу больше максимального существующего id.
    """
    if not users:
        return 1
    return max(user.id for user in users) + 1
