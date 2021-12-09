from django.db.models import Q
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import FundingYear, QualificationValue


def get_base_query():
    return (
        QualificationValue.objects.filter(
            is_deleted=False,
            qualification__is_deleted=False,
            qualification__awarding_body__is_deleted=False,
            funding_year=FundingYear.objects.get(year_code="2021/22"),
        )
        .prefetch_related("qualification")
        .prefetch_related("funding_year")
        .prefetch_related("qualification__awarding_body")
        .order_by(
            "qualification__qualification_category",
            "qualification__qualification_title",
            "qualification__level",
            "qualification__awarding_body__name",
        )
    )


class QualificationListView(ListView):
    model = QualificationValue
    template_name = "qualifications/qualification_list_med_info.html"

    def get_queryset(self):
        query = get_base_query()

        keywords = self.request.GET.get("keywords", "").strip()
        if keywords:
            query = query.filter(
                Q(qualification__qualification_title__icontains=keywords)
                | Q(qualification__qualification_code__icontains=keywords)
            )

        body = self.request.GET.get("body")
        if body:
            query = query.filter(qualification__awarding_body__id=body)

        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        awarding_bodies = list(
            set([qual.qualification.awarding_body for qual in get_base_query()])
        )
        awarding_bodies.sort(key=lambda body: body.name)
        context["awarding_bodies"] = awarding_bodies

        context["keywords"] = self.request.GET.get("keywords", "")

        return context


class QualificationDetailView(DetailView):
    model = QualificationValue
    template_name = "qualifications/qualification_detail.html"

    def get_queryset(self):
        return get_base_query()
