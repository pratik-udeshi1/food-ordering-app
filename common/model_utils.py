from django.apps import apps

import hashlib
import random


def create_instance(model_name, **kwargs):
    model = ""
    try:
        model = apps.get_model(app_label='apps', model_name=model_name)
        instance = model.objects.create(**kwargs)
        return instance
    except model.DoesNotExist:
        return None


def get_instance(model_name, **kwargs):
    model = ""
    try:
        model = apps.get_model(app_label='apps', model_name=model_name)
        instance = model.objects.get(**kwargs)
        return instance
    except model.DoesNotExist:
        return None


def filter_instance(model_name, **kwargs):
    model = apps.get_model(app_label='apps', model_name=model_name)
    return model.objects.filter(**kwargs)


def make_secret(keyword: str):
    """
    Generate a random secret token, everytime you call it wit same keyword
    """
    return hashlib.sha256('{}-{}'.format(str(random.getrandbits(256)), keyword).encode('utf-8')).hexdigest()


def make_password(keyword: str):
    """
     convert the keyword into hashed_keyword
     - using the sha256 hash Algo
     """
    return hashlib.sha256('{}'.format(keyword).encode()).hexdigest()


def random_chars(length: int):
    """
    this will create a random characters of uppercase and digits mixed
    currently using for:
    1. creating temporary password
    2. creating product code of 7 characters
    """
    # raw_chars = [ch for ch in string.ascii_uppercase] + [num for num in string.digits]
    # random_characters = "".join(random.choices(raw_chars, k=length))
    # return random_characters
    return ''.join(random.choice('0123456789ABCDEF') for _ in range(length))
