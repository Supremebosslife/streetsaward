from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        print("EmailBackend authenticate called with username:", username)
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None

        if user.check_password(password):
            print("Authentication successful for user:", user)
            return user

        print("Authentication failed for user:", user)
        return None

    def get_user(self, user_id):
        print("EmailBackend get_user called with user_id:", user_id)
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None