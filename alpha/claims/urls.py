from django.urls import path
from django.views.generic import TemplateView

from alpha.claims import views

urlpatterns = [
    path(
        "qualification_input/",
        views.QualificationInput.as_view(),
        name="qualification_input",
    ),
    path(
        "qualification_summary/",
        views.QualificationSummary.as_view(),
        name="qualification_summary",
    ),
    path(
        "employee_input/",
        views.EmployeeInput.as_view(),
        name="employee_input",
    ),
    path(
        "claim_summary/",
        views.ClaimSummary.as_view(),
        name="claim_summary",
    ),
    path(
        "cert_date/<id>",
        views.CertDate.as_view(),
        name="cert_date",
    ),
    path(
        "candidate_uln/<id>",
        views.CandidateUln.as_view(),
        name="candidate_uln",
    ),
    path(
        "cert_upload/<id>",
        views.CertUpload.as_view(),
        name="cert_upload",
    ),
    path(
        "learning_provider/<id>",
        views.LearningProvider.as_view(),
        name="learning_provider",
    ),
    path(
        "apprenticeship/<id>",
        views.Apprenticeship.as_view(),
        name="apprenticeship",
    ),
    path(
        "claim_value/<id>",
        views.ClaimValue.as_view(),
        name="claim_value",
    ),
    path("done/", TemplateView.as_view(template_name="claims/done.html"), name="done"),
]
