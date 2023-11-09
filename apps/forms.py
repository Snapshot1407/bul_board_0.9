from django import forms
from snowpenguin.django.recaptcha3.fields import ReCaptchaField
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Reviews, Rating, RatingStar, Post


class PostAdminForm(forms.ModelForm):
    """Форма с виджетом ckeditor"""
    description_ru = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())
    description_en = forms.CharField(label="Описание_en", widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'

class ReviewForm(forms.ModelForm):
    """Форма отзывов"""
    captcha = ReCaptchaField()

    class Meta:
        model = Reviews
        fields = ("name", "email", "text", "captcha")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control border"}),
            "email": forms.EmailInput(attrs={"class": "form-control border"}),
            "text": forms.Textarea(attrs={"class": "form-control border"})
        }


class RatingForm(forms.ModelForm):
    """Форма добавления рейтинга"""
    star = forms.ModelChoiceField(
        queryset=RatingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None
    )

    class Meta:
        model = Rating
        fields = ("star",)
