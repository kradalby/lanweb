from django.contrib import admin
from models import Application, Crew, CrewTeam

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['user']
    def save_model(self, request, obj, form, change): 
        if not change:
            obj.user = request.user
        obj.save()

class CrewAdmin(admin.ModelAdmin):
    list_display = ['name']


class CrewTeamAdmin(admin.ModelAdmin):
    list_display = ['name','crew']

admin.site.register(Application, ApplicationAdmin)
admin.site.register(Crew, CrewAdmin)
admin.site.register(CrewTeam, CrewTeamAdmin)
