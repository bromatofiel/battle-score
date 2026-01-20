from django.db import transaction
from user.models import User, Profile


class UserController:
    @staticmethod
    @transaction.atomic
    def create_user(email, password, pseudo, **kwargs):
        """
        Create a new user and its associated profile.
        """
        user = User.objects.create_user(
            email=email,
            password=password,
            username=email,  # Using email as username for standard AbstractUser compatibility if needed
            **kwargs,
        )

        Profile.objects.create(user=user, pseudo=pseudo)

        return user

    @staticmethod
    def delete_user(user, password):
        """
        Check password and delete the user.
        """
        if user.check_password(password):
            user.delete()
            return True
        return False
