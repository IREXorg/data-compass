from django.db.models import CharField, Value
from django.utils import timezone
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin

from apps.surveys.models import Survey
from core.mixins import CSVResponseMixin, FacilitatorMixin, PageMixin

from ..models import DatasetResponse, DatasetTopicReceived, DatasetTopicShared, DatasetTopicStorageAccess


class DatasetSharedListView(SingleObjectMixin, FacilitatorMixin, PageMixin, CSVResponseMixin, ListView):
    """
    Export topic-dataset instances shared to entities.
    """

    model = DatasetTopicShared
    pk_url_kwarg = 'survey'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(
            queryset=Survey.objects.filter(project__facilitators=self.request.user)
        )
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects\
            .filter(dataset_response__response__survey=self.object)\
            .exclude(dataset_response__response__completed_at__isnull=True)\
            .select_related(
                'entity',
                'entity__hierarchy_level',
                'dataset_response',
                'dataset_response__dataset',
                'dataset_response__dataset_frequency',
                'topic',
                'dataset_response__response__respondent',
                'dataset_response__response__respondent__gender',
                'dataset_response__response__respondent__hierarchy',
                'dataset_response__response__respondent__role',
                'dataset_response__response__respondent__role__hierarchy_level',
                'dataset_response__response',
                'dataset_response__response__survey',
                'dataset_response__response__survey__project'
            )

    def get_rows(self):

        hierarchy_levels = self.object.project.hierarchy_levels.values_list('name', flat=True)

        yield [
            'id',
            'entity',
            'entity_id',
            'entity_hierarchy_level',
            'entity_hierarchy_level_id',
            'topic',
            'topic_id',
            'topic_frequency',
            'dataset',
            'dataset_id',
            'respondent_id',
            'respondent_first_name',
            'respondent_last_name',
            'respondent_email',
            'respondent_gender',
            'respondent_gender_id',
            'respondent_hierarchy_level',
            'respondent_hierarchy_level_id',
            'respondent_hierarchy',
            'respondent_hierarchy_id',
            'respondent_role',
            'respondent_role_id',
            'response_id',
            'topic_response_id',
            'response_completed_at',
            'response_consented_at',
            'survey',
            'survey_display_name',
            'survey_id',
            'project',
            'project_id',
        ] + [f'_respondent_{key}' for key in hierarchy_levels]

        for obj in self.object_list.iterator():

            respondent = obj.dataset_response.response.respondent
            respondent_hierarchy_dict = respondent.extras.get('hierarchy_dict') or respondent.build_hierarchy_dict()

            # role
            role = respondent.role
            if role:
                role_name = role.name
                role_id = role.id

                # hierarchy level
                hierarchy_level = role.hierarchy_level
                if hierarchy_level:
                    hierarchy_level_name = hierarchy_level.name
                    hierarchy_level_id = hierarchy_level.id
                else:
                    hierarchy_level_name = ''
                    hierarchy_level_id = None
            else:
                role_name = ''
                role_id = None
                hierarchy_level_name = ''
                hierarchy_level_id = None

            # hierarchy
            hierarchy = respondent.hierarchy
            if hierarchy:
                hierarchy_name = hierarchy.name
                hierarchy_id = hierarchy.id
            else:
                hierarchy_name = ''
                hierarchy_id = None

            # entity hierarchy level
            entity_hierarchy_level = obj.entity.hierarchy_level
            if entity_hierarchy_level:
                entity_hierarchy_level_name = entity_hierarchy_level.name
                entity_hierarchy_level_id = entity_hierarchy_level.id
            else:
                entity_hierarchy_level_name = ''
                entity_hierarchy_level_id = None

            yield [
                obj.id,
                obj.entity.name,
                obj.entity.id,
                entity_hierarchy_level_name,
                entity_hierarchy_level_id,
                obj.dataset_response.dataset.name,
                obj.dataset_response.dataset.id,
                obj.dataset_response.dataset_frequency.name,
                obj.topic.name,
                obj.topic.id,
                respondent.id,
                respondent.first_name,
                respondent.last_name,
                respondent.email,
                respondent.gender.name,
                respondent.gender.id,
                hierarchy_level_name,
                hierarchy_level_id,
                hierarchy_name,
                hierarchy_id,
                role_name,
                role_id,
                obj.dataset_response.response.id,
                obj.dataset_response.id,
                obj.dataset_response.response.completed_at,
                obj.dataset_response.response.consented_at,
                obj.dataset_response.response.survey.name,
                obj.dataset_response.response.survey.display_name,
                obj.dataset_response.response.survey.id,
                obj.dataset_response.response.survey.project.name,
                obj.dataset_response.response.survey.project.id,
            ] + [value for value in respondent_hierarchy_dict.values()]

    def get_filename(self):
        return f'entities-datasets-shared-to-{str(timezone.now().date())}.csv'

    def get_renderer(self):
        return 'csv'


