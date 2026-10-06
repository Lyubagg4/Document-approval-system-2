"""Модуль работы с пользователями (ПР2 — функциональная модель)."""

from typing import Dict, List


def add_user(
    users: Dict[int, dict],
    name: str,
    department: str,
    role: str,
    email: str,
) -> dict:
    """Добавить пользователя в словарь users."""
    next_id = _next_id(list(users.keys()))
    user = {
        "id": next_id,
        "name": name,
        "department": department,
        "role": role,
        "email": email,
    }
    users[next_id] = user
    return user


def find_user(users: Dict[int, dict], query: str) -> List[dict]:
    """Найти пользователей по подстроке ФИО или email."""
    query_lower = query.lower()
    return [
        user
        for user in users.values()
        if query_lower in user["name"].lower()
        or query_lower in user["email"].lower()
    ]


def find_user_by_id(users: Dict[int, dict], user_id: int) -> dict:
    """Найти пользователя по идентификатору."""
    return users.get(user_id)


def show_users(users: Dict[int, dict]) -> None:
    """Вывести список пользователей."""
    if not users:
        print("Список пользователей пуст.")
        return
    print("\n--- Пользователи ---")
    for user in users.values():
        print(
            f"#{user['id']} {user['name']} "
            f"({user['department']}, {user['role']})"
        )


def _next_id(existing_ids: List[int]) -> int:
    """Вычислить следующий идентификатор."""
    if not existing_ids:
        return 1
    return max(existing_ids) + 1
