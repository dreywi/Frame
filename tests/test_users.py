import pytest

from models import User
from models.users import add_user, find_user, find_user_by_id


def test_user_creation():
    user = User(1, "Анна", "anna@example.com")
    assert user.id == 1
    assert user.name == "Анна"
    assert user.email == "anna@example.com"


def test_user_str():
    assert str(User(1, "Анна", "anna@example.com")) == (
        "[1] Анна <anna@example.com>"
    )


def test_user_invalid_email():
    with pytest.raises(ValueError):
        User(1, "Анна", "no-email")


def test_user_from_data():
    user = User.from_data({"id": 5, "name": "Иван", "email": "i@x.ru"})
    assert isinstance(user, User)
    assert user.id == 5


def test_add_user_assigns_next_id():
    users = [User(1, "Анна", "anna@example.com")]
    add_user(users, "Иван", "ivan@example.com")
    assert len(users) == 2
    assert users[1].id == 2


def test_find_user_by_name_and_email():
    users = [User(1, "Анна", "anna@example.com"),
             User(2, "Иван", "ivan@example.com")]
    assert find_user(users, "анна") == [users[0]]
    assert find_user(users, "IVAN@") == [users[1]]


def test_find_user_by_id_missing():
    assert find_user_by_id([], 1) is None
