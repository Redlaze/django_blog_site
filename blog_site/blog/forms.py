from django import forms


class EmailPostForm(forms.Form):
    name = forms.CharField(
        max_length=25,
        label='Имя',
    )
    email = forms.EmailField(
        label='E-mail',
    )
    to = forms.EmailField(
        label='Кому'
    )
    comments = forms.CharField(
        required=False,
        widget=forms.Textarea,
        label='Комментарии',
    )
