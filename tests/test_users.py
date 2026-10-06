"""Автоматизированные тесты класса User и CRUD-функций.

Проверяются:
    * создание объекта User и значения его атрибутов;
    * строковое представление __str__;
    * метод класса from_data и to_dict (преобразование в/из JSON);
    * добавление пользователя в коллекцию (Create);
    * поиск пользователя по идентификатору (Read);
    * обновление данных пользователя (Update);
    * удаление пользователя из коллекции (Delete).
"""

from models import User
from models.users import (
    add_user,
    delete_user,
    find_user,
    update_user,
)


def test_user_creation():
    """Создание объекта User и проверка атрибутов."""
    user = User(
        user_id=1,
        name="Иванов Иван",
        department="Юридический отдел",
        role="Юрист",
        email="ivanov@example.com",
    )
    assert user.id == 1
    assert user.name == "Иванов Иван"
    assert user.department == "Юридический отдел"
    assert user.role == "Юрист"
    assert user.email == "ivanov@example.com"


def test_user_str():
    """Строковое представление объекта пользователя."""
    user = User(
        user_id=1,
        name="Иванов Иван",
        department="Юридический отдел",
        role="Юрист",
        email="ivanov@example.com",
    )
    text = str(user)
    assert "Иванов Иван" in text
    assert "Юридический отдел" in text
    assert "Юрист" in text


def test_user_from_data_and_to_dict():
    """Преобразование пользователя в словарь и обратно."""
    user = User(
        user_id=1,
        name="Петров Пётр",
        department="Отдел закупок",
        role="Руководитель",
        email="petrov@example.com",
    )
    data = user.to_dict()
    assert data["id"] == 1
    assert data["name"] == "Петров Пётр"
    restored = User.from_data(data)
    assert restored.id == 1
    assert restored.email == "petrov@example.com"


def test_add_user():
    """Добавление пользователя в коллекцию (Create)."""
    users: list = []
    user = add_user(
        users,
        name="Иванов Иван",
        department="Юридический отдел",
        role="Юрист",
        email="ivanov@example.com",
    )
    assert len(users) == 1
    assert users[0] is user
    assert user.id == 1


def test_find_user():
    """Поиск пользователя по идентификатору (Read)."""
    users: list = []
    add_user(
        users,
        name="Иванов Иван",
        department="Юридический отдел",
        role="Юрист",
        email="ivanov@example.com",
    )
    user = find_user(users, 1)
    assert user is not None
    assert user.id == 1
    assert find_user(users, 999) is None


def test_update_user():
    """Обновление данных пользователя (Update)."""
    users: list = []
    add_user(
        users,
        name="Иванов Иван",
        department="Юридический отдел",
        role="Юрист",
        email="ivanov@example.com",
    )
    result = update_user(
        users,
        1,
        name="Петров Пётр",
        email="petrov@example.com",
    )
    assert result is True
    user = find_user(users, 1)
    assert user.name == "Петров Пётр"
    assert user.email == "petrov@example.com"
    assert user.department == "Юридический отдел"  # не менялось


def test_update_unknown_user():
    """Обновление несуществующего пользователя возвращает False."""
    users: list = []
    result = update_user(users, 999, name="X")
    assert result is False


def test_delete_user():
    """Удаление пользователя из коллекции (Delete)."""
    users: list = []
    add_user(
        users,
        name="Иванов Иван",
        department="Юридический отдел",
        role="Юрист",
        email="ivanov@example.com",
    )
    result = delete_user(users, 1)
    assert result is True
    assert len(users) == 0
    assert find_user(users, 1) is None


def test_delete_unknown_user():
    """Удаление несуществующего пользователя возвращает False."""
    users: list = []
    result = delete_user(users, 999)
    assert result is False
