from django import forms


class EmailLoginForm(forms.Form):
    email = forms.EmailField()
    email.widget.attrs.update({
            'class': 'input__wide',
        })
