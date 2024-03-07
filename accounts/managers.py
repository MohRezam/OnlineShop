from django.contrib.auth.models import BaseUserManager
from django.db.models import QuerySet


class UserManager(BaseUserManager):
    """
    Manager for the custom user model.

    This manager provides methods for creating and retrieving user objects.
    It also excludes deleted users from queryset by default.

    Methods:
        create_user(phone_number, email, first_name, last_name, password):
            Creates a new user object with the provided details.
            Args:
                phone_number (str): The phone number of the user.
                email (str): The email address of the user.
                first_name (str): The first name of the user.
                last_name (str): The last name of the user.
                password (str): The password of the user.

            Returns:
                User: The newly created user object.

        create_superuser(phone_number, email, first_name, last_name, password):
            Creates a new superuser object with the provided details.
            Args:
                phone_number (str): The phone number of the user.
                email (str): The email address of the user.
                first_name (str): The first name of the user.
                last_name (str): The last name of the user.
                password (str): The password of the user.

            Returns:
                User: The newly created superuser object.

        get_queryset():
            Returns a queryset containing all non-deleted users.

            Returns:
                QuerySet: A queryset containing non-deleted user objects.
    """
    
    def create_user(self, phone_number, email, first_name, last_name, password):
        if not phone_number:
            raise ValueError("User must have a phone number")
        
        if not email:
            raise ValueError("User must have an email")
        
        if not first_name:
            raise ValueError("User must have a first name")
        
        if not last_name:
            raise ValueError("User must have a last name")
        
        # self.model is the model User!
        user = self.model( 
            phone_number=phone_number,
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, phone_number, email, first_name, last_name, password):
        user = self.create_user(
            phone_number=phone_number,
            email=email,
            first_name=first_name,
            last_name = last_name,
            password=password,
        )
        user.is_staff = True
        user.save(using=self._db)
        return user
    
    def get_queryset(self):
        return QuerySet(self.model, using=self._db).exclude(is_deleted=True)
    