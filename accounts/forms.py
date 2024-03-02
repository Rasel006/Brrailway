from django.contrib.auth.models import User
from django import forms
from .models import UserBrrailwayAccount
from django.contrib.auth.forms import UserCreationForm

class UserRegistrationForm(UserCreationForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'birth_date', 'email']

    def save(self, commit=True):
        username = self.cleaned_data['username']
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        email = self.cleaned_data.get('email')
        password = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password != password2:
            raise forms.ValidationError({'Error': 'Passwords do not match'})

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError({'Error': 'username already exists'})

        our_user = super().save(commit=False)
        if commit:
            our_user.is_active = False
            our_user.save()

            birth_date = self.cleaned_data.get('birth_date')
            UserBrrailwayAccount.objects.create(
                user=our_user,
                birth_date=birth_date,
                account_no=1000 + our_user.id
            )

        return our_user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })
            
class UserUpdateForm(forms.ModelForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })
        if self.instance:
            try:
                user_account = self.instance.account
            except UserBrrailwayAccount.DoesNotExist:
                user_account = None

            if user_account:
                self.fields['birth_date'].initial = user_account.birth_date

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

            user_account, created = UserBrrailwayAccount.objects.get_or_create(user=user)
            user_account.birth_date = self.cleaned_data['birth_date']
            user_account.save()

        return user