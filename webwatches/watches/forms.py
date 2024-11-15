from django import forms
from .models import Cart

class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['quantity']  # You can add more fields if needed, e.g., removing items

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quantity'].widget = forms.NumberInput(attrs={'min': 1})

class CheckoutForm(forms.Form):
    address = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter your shipping address'}))
    payment_method = forms.ChoiceField(choices=[
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
    ])