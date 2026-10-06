from django import forms
from django.utils import timezone

from .models import Donor


class DonorForm(forms.ModelForm):

    class Meta:

        model = Donor

        fields = [
            "name",
            "email",
            "phone",
            "date_of_birth",
            "gender",
            "blood_group",
            "address",
            "city",
            "last_donation_date",
            "is_available",
        ]

        widgets = {

            "name": forms.TextInput(
                attrs={
                    "placeholder": "Enter your full name"
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "placeholder": "Enter your email address"
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "placeholder": "Enter your phone number"
                }
            ),

            "date_of_birth": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),

            "gender": forms.Select(),

            "blood_group": forms.Select(),

            "address": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Enter your complete address"
                }
            ),

            "city": forms.TextInput(
                attrs={
                    "placeholder": "Enter your city"
                }
            ),

            "last_donation_date": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),

            "is_available": forms.CheckboxInput(),
        }

    def clean_name(self):

        name = self.cleaned_data["name"].strip()

        if len(name) < 2:
            raise forms.ValidationError(
                "Please enter a valid name."
            )

        return name

    def clean_phone(self):

        phone = self.cleaned_data["phone"].strip()

        # Keep only digits for validation
        digits = "".join(
            character for character in phone
            if character.isdigit()
        )

        if len(digits) != 10:
            raise forms.ValidationError(
                "Please enter a valid 10-digit phone number."
            )

        return digits

    def clean_date_of_birth(self):

        date_of_birth = self.cleaned_data["date_of_birth"]

        if date_of_birth > timezone.localdate():

            raise forms.ValidationError(
                "Date of birth cannot be in the future."
            )

        return date_of_birth

    def clean_last_donation_date(self):

        last_donation_date = self.cleaned_data.get(
            "last_donation_date"
        )

        if (
            last_donation_date
            and last_donation_date > timezone.localdate()
        ):

            raise forms.ValidationError(
                "Last donation date cannot be in the future."
            )

        return last_donation_date