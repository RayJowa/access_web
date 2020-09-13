from django import forms

from .constants import SPECIALTIES


class DoctorForm(forms.Form):

    def __init__(self, *args, **kwargs):
        cities = kwargs.pop('cities_list')
        super(DoctorForm, self).__init__(*args, **kwargs)
        self.fields['city'] = forms.ChoiceField(choices=cities)

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
    ),
        error_messages={
            'required': 'Please select a title'
        }
    )

    gender = forms.ChoiceField(choices=(
        ('male', 'Male'),
        ('female', "Female")
    ),
        required=False
    )

    date_of_birth = forms.DateField(required=False)  # TODO validate date of birth > 18, Find datepicker
    address = forms.CharField(
        max_length=100,
        error_messages={
            'required': 'Please enter your address'
        }
    )

    suburb = forms.CharField(max_length=20)
    # city = forms.CharField(max_length=20)
    phone1 = forms.CharField(
        max_length=10,
        error_messages={
            'required': 'Please enter phone number'
        }
    )
    phone2 = forms.CharField(max_length=10, required=False)
    email = forms.EmailField(required=False)


# class SpecialistForm(forms.Form):
#
#     def __init__(self, *args, **kwargs):
#         super(SpecialistForm, self).__init__(*args, **kwargs)
#         self.fields['city'] = forms.CharField(max_length=20)
#         self.fields['suburb'] = forms.CharField(max_length=20, required=False)
#
#     first_name = forms.CharField(
#         max_length=20,
#         error_messages={
#             'required': 'Please enter name'
#         }
#     )
#
#     surname = forms.CharField(
#         max_length=20,
#         error_messages={
#             'required': 'Please enter surname'
#         }
#     )
#
#     title = forms.ChoiceField(choices=(
#         ('Dr', 'Dr'),
#         ('Prof', 'Prof'),
#         ('Mr', 'Mr'),
#         ('Mrs', 'Mrs')
#     ),
#         error_messages={
#             'required': 'Please select a title'
#         }
#     )
#
#     gender = forms.ChoiceField(choices=(
#         ('male', 'Male'),
#         ('female', "Female")
#     ),
#         required=False
#     )
#
#     date_of_birth = forms.DateField(required=False)  # TODO validate date of birth > 18, Find datepicker
#     address = forms.CharField(
#         max_length=100,
#         error_messages={
#             'required': 'Please enter your address'
#         }
#     )
#
#     # suburb = forms.CharField(max_length=20)
#     city = forms.CharField(max_length=20)
#     phone1 = forms.CharField(
#         max_length=10,
#         error_messages={
#             'required': 'Please enter phone number'
#         }
#     )
#     phone2 = forms.CharField(max_length=10, required=False)
#     email = forms.EmailField(required=False)
#
#     specialty = forms.ChoiceField(
#         choices=SPECIALTIES
#     )


class SpecialistForm(DoctorForm):

    def __init__(self, *args, **kwargs):
        super(SpecialistForm, self).__init__(*args, **kwargs)
        self.fields['suburb'] = forms.CharField(max_length=20, required=False)

    specialty = forms.ChoiceField(
        choices=SPECIALTIES,
    )


class SpecialistSearchForm(forms.Form):

    def __init__(self, *args, **kwargs):
        cities = kwargs.pop('cities_list')
        specialties = kwargs.pop('specialties_list')
        super(SpecialistSearchForm, self).__init__(*args, **kwargs)
        self.fields['city'] = forms.ChoiceField(choices=cities, required=False)
        self.fields['specialty'] = forms.ChoiceField(choices=specialties, required=False)

    surname = forms.CharField(max_length=20, required=False)


class DoctorSearchForm(forms.Form):

    def __init__(self, *args, **kwargs):
        cities = kwargs.pop('cities_list')
        super(DoctorSearchForm, self).__init__(*args, **kwargs)
        self.fields['city'] = forms.ChoiceField(choices=cities, required=True)

    surname = forms.CharField(max_length=20, required=False)
    suburb = forms.CharField(max_length=20, required=False)


class PolicySearchForm(forms.Form):
    policy_number = forms.CharField(max_length=20, required=False)
    surname = forms.CharField(max_length=20, required=False)
    id_number = forms.CharField(max_length=20, required=False)




