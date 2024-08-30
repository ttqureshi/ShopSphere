from django.test import TestCase

from users.forms import UserRegisterForm, OrderForm, UserUpdateForm


class TestUserRegisterForm(TestCase):
    def test_register_valid_form(self):
        form = UserRegisterForm(
            data={
                "username": "testuser",
                "email": "testuser@gmail.com",
                "password1": "qwe!2#5ewer",
                "password2": "qwe!2#5ewer",
            }
        )
        self.assertTrue(form.is_valid())

    def test_register_invalid_form(self):
        for i in range(4):
            data = {
                "username": "testuser",
                "email": "testuser@gmail.com",
                "password1": "password123",
                "password2": "password123",
            }
            keys = list(data.keys())
            del data[keys[i]]
            form = UserRegisterForm(data=data)
            self.assertFalse(form.is_valid())


class TestOrderForm(TestCase):
    def test_order_valid_form(self):
        form = OrderForm(
            data={
                "full_name": "fullname",
                "contact_no": "+923000000000",
                "address": "address",
                "city": "city",
                "state": "state",
                "zipcode": "12345",
                "country": "country",
            }
        )

        self.assertTrue(form.is_valid())

    def test_order_invalid_form(self):
        for i in range(7):
            data = {
                "full_name": "fullname",
                "contact_no": "+923000000000",
                "address": "address",
                "city": "city",
                "state": "state",
                "zipcode": "12345",
                "country": "country",
            }
            keys = list(data.keys())
            del data[keys[i]]
            form = OrderForm(data=data)
            self.assertFalse(form.is_valid())


class TestUserUpdateForm(TestCase):
    def test_user_update_valid_form(self):
        form = UserUpdateForm(
            data={
                "username": "username",
                "email": "user@gmail.com",
            }
        )

        self.assertTrue(form.is_valid())

    def test_user_update_invalid_form(self):
        form1 = UserUpdateForm(
            data={
                "email": "user@gmail.com",
            }
        )
        form2 = UserUpdateForm(
            data={
                "username": "username",
            }
        )
        self.assertFalse(form1.is_valid())
        self.assertFalse(form2.is_valid())
