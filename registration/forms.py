from django import forms


class PaymentForm(forms.Form):
    email = forms.EmailField()
    name = forms.CharField(max_length=30)
    card_number = forms.CharField(max_length=20)
    card_expiry_date = forms.DateField()
    birth_date = forms.DateField()
    card_password = forms.CharField(max_length=2)

    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'class': 'input__wide',
        })
        self.fields['name'].widget.attrs.update({
            'class': 'input__wide',
        })
        self.fields['card_number'].widget.attrs.update({
            'class': 'input__wide',
        })
        self.fields['card_expiry_date'].widget.attrs.update({
            'class': 'input__wide',
        })
        self.fields['birth_date'].widget.attrs.update({
            'class': 'input__wide',
        })
        self.fields['card_password'].widget.attrs.update({
            'class': 'input__wide',
        })
