from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is not None:
            username = username.strip()  # Remove leading/trailing whitespace
        else:
            print("Username is None")  # Debug
            return None
        
        try:
            user = UserModel.objects.get(stud_no=username)  # Fetch user by stud_no
            print(f"User found: {user}")  # Debug
        except UserModel.DoesNotExist:
            print(f"No user found with stud_no: {username}")  # Debug
            return None
        else:
            if user.check_password(password):  # Validate password
                print("Password is correct")  # Debug
                return user
            else:
                print("Password is incorrect")  # Debug
        return None