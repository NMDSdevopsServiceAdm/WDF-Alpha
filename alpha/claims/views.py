from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView, TemplateView

from alpha.employees.models import Employee
from alpha.learning_providers.models import LearningProvider as LearningProviderModel
from alpha.qualifications.models import FundingYear, QualificationValue

from .forms import CandidateUlnForm, QualificationInputForm


def get_qualification(code):
    return (
        QualificationValue.objects.filter(
            is_deleted=False,
            qualification__is_deleted=False,
            qualification__awarding_body__is_deleted=False,
            funding_year=FundingYear.objects.get(year_code="2021/22"),
            qualification__qualification_code=code,
        )
        .prefetch_related("qualification")
        .prefetch_related("funding_year")
        .prefetch_related("qualification__awarding_body")
        .get()
    )


class QualificationInput(FormView):
    form_class = QualificationInputForm
    template_name = "claims/qualification_input.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["can_save_draft"] = False
        return context

    def get(self, request, *args, **kwargs):
        self.request.session.clear()
        self.request.session["individual_claims"] = {}
        self.request.session["running_total"] = 0

        self.request.session["previous_learning_provider_dropdown"] = ""
        self.request.session["previous_learning_provider_freetext"] = ""
        self.request.session["previous_apprenticeship_radio"] = None
        self.request.session["previous_claim_value_radio"] = None
        self.request.session["previous_claim_value_freetext"] = ""

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        self.request.session["claim_code"] = form.cleaned_data["claim_code"]
        qual = get_qualification(form.cleaned_data["claim_code"])
        self.request.session["qualification"] = {
            "qualification_code": qual.qualification.qualification_code,
            "qualification_title": qual.qualification.qualification_title,
            "awarding_body_name": qual.qualification.awarding_body.name_human,
            "qualification_type": qual.qualification.qualification_type2,
            "fund_value": qual.funding_value,
        }
        return redirect(reverse("qualification_summary"))

    def form_invalid(self, form):
        form.fields["claim_code"].widget.attrs["class"] += " govuk-input--error"
        context = self.get_context_data(form=form)
        return self.render_to_response(context)


class QualificationSummary(TemplateView):
    template_name = "claims/qualification_summary.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["can_save_draft"] = True
        return context

    def post(self, request, *args, **kwargs):
        return redirect(reverse("employee_input"))


class EmployeeInput(TemplateView):
    template_name = "claims/employee_input.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["can_save_draft"] = True
        context["employees"] = Employee.objects.all().order_by("name")
        return context

    def post(self, request, *args, **kwargs):
        employees = request.POST.getlist("employee")
        individual_claims = {}
        for id_ in employees:
            employee = Employee.objects.all().get(pk=int(id_))
            individual_claims[employee.id] = {
                "name": employee.name,
                "is_complete": False,
                "claim": {"value": 0},
            }
        self.request.session["individual_claims"] = individual_claims
        return redirect(reverse("claim_summary"))


class ClaimSummary(TemplateView):
    template_name = "claims/claim_summary.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["can_save_draft"] = True
        context["can_submit"] = (
            False
            not in [
                v["is_complete"]
                for k, v in self.request.session["individual_claims"].items()
            ]
            and len(self.request.session["individual_claims"]) > 0
        )
        return context

    def post(self, request, *args, **kwargs):
        return redirect(reverse("done"))


class CertDate(TemplateView):
    template_name = "claims/individual/cert_date.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["can_save_draft"] = True
        context["current_individual_claim"] = self.request.session["individual_claims"][
            self.kwargs["id"]
        ]
        return context

    def post(self, request, *args, **kwargs):
        id_ = kwargs["id"]
        date = f"""{
            request.POST.get('certificate-issued-day')
        }/{
            request.POST.get('certificate-issued-month')
        }/{
            request.POST.get('certificate-issued-year')
        }"""
        self.request.session["individual_claims"][id_]["cert_date"] = date
        return redirect(reverse("candidate_uln", kwargs={"id": id_}))


