from django import forms


class PaymentForm(forms.Form):
    card_number = forms.CharField(label='Card Number', required=True)
    exp_month = forms.IntegerField(label='Expiration Month', required=True)
    exp_year = forms.IntegerField(label='Expiration Year', required=True)
    cvc = forms.CharField(label='CVC', required=True)

    token = forms.CharField(widget=forms.HiddenInput, required=True)
