from django.contrib.auth.forms import UserCreationForm as BaseForm
from .models import User


class UserCreationForm(BaseForm):
	class Meta:
		model = User
		fields = [
			"email",
			"username",
			"password1",
			"password2"
		]