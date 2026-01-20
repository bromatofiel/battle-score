import datetime
from django.db import models
from django.forms.models import model_to_dict

class BaseModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def diff(self, other_model):
        """
        Returns a dict of differences between this model and another.
        """
        diff = {}
        fields = [f.name for f in self._meta.fields]
        d1 = model_to_dict(self, fields=fields)
        d2 = model_to_dict(other_model, fields=fields)
        for field in fields:
            if d1[field] != d2[field]:
                diff[field] = (d1[field], d2[field])
        return diff

    @classmethod
    def grab(cls, **kwargs):
        """
        Helper to get or return None.
        """
        try:
            return cls.objects.get(**kwargs)
        except cls.DoesNotExist:
            return None
