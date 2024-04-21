from django import forms


class BootstrapForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(BootstrapForm, self).__init__(*args, **kwargs)
        for name, field in self.fields:
            if field.widget.arrts:
                self.fields[field].widget.attrs['class'] = 'form-control'
                self.fields[field].widget.attrs['placeholder'] = self.fields[field].label
            else:
                field.widget.attrs = {
                    'class': 'form-control',
                    'placeholder': field.label
                }
