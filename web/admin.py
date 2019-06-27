# Register your models here.
from django.contrib import admin
from .models import Cofre, Transacao, Local

admin.site.register(Local)
admin.site.register(Cofre)
admin.site.register(Transacao)
