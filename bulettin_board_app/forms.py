from django import forms

from bulettin_board_app.models import Announcement


class AnnoucementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['name', 'description', 'user', 'category', 'locations']
        labels = {
            'name': 'Nazwa',
            'description': 'Opis',
            'user': 'User',
            'category': 'Kategoria',
            'locations': 'Lokalizacja'
        }
        widgets = {'description': forms.Textarea(attrs={'cols': 80})}