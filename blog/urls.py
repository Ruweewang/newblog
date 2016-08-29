from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from myblog.upload import upload_image

urlpatterns = [

    url(r"^uploads/(?P<path>.*)$", \
                "django.views.static.serve", \
                {"document_root": settings.MEDIA_ROOT,}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('myblog.urls')),
    url(r'^admin/upload/(?P<dir_name>[^/]+)$',upload_image,name='upload_image'),

]
