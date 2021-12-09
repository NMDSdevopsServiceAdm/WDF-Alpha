from django.urls import path
from django.views.generic import TemplateView

from alpha.qualifications import views

urlpatterns = [
    path("med/", views.QualificationListView.as_view(), name="qualification_list"),
    path(
        "low/",
        views.QualificationListView.as_view(
            template_name="qualifications/qualification_list_low_info.html"
        ),
        name="qualification_list_low_info",
    ),
    path(
        "high/",
        views.QualificationListView.as_view(
            template_name="qualifications/qualification_list_high_info.html"
        ),
        name="qualification_list_high_info",
    ),
    path(
        "scratchpad/",
        TemplateView.as_view(template_name="qualifications/scratchpad.html"),
    ),
    path("<pk>/", views.QualificationDetailView.as_view(), name="qualification_detail"),
]
