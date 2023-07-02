from ..user import InvalidPassword, User
import pytest
from werkzeug.security import generate_password_hash


class TestUser:
    def test_check_user_validity_valid_password(self):
        user = User("john", "password123")
        password = generate_password_hash("password123")
        user.check_user_validity(password)

    def test_check_user_validity_invalid_password(self):
        user = User("john", "password123")
        password = generate_password_hash("incorrectpassword")
        with pytest.raises(InvalidPassword):
            user.check_user_validity(password)

    def test_add_id(self):
        user = User("john", "password123")
        user_id = 123
        user.add_id(user_id)
        assert user.id == user_id


if __name__ == "__main__":
    pytest.main()
