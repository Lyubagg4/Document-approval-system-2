"""Автоматизированные тесты класса User и функций работы с пользователями.

Проверяются:
    * создание объекта User и значения его атрибутов;
    * строковое представление __str__;
    * метод класса from_data;
    * добавление пользователя в коллекцию;
    * поиск пользователя по подстроке;
    * поиск пользователя по идентификатору.
"""

from models import User
from models.users import add_user, find_user, find_user_by_id


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


def test_user_from_data():
    """Создание пользователя из словаря данных."""
    data = {
        "id": 1,
        "name": "Петров Пётр",
        "department": "Отдел закупок",
        "role": "Руководитель",
        "email": "petrov@example.com",
    }
    user = User.from_data(data)
    assert user.id == 1
    assert user.name == "Петров Пётр"
    assert user.email == "petrov@example.com"


def test_user_to_dict():
    """Преобразование пользователя в словарь."""
    user = User(
        user_id=1,
        name="Иванов Иван",
        department="Юридический отдел",
        role="Юрист",
        email="ivanov@example.com",
    )
    data = user.to_dict()
    assert data["id"] == 1
    assert data["name"] == "Иванов Иван"
    assert data["email"] == "ivanov@example.com"


def test_add_user():
    """Добавление пользователя в коллекцию."""
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
    """Поиск пользователя по подстроке ФИО или email."""
    users: list = []
    add_user(
        users,
        name="Иванов Иван",
        department="Юридический отдел",
        role="Юрист",
        email="ivanov@example.com",
    )
    add_user(
        users,
        name="Петров Пётр",
        department="Отдел закупок",
        role="Руководитель",
        email="petrov@example.com",
    )
    found = find_user(users, "иванов")
    assert len(found) == 1
    assert found[0].name == "Иванов Иван"
    found_email = find_user(users, "petrov@")
    assert len(found_email) == 1


def test_find_user_by_id():
    """Поиск пользователя по идентификатору."""
    users: list = []
    add_user(
        users,
        name="Иванов Иван",
        department="Юридический отдел",
        role="Юрист",
        email="ivanov@example.com",
    )
    user = find_user_by_id(users, 1)
    assert user is not None
    assert user.id == 1
    assert find_user_by_id(users, 999) is None
