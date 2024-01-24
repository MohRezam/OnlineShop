from django.db import models
from django.db.models import Manager, QuerySet

class AppQuerySet(QuerySet):
    def delete(self):
        self.update(is_deleted=True)

        
class AppManager(Manager):
    def get_queryset(self):
        return QuerySet(self.model, using=self._db).exclude(is_deleted=True)


class BaseModel(models.Model):
    class Meta:
        abstract = True
        
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(auto_now=True, editable=False)
    
    def delete(self):
        self.is_deleted = True
        self.save()
                
    objects = AppManager()
