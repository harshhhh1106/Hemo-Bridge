from django import forms

from .models import BloodRequest


class BloodRequestForm(forms.ModelForm):

    class Meta:
        model = BloodRequest

        fields = [
            "hospital",
            "patient_name",
            "blood_group",
            "units_required",
            "urgency",
            "reason",
        ]

        widgets = {
            "hospital": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),

            "patient_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter patient name"
                }
            ),

            "blood_group": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),

            "units_required": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "1",
                    "placeholder": "Enter number of units"
                }
            ),

            "urgency": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),

            "reason": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Enter reason for blood requirement"
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        blood_group = kwargs.pop(
            "blood_group",
            None
        )

        super().__init__(*args, **kwargs)

        if blood_group:
            self.fields["blood_group"].initial = blood_group