from django.contrib import admin

# Register your models here.

from .models import Player, Room, Match

admin.site.register(Player)
admin.site.register(Room)
admin.site.register(Match)