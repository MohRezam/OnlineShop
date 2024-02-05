from django.contrib.auth.models import BaseUserManager
from django.db.models import Manager, QuerySet


class UserManager(BaseUserManager):
    def create_user(self, phone_number, email, first_name, last_name, password, address=None):
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
            address=address,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, phone_number, email, first_name, last_name, password, address=None):
        user = self.create_user(
            phone_number=phone_number,
            email=email,
            first_name=first_name,
            last_name = last_name,
            password=password,
            address=address,
        )
        user.is_staff = True
        user.save(using=self._db)
        return user
    
    def get_queryset(self):
        return QuerySet(self.model, using=self._db).exclude(is_deleted=True)
    