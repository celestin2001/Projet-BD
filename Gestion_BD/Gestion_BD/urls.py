
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('gestion_utilisateur.url')),
    path('gestion_content/',include('gestion_content.url')),
    path('i18n/',include('django.conf.urls.i18n')),
    #  path('accounts/', include('allauth.urls')),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
