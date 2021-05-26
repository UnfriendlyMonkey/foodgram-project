from django.contrib.auth.forms import UserCreationForm, ValidationError
from django.contrib.auth import get_user_model
from django.forms import EmailField


User = get_user_model()


class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    email = EmailField(required=True)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('User with this email already exists')
        return email