class CandidateUln(FormView):
    template_name = "claims/individual/candidate_uln.html"
    form_class = CandidateUlnForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["can_save_draft"] = True
        context["current_individual_claim"] = self.request.session["individual_claims"][
            self.kwargs["id"]
        ]
        return context

    def form_valid(self, form):
        id_ = self.kwargs["id"]
        self.request.session["individual_claims"][id_][
            "candidate_uln"
        ] = form.cleaned_data["candidate_uln"]
        self.request.session["individual_claims"][id_][
            "candidate_reg_no"
        ] = form.cleaned_data["candidate_reg_no"]
        return redirect(reverse("cert_upload", kwargs={"id": id_}))

    def form_invalid(self, form):
        form.fields["candidate_uln"].widget.attrs["class"] += " govuk-input--error"
        context = self.get_context_data(form=form)
        return self.render_to_response(context)


class CertUpload(TemplateView):
    template_name = "claims/individual/cert_upload.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["can_save_draft"] = True
        context["current_individual_claim"] = self.request.session["individual_claims"][
            self.kwargs["id"]
        ]
        return context

    def post(self, request, *args, **kwargs):
        id_ = kwargs["id"]
        self.request.session["individual_claims"][id_]["cert_file"] = request.POST.get(
            "cert-upload"
        )
        return redirect(reverse("learning_provider", kwargs={"id": id_}))


class LearningProvider(TemplateView):
    template_name = "claims/individual/learning_provider.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["can_save_draft"] = True
        context["current_individual_claim"] = self.request.session["individual_claims"][
            self.kwargs["id"]
        ]
        context["learning_providers"] = LearningProviderModel.objects.all().order_by(
            "provider"
        )
        return context

    def post(self, request, *args, **kwargs):
        id_ = kwargs["id"]
        if request.POST.get("learning-provider") == "n/a":
            self.request.session["individual_claims"][id_][
                "learning_provider"
            ] = request.POST.get("other-learning-provider", "")
        else:
            self.request.session["individual_claims"][id_][
                "learning_provider"
            ] = LearningProviderModel.objects.get(
                pk=int(request.POST.get("learning-provider"))
            ).provider
        self.request.session["previous_learning_provider_dropdown"] = request.POST.get(
            "learning-provider", ""
        )
        self.request.session["previous_learning_provider_freetext"] = request.POST.get(
            "other-learning-provider", ""
        )
        return redirect(reverse("apprenticeship", kwargs={"id": id_}))


class Apprenticeship(TemplateView):
    template_name = "claims/individual/apprenticeship.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["can_save_draft"] = True
        context["current_individual_claim"] = self.request.session["individual_claims"][
            self.kwargs["id"]
        ]
        return context

    def post(self, request, *args, **kwargs):
        id_ = kwargs["id"]
        apprenticeship = bool(request.POST.get("apprenticeship") == "yes")
        self.request.session["previous_apprenticeship_radio"] = apprenticeship
        self.request.session["individual_claims"][id_][
            "apprenticeship"
        ] = apprenticeship
        return redirect(reverse("claim_value", kwargs={"id": id_}))


class ClaimValue(TemplateView):
    template_name = "claims/individual/claim_value.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["can_save_draft"] = True
        context["current_individual_claim"] = self.request.session["individual_claims"][
            self.kwargs["id"]
        ]
        return context

    def post(self, request, *args, **kwargs):
        id_ = kwargs["id"]

        self.request.session["individual_claims"][id_]["claim"] = {}
        full_value = request.POST.get("claim-full-value") == "yes"
        self.request.session["individual_claims"][id_]["claim"][
            "full_value"
        ] = full_value
        self.request.session["previous_claim_value_radio"] = full_value
        if full_value:
            self.request.session["individual_claims"][id_]["claim"][
                "value"
            ] = self.request.session["qualification"]["fund_value"]
            self.request.session["previous_claim_value_freetext"] = ""
        else:
            claim_value = request.POST.get("claim-value")
            self.request.session["individual_claims"][id_]["claim"]["value"] = int(
                claim_value if claim_value else 0
            )
            self.request.session["previous_claim_value_freetext"] = claim_value

        self.request.session["running_total"] = sum(
            [
                v["claim"]["value"]
                for k, v in self.request.session["individual_claims"].items()
            ]
        )
        self.request.session["individual_claims"][id_]["is_complete"] = True
        return redirect(reverse("claim_summary"))