class DatasetReceivedListView(DatasetSharedListView):
    """
    Export topic-dataset instances received from entities.
    """
    model = DatasetTopicReceived

    def get_filename(self):
        return f'entities-datasets-received-from-{str(timezone.now().date())}.csv'


class DatasetSharedReceivedListView(DatasetSharedListView):
    """
    Export topic-dataset instances shared and received from entities.
    """

    def get_queryset(self):
        select_related = [
            'entity',
            'entity__hierarchy_level',
            'dataset_response__dataset',
            'topic',
            'dataset_response__response__respondent',
            'dataset_response__response__respondent__gender',
            'dataset_response__response__respondent__hierarchy',
            'dataset_response__response__respondent__role',
            'dataset_response__response__respondent__role__hierarchy_level',
            'dataset_response__response',
            'dataset_response__response__survey',
            'dataset_response__response__survey__project'
        ]

        shared_qs = DatasetTopicShared.objects\
            .filter(dataset_response__response__survey=self.object)\
            .exclude(dataset_response__response__completed_at__isnull=True)\
            .select_related(*select_related)\
            .annotate(_type=Value('shared to', output_field=CharField()))

        received_qs = DatasetTopicReceived.objects\
            .filter(dataset_response__response__survey=self.object)\
            .exclude(dataset_response__response__completed_at__isnull=True)\
            .select_related(*select_related)\
            .annotate(_type=Value('received from', output_field=CharField()))

        return shared_qs.union(received_qs)

    def get_rows(self):
        hierarchy_levels = self.object.project.hierarchy_levels.values_list('name', flat=True)

        yield [
            'id',
            'direction',
            'entity',
            'entity_id',
            'entity_hierarchy_level',
            'entity_hierarchy_level_id',
            'topic',
            'topic_id',
            'topic_frequency',
            'dataset',
            'dataset_id',
            'respondent_id',
            'respondent_first_name',
            'respondent_last_name',
            'respondent_email',
            'respondent_gender',
            'respondent_gender_id',
            'respondent_hierarchy_level',
            'respondent_hierarchy_level_id',
            'respondent_hierarchy',
            'respondent_hierarchy_id',
            'respondent_role',
            'respondent_role_id',
            'response_id',
            'topic_response_id',
            'response_completed_at',
            'response_consented_at',
            'survey',
            'survey_display_name',
            'survey_id',
            'project',
            'project_id',
        ] + [f'_respondent_{key}' for key in hierarchy_levels]

        for obj in self.object_list.iterator():

            respondent = obj.dataset_response.response.respondent
            respondent_hierarchy_dict = respondent.extras.get('hierarchy_dict') or respondent.build_hierarchy_dict()

            # role
            role = respondent.role
            if role:
                role_name = role.name
                role_id = role.id

                # hierarchy level
                hierarchy_level = role.hierarchy_level
                if hierarchy_level:
                    hierarchy_level_name = hierarchy_level.name
                    hierarchy_level_id = hierarchy_level.id
                else:
                    hierarchy_level_name = ''
                    hierarchy_level_id = None
            else:
                role_name = ''
                role_id = None
                hierarchy_level_name = ''
                hierarchy_level_id = None

            # hierarchy
            hierarchy = respondent.hierarchy
            if hierarchy:
                hierarchy_name = hierarchy.name
                hierarchy_id = hierarchy.id
            else:
                hierarchy_name = ''
                hierarchy_id = None

            # entity hierarchy level
            entity_hierarchy_level = obj.entity.hierarchy_level
            if entity_hierarchy_level:
                entity_hierarchy_level_name = entity_hierarchy_level.name
                entity_hierarchy_level_id = entity_hierarchy_level.id
            else:
                entity_hierarchy_level_name = ''
                entity_hierarchy_level_id = None

            if respondent.gender:
                respondent_gender_name = respondent.gender.name
                respondent_gender_id = respondent.gender.id
            else:
                respondent_gender_name = ''
                respondent_gender_id = None

            yield [
                obj.id,
                obj._type,
                obj.entity.name,
                obj.entity.id,
                entity_hierarchy_level_name,
                entity_hierarchy_level_id,
                obj.dataset_response.dataset.name,
                obj.dataset_response.dataset.id,
                obj.dataset_response.dataset_frequency.name,
                obj.topic.name,
                obj.topic.id,
                respondent.id,
                respondent.first_name,
                respondent.last_name,
                respondent.email,
                respondent_gender_name,
                respondent_gender_id,
                hierarchy_level_name,
                hierarchy_level_id,
                hierarchy_name,
                hierarchy_id,
                role_name,
                role_id,
                obj.dataset_response.response.id,
                obj.dataset_response.id,
                obj.dataset_response.response.completed_at,
                obj.dataset_response.response.consented_at,
                obj.dataset_response.response.survey.name,
                obj.dataset_response.response.survey.display_name,
                obj.dataset_response.response.survey.id,
                obj.dataset_response.response.survey.project.name,
                obj.dataset_response.response.survey.project.id,
            ] + [value for value in respondent_hierarchy_dict.values()]

    def get_filename(self):
        return f'entities-datasets-shared and-received-{str(timezone.now().date())}.csv'


