import json
import re

from django import forms
from django.core.exceptions import ValidationError

from .models import Mod


class ModForm(forms.ModelForm):
    slug = forms.SlugField(
        min_length=3,
        max_length=100,
        label='URL-ідентифікатор',
        help_text='Від 3 до 100 символів: латинські літери, цифри та дефіси.',
        error_messages={
            'required': 'Вкажіть URL-ідентифікатор.',
            'invalid': 'Використовуйте лише латинські літери, цифри та дефіси.',
            'min_length': 'Ідентифікатор має містити щонайменше 3 символи.',
            'max_length': 'Ідентифікатор не може бути довшим за 100 символів.',
            'unique': 'Картка з таким URL-ідентифікатором уже існує.',
        },
    )
    name = forms.CharField(
        min_length=2,
        max_length=100,
        label='Назва',
        error_messages={
            'required': 'Вкажіть назву картки.',
            'min_length': 'Назва має містити щонайменше 2 символи.',
            'max_length': 'Назва не може бути довшою за 100 символів.',
        },
    )
    logo = forms.CharField(
        min_length=14,
        max_length=255,
        label='Шлях до логотипа',
        help_text='Шлях до зображення у static, наприклад main/img/my-mod.webp.',
        error_messages={
            'required': 'Вкажіть шлях до логотипа.',
            'min_length': 'Вкажіть коректний шлях до логотипа.',
            'max_length': 'Шлях до логотипа не може бути довшим за 255 символів.',
        },
    )
    description = forms.CharField(
        min_length=20,
        max_length=2000,
        widget=forms.Textarea(attrs={'rows': 4}),
        label='Опис',
        error_messages={
            'required': 'Вкажіть опис картки.',
            'min_length': 'Опис має містити щонайменше 20 символів.',
            'max_length': 'Опис не може бути довшим за 2000 символів.',
        },
    )
    category = forms.CharField(
        min_length=2,
        max_length=50,
        label='Категорія',
        error_messages={
            'required': 'Вкажіть категорію.',
            'min_length': 'Назва категорії має містити щонайменше 2 символи.',
            'max_length': 'Категорія не може бути довшою за 50 символів.',
        },
    )
    mc_version = forms.CharField(
        min_length=1,
        max_length=20,
        label='Версія Minecraft',
        help_text='Наприклад: 1.20.1 або 1.21+.',
        error_messages={
            'required': 'Вкажіть версію Minecraft.',
            'min_length': 'Вкажіть версію Minecraft.',
            'max_length': 'Версія не може бути довшою за 20 символів.',
        },
    )
    downloads = forms.CharField(
        min_length=1,
        max_length=20,
        label='Кількість завантажень',
        help_text='Введіть число, наприклад 1500, 50M+ або 2.5K.',
        error_messages={
            'required': 'Вкажіть кількість завантажень.',
            'min_length': 'Вкажіть кількість завантажень.',
            'max_length': 'Значення не може бути довшим за 20 символів.',
        },
    )
    features = forms.CharField(
        max_length=4000,
        widget=forms.Textarea(attrs={'rows': 5}),
        label='Особливості (JSON)',
        help_text='Введіть JSON-масив із 1–10 рядків, наприклад ["Швидкий", "Сумісний"].',
        error_messages={
            'required': 'Додайте хоча б одну особливість.',
            'invalid': 'Особливості не можуть бути довшими за 4000 символів.',
            'max_length': 'Особливості не можуть бути довшими за 4000 символів.',
        },
    )

    class Meta:
        model = Mod
        fields = (
            'slug',
            'name',
            'logo',
            'description',
            'category',
            'mc_version',
            'downloads',
            'features',
            'tags',
        )
        labels = {'tags': 'Теги'}
        error_messages = {'tags': {'invalid_choice': 'Оберіть теги зі списку.'}}
        widgets = {
            'tags': forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name != 'tags':
                field.widget.attrs['class'] = 'form-control'
        self.fields['tags'].widget.attrs['class'] = 'form-check-input'

    def clean_logo(self):
        logo = self.cleaned_data['logo'].strip()
        if not re.fullmatch(
            r'main/img/[A-Za-z0-9][A-Za-z0-9._-]*\.(?:png|jpe?g|webp|gif)',
            logo,
            flags=re.IGNORECASE,
        ):
            raise ValidationError(
                'Логотип має бути зображенням із папки static/main/img/.'
            )
        return logo

    def clean_mc_version(self):
        version = self.cleaned_data['mc_version'].strip()
        if not re.fullmatch(r'\d+(?:\.\d+)*(?:\+)?', version):
            raise ValidationError(
                'Вкажіть версію у форматі 1.20.1 або 1.21+.'
            )
        return version

    def clean_downloads(self):
        downloads = self.cleaned_data['downloads'].strip()
        if not re.fullmatch(r'\d+(?:[.,]\d+)?\s*[KMB]?\+?', downloads, re.IGNORECASE):
            raise ValidationError(
                'Введіть число завантажень, наприклад 1500, 50M+ або 2.5K.'
            )
        return downloads

    def clean_features(self):
        raw_features = self.cleaned_data['features']
        try:
            features = json.loads(raw_features)
        except json.JSONDecodeError as exc:
            raise ValidationError(
                'Введіть коректний JSON-масив особливостей.'
            ) from exc

        if not isinstance(features, list) or not 1 <= len(features) <= 10:
            raise ValidationError(
                'Потрібно вказати JSON-масив від 1 до 10 особливостей.'
            )
        if any(
            not isinstance(feature, str)
            or not 2 <= len(feature.strip()) <= 120
            for feature in features
        ):
            raise ValidationError(
                'Кожна особливість має бути рядком довжиною від 2 до 120 символів.'
            )
        return [feature.strip() for feature in features]

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        if len(tags) > 10:
            raise ValidationError('Можна обрати не більше 10 тегів.')
        return tags
