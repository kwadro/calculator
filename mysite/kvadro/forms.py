from django import forms

class CalculateForm(forms.Form):
    name = forms.CharField(initial="Свято", label="Назва")
    count_people = forms.IntegerField(initial=10, min_value=3, max_value=100, label="Кількість гостей", help_text="")
    count_man = forms.IntegerField(initial=5, min_value=0, max_value=100, label="Чоловіків", help_text="")
    count_woman = forms.IntegerField(initial=5, min_value=0, max_value=100, label="Жінок", help_text="")

class CalculateRecipeForm(forms.Form):
    name = forms.CharField(initial="Продукти", label="Продукти")