from django import forms
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe


class QualificationInputForm(forms.Form):
    claim_code = forms.CharField(
        label="",
        initial="",
        widget=forms.TextInput(
            attrs={
                "class": "govuk-input govuk-input--width-20",
                "aria-describedby": "claim-code-hint",
            }
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data["claim_code"] != "603/3496/4":
            raise ValidationError("invalid")
        return cleaned_data


class CandidateUlnForm(forms.Form):
    candidate_uln = forms.CharField(
        label="",
        initial="2000000001",
        widget=forms.TextInput(
            attrs={
                "class": "govuk-input govuk-input--width-20",
            }
        ),
    )
    candidate_reg_no = forms.CharField(
        label="",
        initial="P010001A",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "govuk-input govuk-input--width-20",
                "aria-describedby": "candidate-reg-no-hint",
            }
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        if (
            len(cleaned_data["candidate_uln"]) == 10
            and cleaned_data["candidate_uln"][0] == "2"
        ):
            # accept and move on to the next step
            pass
        elif cleaned_data["candidate_uln"] == "1000000001":
            raise ValidationError(
                mark_safe(
                    """The ULN must match the learner you are claiming for
                    <div id="claim-code-hint" class="govuk-hint">
                    The ULN entered does not match the name of the learner you’re adding details for.
                    </div>"""
                )
            )
        elif cleaned_data["candidate_uln"] == "1000000002":
            raise ValidationError(
                mark_safe(
                    """The ULN must match the exact name of the learner you are claiming for
                    <div id="claim-code-hint" class="govuk-hint">
                    The ULN entered matches a similar name in the Learner Records Service (LRS)
                    to the selected candidate.
                    Amend the name on your claim before submitting or check and update the candidate’s LRS record.
                    LRS records are usually managed by your Learning Provider.
                    </div>"""
                )
            )
        else:
            raise ValidationError(
                mark_safe(
                    """The ULN must match a learner record
                    <div id="claim-code-hint" class="govuk-hint">
                    The ULN you entered does not match any learner records. Enter the correct ULN.
                    </div>"""
                )
            )
        return cleaned_data
