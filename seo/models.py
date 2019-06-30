from django.db import models

# Create your models here.


class RobotsTxt(models.Model):
    text = models.TextField()

    def __str__(self):
        return 'robots.txt'

    def save(self, *args, **kwargs):
        self.pk = 1
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'robots.txt'
        verbose_name_plural = 'robots.txt'
