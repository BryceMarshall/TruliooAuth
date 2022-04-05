from django.forms import EmailField, CharField, ModelForm, Form, PasswordInput


class LoginForm(Form):
    email = EmailField()
    password = CharField(widget=PasswordInput(attrs={'data-toggle': 'password'}))

class RegisterForm(Form):
    email = EmailField()
    password = CharField(widget=PasswordInput(attrs={'data-toggle': 'password'}))
    confirm_password = CharField(widget=PasswordInput(attrs={'data-toggle': 'password'}))


