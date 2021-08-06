from django import forms
from components.models import Bloggers

class BloggersForm(forms.ModelForm):
    class Meta:
        model = Bloggers
        fields = "__all__"
