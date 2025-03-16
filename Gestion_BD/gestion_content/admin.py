from django.contrib import admin
from .models import *

# class title(admin.ModelAdmin):
#     list_display = ('notation_auteur','comment')
    
admin.site.register(Work)
admin.site.register(Genre)
admin.site.register(Notation)
admin.site.site_header ="Plateforme DB"
admin.site.index_title ="Auteur DB"


