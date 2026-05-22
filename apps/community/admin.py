from django.contrib import admin

from apps.community.models import House
from apps.community.models.community import Community
from apps.community.models.building import Building
from apps.community.models.unit import Unit

admin.site.register(Community)
admin.site.register(Building)
admin.site.register(Unit)
admin.site.register(House)