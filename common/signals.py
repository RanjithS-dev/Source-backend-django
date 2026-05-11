from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.forms.models import model_to_dict
from .firebase_utils import sync_to_firestore, delete_from_firestore
from .models import BaseModel

def get_syncable_models():
    from django.apps import apps
    return [m for m in apps.get_models() if issubclass(m, BaseModel)]

@receiver(post_save)
def firebase_sync_post_save(sender, instance, created, **kwargs):
    # Only sync models that inherit from BaseModel
    if not isinstance(instance, BaseModel):
        return
        
    collection_name = sender._meta.model_name + "s" # e.g. employee -> employees
    data = model_to_dict(instance)
    
    # Handle datetime serialization
    for key, value in data.items():
        if hasattr(value, 'isoformat'):
            data[key] = value.isoformat()
            
    sync_to_firestore(collection_name, instance.id, data)

@receiver(post_delete)
def firebase_sync_post_delete(sender, instance, **kwargs):
    if not isinstance(instance, BaseModel):
        return
        
    collection_name = sender._meta.model_name + "s"
    delete_from_firestore(collection_name, instance.id)
