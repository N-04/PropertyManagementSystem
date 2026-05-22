from django.db import models
from apps.users.models.menu import Menu
from apps.users.models.permission import Permission


class Role(models.Model):

    menus = models.ManyToManyField(
        Menu,
        blank = True
    )

    title = models.CharField(
        max_length=50,
        null = True,
        blank = True
    )

    permissions = models.ManyToManyField(
        Permission,
        blank = True
    )

    created_at = models.DateTimeField(
        auto_now_add = True
    )

    class Meta:

        db_table = 'role'

    def __str__(self):

        return self.title