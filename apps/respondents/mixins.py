from core.mixins import FacilitatorMixin


class RespondentFacilitatorMixin(FacilitatorMixin):
    """
    CBV mixin which makes sure user is a facilitator and limits respondent
    queryset to only objects where the user is among the respective
    project facilitators.
    """

    def get_queryset(self):
        """
        Returns queryset of respondents where user is among facilitators.
        """
        return self.model.objects.filter(survey__project__facilitators=self.request.user)