class DatasetStorageAccessListView(SingleObjectMixin, FacilitatorMixin, PageMixin, CSVResponseMixin, ListView):
    """
    Export topic-dataset instances storage and access.
    """

    model = DatasetTopicStorageAccess
    pk_url_kwarg = 'survey'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(
            queryset=Survey.objects.filter(project__facilitators=self.request.user)
        )
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects\
            .filter(response__dataset_response__response__survey=self.object)\
            .exclude(response__dataset_response__response__completed_at__isnull=True)\
            .select_related(
                'storage',
                'access',
                'response__dataset_response__dataset',
                'response__topic',
                'response__dataset_response__response__respondent',
                'response__dataset_response__response__respondent__gender',
                'response__dataset_response__response__respondent__hierarchy',
                'response__dataset_response__response__respondent__role',
                'response__dataset_response__response',
                'response__dataset_response__response__survey',
                'response__dataset_response__response__survey__project'
            )

    def get_rows(self):
        hierarchy_levels = self.object.project.hierarchy_levels.values_list('name', flat=True)

        yield [
            'id',
            'topic',
            'topic_id',
            'dataset',
            'dataset_id',
            'storage',
            'storage_id',
            'access',
            'access_id',
            'respondent_id',
            'respondent_first_name',
            'respondent_last_name',
            'respondent_email',
            'respondent_gender',
            'respondent_gender_id',
            'respondent_hierarchy_level',
            'respondent_hierarchy_level_id',
            'respondent_hierarchy',
            'respondent_hierarchy_id',
            'respondent_role',
            'respondent_role_id',
            'response_id',
            'topic_response_id',
            'dataset_response_id',
            'response_completed_at',
            'response_consented_at',
            'survey',
            'survey_display_name',
            'survey_id',
            'project',
            'project_id',
        ] + [f'_respondent_{key}' for key in hierarchy_levels]

        for obj in self.object_list.iterator():

            respondent = obj.response.dataset_response.response.respondent
            respondent_hierarchy_dict = respondent.extras.get('hierarchy_dict') or respondent.build_hierarchy_dict()

            # role
            role = respondent.role
            if role:
                role_name = role.name
                role_id = role.id

                # hierarchy level
                hierarchy_level = role.hierarchy_level
                if hierarchy_level:
                    hierarchy_level_name = hierarchy_level.name
                    hierarchy_level_id = hierarchy_level.id
                else:
                    hierarchy_level_name = ''
                    hierarchy_level_id = None
            else:
                role_name = ''
                role_id = None
                hierarchy_level_name = ''
                hierarchy_level_id = None

            # hierarchy
            hierarchy = respondent.hierarchy
            if hierarchy:
                hierarchy_name = hierarchy.name
                hierarchy_id = hierarchy.id
            else:
                hierarchy_name = ''
                hierarchy_id = None

            if respondent.gender:
                respondent_gender_name = respondent.gender.name
                respondent_gender_id = respondent.gender.id
            else:
                respondent_gender_name = ''
                respondent_gender_id = None

            yield [
                obj.id,
                obj.response.dataset_response.dataset.name,
                obj.response.dataset_response.dataset.id,
                obj.response.topic.name,
                obj.response.topic.id,
                obj.storage.name,
                obj.storage.id,
                obj.access.name,
                obj.access.id,
                respondent.id,
                respondent.first_name,
                respondent.last_name,
                respondent.email,
                respondent_gender_name,
                respondent_gender_id,
                hierarchy_level_name,
                hierarchy_level_id,
                hierarchy_name,
                hierarchy_id,
                role_name,
                role_id,
                obj.response.dataset_response.response.id,
                obj.response.dataset_response.id,
                obj.response.id,
                obj.response.dataset_response.response.completed_at,
                obj.response.dataset_response.response.consented_at,
                obj.response.dataset_response.response.survey.name,
                obj.response.dataset_response.response.survey.display_name,
                obj.response.dataset_response.response.survey.id,
                obj.response.dataset_response.response.survey.project.name,
                obj.response.dataset_response.response.survey.project.id,
            ] + [value for value in respondent_hierarchy_dict.values()]

    def get_filename(self):
        return f'datasets-storage-and-access-{str(timezone.now().date())}.csv'

    def get_renderer(self):
        return 'csv'


