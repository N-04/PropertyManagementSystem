from django.db import models


class Permission(models.Model):

    title = models.CharField(
        max_length=50
    )

    code = models.CharField(
        max_length=100,
        unique=True
    )

    path = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )

    method = models.CharField(
        max_length=20,
        default='GET'
    )

    class Meta:

        db_table = 'permission'

        verbose_name = '权限'

        verbose_name_plural = verbose_name

    def __str__(self):

        return self.title