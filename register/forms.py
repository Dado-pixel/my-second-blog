
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)
User = get_user_model()




class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)

            if not user:
                raise forms.ValidationError('Utente inesistente')
            if not user.check_password(password):
                raise forms.ValidationError('Password errata')
            if not user.is_active:
                raise forms.ValidationError('Utente disabilitato')
        return super(UserLoginForm, self).clean(*args, **kwargs)

class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(label='Indirizzo e-mail')
    email_confirmation = forms.EmailField(label='Conferma e-mail')
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'email_confirmation',
            'password',
        ]

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        email_confirmation = self.cleaned_data.get('email_confirmation')
        if email != email_confirmation:
            raise forms.ValidationError('Sono stati inseriti due indirizzi e-mail differenti')
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError('Indirizzo e-mail utilizzato')
        return super(UserRegisterForm, self).clean(*args, **kwargs)