class DatasetResponseListView(SingleObjectMixin, FacilitatorMixin, PageMixin, CSVResponseMixin, ListView):
    """
    Export topic encounter frequency.
    """

    model = DatasetResponse
    pk_url_kwarg = 'survey'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(
            queryset=Survey.objects.filter(project__facilitators=self.request.user)
        )
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects\
            .filter(response__survey=self.object)\
            .exclude(response__completed_at__isnull=True)\
            .select_related(
                'dataset',
                'dataset_frequency',
                'response__respondent',
                'response__respondent__gender',
                'response__respondent__hierarchy',
                'response__respondent__role',
                'response',
                'response__survey',
                'response__survey__project'
            )

    def get_rows(self):
        hierarchy_levels = self.object.project.hierarchy_levels.values_list('name', flat=True)

        yield [
            'id',
            'topic',
            'topic_id',
            'topic_frequency',
            'topic_frequency_id',
            'respondent_id',
            'respondent_first_name',
            'respondent_last_name',
            'respondent_email',
            'respondent_gender',
            'respondent_gender_id',
            'respondent_hierarchy_level',
            'respondent_hierarchy_level_id',
            'respondent_hierarchy',
            'respondent_hierarchy_id',
            'respondent_role',
            'respondent_role_id',
            'response_id',
            'response_completed_at',
            'response_consented_at',
            'survey',
            'survey_display_name',
            'survey_id',
            'project',
            'project_id',
        ] + [f'_respondent_{key}' for key in hierarchy_levels]

        for obj in self.object_list.iterator():

            respondent = obj.response.respondent
            respondent_hierarchy_dict = respondent.extras.get('hierarchy_dict') or respondent.build_hierarchy_dict()

            # role
            role = respondent.role
            if role:
                role_name = role.name
                role_id = role.id

                # hierarchy level
                hierarchy_level = role.hierarchy_level
                if hierarchy_level:
                    hierarchy_level_name = hierarchy_level.name
                    hierarchy_level_id = hierarchy_level.id
                else:
                    hierarchy_level_name = ''
                    hierarchy_level_id = None
            else:
                role_name = ''
                role_id = None
                hierarchy_level_name = ''
                hierarchy_level_id = None

            # hierarchy
            hierarchy = respondent.hierarchy
            if hierarchy:
                hierarchy_name = hierarchy.name
                hierarchy_id = hierarchy.id
            else:
                hierarchy_name = ''
                hierarchy_id = None

            if respondent.gender:
                respondent_gender_name = respondent.gender.name
                respondent_gender_id = respondent.gender.id
            else:
                respondent_gender_name = ''
                respondent_gender_id = None

            yield [
                obj.id,
                obj.dataset.name,
                obj.dataset.id,
                obj.dataset_frequency.name,
                obj.dataset_frequency.id,
                respondent.id,
                respondent.first_name,
                respondent.last_name,
                respondent.email,
                respondent_gender_name,
                respondent_gender_id,
                hierarchy_level_name,
                hierarchy_level_id,
                hierarchy_name,
                hierarchy_id,
                role_name,
                role_id,
                obj.response.id,
                obj.response.completed_at,
                obj.response.consented_at,
                obj.response.survey.name,
                obj.response.survey.display_name,
                obj.response.survey.id,
                obj.response.survey.project.name,
                obj.response.survey.project.id,
            ] + [value for value in respondent_hierarchy_dict.values()]

    def get_filename(self):
        return f'topic-encounter-frequency-{str(timezone.now().date())}.csv'

    def get_renderer(self):
        return 'csv'
