from django.utils.deconstruct import deconstructible
import uuid
import os


@deconstructible
class HashedUploadTo(object):
    def __init__(self, path):
        self.path = path

    def __call__(self, instance, filename):
        filename_base, filename_ext = os.path.splitext(filename)
        return f"{self.path}{filename_base}-{uuid.uuid4()}{filename_ext}"
