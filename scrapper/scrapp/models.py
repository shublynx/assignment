from django.db import models

# Create your models here.

class CollectedData(models.Model):
    data = models.JSONField()

    def __str__(self) -> str:
        return self.data[3]