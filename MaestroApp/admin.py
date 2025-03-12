from django.contrib import admin
from .models import MaestroInstrument, MaestroClass, MaestroLesson, MaestroAssignment, MaestroUser


admin.site.register(MaestroInstrument)
admin.site.register(MaestroClass)
admin.site.register(MaestroLesson)
admin.site.register(MaestroAssignment)
admin.site.register(MaestroUser)
admin.site.site_header = "Maestro Administration"
admin.site.index_title = "Admin Dashboard"