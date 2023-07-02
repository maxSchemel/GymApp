from GymApp.flaskr.src.domain.user import User
import pytest


class TestUser:

    def test_add_id(self):
        user = User("john", "password123")
        user_id = 123
        user.add_id(user_id)
        assert user.id == user_id


if __name__ == "__main__":
    pytest.main()
