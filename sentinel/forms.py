from django import forms


class EmailLoginForm(forms.Form):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'class': 'input__wide',
            'autofocus': 'autofocus',
        })
