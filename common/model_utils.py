from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist


def get_or_create_instance(model, create_kwargs=None, **filter_kwargs):
    if create_kwargs:
        # Create and return an instance if create_kwargs are provided
        instance, created = model.objects.get_or_create(**filter_kwargs, defaults=create_kwargs)
    else:
        try:
            instance = model.objects.get(**filter_kwargs)
        except ObjectDoesNotExist:
            instance = None

    return instance


def filter_instance(model, ordering=None, **filter_kwargs):
    instances = model.objects.filter(**filter_kwargs)
    if ordering:
        instances = instances.order_by(ordering)
    return instances


def update_instance(app_label, model_name, instance_id, update_data):
    model = apps.get_model(app_label=app_label, model_name=model_name)
    try:
        instance = model.objects.get(id=instance_id)
        for key, value in update_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
    except model.DoesNotExist:
        return None


def delete_instance(app_label, model_name, instance_id):
    model = apps.get_model(app_label=app_label, model_name=model_name)
    try:
        instance = model.objects.get(id=instance_id)
        instance.delete()
        return True
    except model.DoesNotExist:
        return False


def list_instances(app_label, model_name, **filter_kwargs):
    model = apps.get_model(app_label=app_label, model_name=model_name)
    instances = model.objects.filter(**filter_kwargs)
    return instances


def count_instances(app_label, model_name, **filter_kwargs):
    model = apps.get_model(app_label=app_label, model_name=model_name)
    count = model.objects.filter(**filter_kwargs).count()
    return count
