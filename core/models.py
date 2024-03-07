from django.db import models
from django.db.models import Manager, QuerySet
from django.utils import timezone

class AppQuerySet(QuerySet):
    def delete(self):
        self.update(is_deleted=True, deleted_at=timezone.now())

        
class AppManager(Manager):
    def get_queryset(self):
        return QuerySet(self.model, using=self._db).exclude(is_deleted=True)


class BaseModel(models.Model):
    """
    Abstract base model for database tables.

    This model provides common fields and methods for other models to inherit.
    It includes fields for tracking creation and update times, and soft deletion.

    Attributes:
        created_at (DateTimeField): The date and time when the record was created.
        updated_at (DateTimeField): The date and time when the record was last updated.
        is_deleted (bool): Indicates if the record is soft deleted.
        deleted_at (DateTimeField): The date and time when the record was deleted.

    Methods:
        delete():
            Soft deletes the record by setting is_deleted to True and updating deleted_at.

    Meta:
        abstract (bool): Indicates that this model is abstract and should not create a table.

    Manager:
        objects (AppManager): Custom manager for filtering out soft deleted records.
    """
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, default=None, editable=False)
    
    # def delete(self):
    """
         Soft deletes the record by setting is_deleted to True and updating deleted_at.
        """
    #     self.is_deleted = True
    #     self.deleted_at = timezone.now()
    #     self.save()
    
    class Meta:
        abstract = True
                
    objects = AppManager()
