from django.contrib import admin
from .models import CollectedData

# Register your models here.


class CollectedDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'data')  
    list_filter = ('id','data',)     
    search_fields = ('id', 'data',)  

admin.site.register(CollectedData,CollectedDataAdmin)