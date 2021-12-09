from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("claims/", include("alpha.claims.urls")),
    path("qualifications/", include("alpha.qualifications.urls")),
    path("", TemplateView.as_view(template_name="home.html")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
