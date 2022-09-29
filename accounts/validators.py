from django.core.exceptions import ValidationError


def PhoneNumberValidator(value):
	if len(str(value)) > 11:
		raise ValidationError("Phone number must have a maximum length of 11 digits")
	elif len(str(value)) < 11:
		raise ValidationError("Phone number must have a minimum length of 11 digits")
	if str(value)[0] != 0:
		raise ValidationError("Phone number must begin with a 0")