# core/backends.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.db.models import Q


class EmailOrUsernameModelBackend(ModelBackend):
    """
    Custom authentication backend that allows login with either email or username
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get('username')

        if username is None or password is None:
            return None

        try:
            # Try to find user by username or email (case insensitive)
            user = User.objects.get(
                Q(username__iexact=username) | Q(email__iexact=username)
            )

            # Check password
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

        except User.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user
            User().set_password(password)
            return None

        return None

    def get_user(self, user_id):
        """
        Get user by ID - required method for authentication backend
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None