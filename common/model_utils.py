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


def update_instance(model, instance_id, update_data):
    try:
        instance = model.objects.get(id=instance_id)
        for key, value in update_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
    except model.DoesNotExist:
        return None


def delete_instance(model, instance_id):
    try:
        instance = model.objects.get(id=instance_id)
        instance.delete()
        return True
    except model.DoesNotExist:
        return False


def list_instances(model, **filter_kwargs):
    instances = model.objects.filter(**filter_kwargs)
    return instances


def count_instances(model, **filter_kwargs):
    count = model.objects.filter(**filter_kwargs).count()
    return count
