from django import forms

from .models import Post, IP

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)

    def clean_text(self):
        text = self.cleaned_data.get("text")
        if "hack" in text:
            raise forms.ValidationError("Impossibile pubblicare il post!")
        else:
        	return text

class Login(forms.ModelForm):
    class Meta:
        model = IP
        fields = ()
