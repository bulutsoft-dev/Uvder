from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    """
    İletişim Formu
    """
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Adınız Soyadınız',
                'required': 'required'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': 'E-posta Adresiniz',
                'required': 'required'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Telefon Numaranız (Opsiyonel)'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Konu',
                'required': 'required'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Mesajınız...',
                'rows': 5,
                'required': 'required'
            }),
        }

    def clean_phone(self):
        """
        Telefon numarası validasyonu (basit kontrol)
        """
        phone = self.cleaned_data.get('phone')
        if phone:
            # Sadece rakamlar ve boşluk kalsın
            clean_phone = ''.join(c for c in phone if c.isdigit())
            if len(clean_phone) < 10:
                raise forms.ValidationError("Lütfen geçerli bir telefon numarası giriniz.")
        return phone
