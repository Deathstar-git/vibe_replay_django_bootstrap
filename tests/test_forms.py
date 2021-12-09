from django.test import TestCase
from main.forms import RegisterUserForm, LoginUserForm


class RegisterUserFormTest(TestCase):
    # Проверка правильного описания к полю username
    def test_username_field_label(self):
        form = RegisterUserForm()
        self.assertTrue(form.fields['username'].label is None or form.fields['username'].label == 'Логин:')

    def test_username_field_placeholder(self):
        form = RegisterUserForm()
        self.assertEqual(form.fields['username'].widget.attrs['placeholder'], 'Придумайте логин')

    # Проверка правильного описания к полю password
    def test_password_field_label(self):
        form = RegisterUserForm()
        self.assertTrue(form.fields['password1'].label is None or form.fields['password1'].label == 'Пароль:')

    def test_password_field_placeholder(self):
        form = RegisterUserForm()
        self.assertEqual(form.fields['password1'].widget.attrs['placeholder'], 'Придумайте пароль')


class LoginUserFormTest(TestCase):
    # Проверка правильного описания к полю username
    def test_username_field_label(self):
        form = LoginUserForm()
        self.assertTrue(form.fields['username'].label is None or form.fields['username'].label == 'Логин:')

    def test_username_field_placeholder(self):
        form = LoginUserForm()
        self.assertEqual(form.fields['username'].widget.attrs['placeholder'], 'Введите логин')

    # Проверка правильного описания к полю password
    def test_password_field_label(self):
        form = LoginUserForm()
        self.assertTrue(form.fields['password'].label is None or form.fields['password'].label == 'Пароль:')

    def test_password_field_placeholder(self):
        form = LoginUserForm()
        self.assertEqual(form.fields['password'].widget.attrs['placeholder'], 'Введите пароль')
