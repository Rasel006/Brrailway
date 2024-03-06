from django import forms
from .models import Train, UserReviews,TrainPurchase

class TrainForm(forms.ModelForm):
    class Meta:
        model = Train
        fields = '__all__'

STAR_CHOICES = [
    ('⭐', '⭐'),
    ('⭐⭐', '⭐⭐'),
    ('⭐⭐⭐', '⭐⭐⭐'),
    ('⭐⭐⭐⭐', '⭐⭐⭐⭐'),
    ('⭐⭐⭐⭐⭐', '⭐⭐⭐⭐⭐'),
]  
class ReviewForm(forms.ModelForm):
    class Meta:
        model = UserReviews
        fields = ['rating', 'body']
        widgets = {
            'rating': forms.Select(choices=STAR_CHOICES),
            'body': forms.Textarea(attrs={'rows': 4}),
        }
        
    def __init__(self, *args, **kwargs):
        self.train = kwargs.pop('train', None)
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        user_purchased_or_borrowed = TrainPurchase.objects.filter(user=self.user, train=self.train).exists()

        if not user_purchased_or_borrowed:
            raise forms.ValidationError("You must purchase the Ticket to leave a review.")

        return cleaned_data

class ReviewUpdateForm(forms.ModelForm):
    class Meta:
        model = UserReviews
        fields = ['rating', 'body']