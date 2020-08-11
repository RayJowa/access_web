from django import forms


class DoctorForm(forms.Form):
    first_name = forms.CharField(
        max_length=20,
        error_messages={
            'required': 'Please enter name'
        }
    )
    surname = forms.CharField(
        max_length=20,
        error_messages={
            'required': 'Please enter surname'
        }
    )
    title = forms.ChoiceField(choices=(
        ('Dr', 'Dr'),
        ('Prof', 'Prof'),
        ('Mr', 'Mr'),
        ('Mrs', 'Mrs')
    ))
    # gender = forms.ChoiceField(choices=(
    #     ('male', 'Male'),
    #     ('female', "Female")
    # ))
    # date_of_birth = forms.DateField(required=False)  # TODO validate date of birth > 18, Find datepicker
    address = forms.CharField(
        max_length=100,
        error_messages={
            'required': 'Please enter your address'
        }
    )
    suburb = forms.CharField(max_length=20)
    city = forms.CharField(max_length=20)
    phone1 = forms.CharField(
        max_length=10,
        error_messages={
            'required': 'Please enter phone number'
        }
    )
    phone2 = forms.CharField(max_length=10, required=False)
    email = forms.EmailField(required=False)
