from django.contrib.auth.forms import UserCreationForm
from .models import Player

class PlayerForm(UserCreationForm):
    class Meta:
        model = Player
        fields = ['username', 'email', 'password1', 'password2']