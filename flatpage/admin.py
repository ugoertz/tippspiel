from django.contrib.auth.models import User
from django.contrib import admin

from hvad.admin import TranslatableAdmin

from .models import Flatpage

class FlatpageAdmin(TranslatableAdmin):
    pass
    # list_display = ('url', 'title',)
    # search_fields = ['title', ]

admin.site.register(Flatpage, FlatpageAdmin)

