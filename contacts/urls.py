from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    #call for login authentication
    path('',include('django.contrib.auth.urls')), 

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

#Customizing admin texts

admin.site.site_header= 'Contact'
admin.site.index_title ='Welcome to project'
admin.site.site_title = 'Control Panel'