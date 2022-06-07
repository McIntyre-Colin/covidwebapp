from django import forms
from apps.core.models import Book, ReadingList, Chart, StateEntry


class AddChartForm(forms.ModelForm):
    class Meta:
        model = Chart
        fields = ['title','chart_type', 'day', 'month', 'year','filter_field']

class AddStateEntryForm(forms.ModelForm):
    class Meta:
        model = StateEntry
        exclude = ['plot']



class AddBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'description']

class AddReadingListForm(forms.ModelForm):
    class Meta:
        model = ReadingList
        fields = ['title', 'category', 'description']

