"""Модуль класса User и CRUD-функций работы с пользователями.

Пользователь — сотрудник организации, который может выступать как автором
документа, так и согласующим.

Для коллекции пользователей реализован базовый набор операций: создание,
поиск по идентификатору, обновление, удаление и вывод списка.
"""

from typing import List, Optional


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
        """Создать объект пользователя."""
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
        """Создать пользователя из словаря данных JSON."""
        return cls(
            user_id=data["id"],
            name=data["name"],
            department=data["department"],
            role=data["role"],
            email=data["email"],
        )

    def to_dict(self) -> dict:
        """Преобразовать пользователя в словарь для JSON."""
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
    """Создать пользователя и добавить его в коллекцию.

    Args:
        users: коллекция пользователей;
        name: ФИО пользователя;
        department: подразделение;
        role: должность;
        email: адрес электронной почты.

    Returns:
        Созданный объект User.
    """
    next_id = _next_id(users)
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
    user_id: int,
) -> Optional[User]:
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


def update_user(
    users: List[User],
    user_id: int,
    name: Optional[str] = None,
    department: Optional[str] = None,
    role: Optional[str] = None,
    email: Optional[str] = None,
) -> bool:
    """Обновить данные пользователя.

    Обновляются только переданные поля. Идентификатор не меняется.

    Args:
        users: коллекция пользователей;
        user_id: идентификатор пользователя;
        name: новое ФИО (если передано);
        department: новое подразделение (если передано);
        role: новая должность (если передано);
        email: новый email (если передано).

    Returns:
        True, если пользователь найден и обновлён.
    """
    user = find_user(users, user_id)
    if user is None:
        return False
    if name is not None:
        user.name = name
    if department is not None:
        user.department = department
    if role is not None:
        user.role = role
    if email is not None:
        user.email = email
    return True


def delete_user(
    users: List[User],
    user_id: int,
) -> bool:
    """Удалить пользователя из коллекции.

    Args:
        users: коллекция пользователей;
        user_id: идентификатор пользователя.

    Returns:
        True, если пользователь найден и удалён.
    """
    user = find_user(users, user_id)
    if user is None:
        return False
    users.remove(user)
    return True


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


def _next_id(users: List[User]) -> int:
    """Вычислить следующий идентификатор пользователя."""
    if not users:
        return 1
    return max(user.id for user in users) + 1
