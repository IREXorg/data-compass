# Generated by Django 3.0.3 on 2020-03-22 14:58

import core.fields
from django.conf import settings
import django.contrib.postgres.fields.jsonb
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HierarchyLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='modified at')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')),
                ('name', models.CharField(max_length=128, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('creator', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_hierarchy_levels', related_query_name='created_hierarchy_level', to=settings.AUTH_USER_MODEL, verbose_name='creator')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='surveys.HierarchyLevel', verbose_name='parent')),
                ('project', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='hierarchy_levels', related_query_name='hierarchy_level', to='projects.Project', verbose_name='project')),
            ],
            options={
                'verbose_name': 'Hierarchy Level',
                'verbose_name_plural': 'Hierarchy Levels',
            },
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='modified at')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('description', models.TextField(verbose_name='description')),
                ('display_name', models.CharField(blank=True, help_text='Use this optional field to provide the survey name as Respondents will see it.', max_length=255, verbose_name='alternative name')),
                ('research_question', models.CharField(help_text='Every Data Compass survey must have a specific research question. What is yours?', max_length=255, verbose_name='research question')),
                ('languages', core.fields.ChoiceArrayField(base_field=models.CharField(choices=[('en', 'English'), ('sw', 'Swahili')], max_length=5), help_text='By default, all surveys have an English version. If your survey will be in other languages, select or add them here. You will provide translations later.', size=None, verbose_name='languages')),
                ('code', models.SlugField(allow_unicode=True, blank=True, verbose_name='code')),
                ('dont_link_hierarchy_levels', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], default=False, help_text='This can be easier in some contexts, but will limit aggregate or comparative analyses.', verbose_name='do not link respondents with system hierarchy levels')),
                ('allow_respondent_hierarchy_levels', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], default=False, help_text="Respondents will select from the List you provided for each level. If they can't find theirs, they can add their own?", verbose_name='allow respondent hierarchy levels')),
                ('login_required', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], default=True, help_text="If no, they won't be able to save and return to their responses, or view previous responses.", verbose_name='login required')),
                ('invitation_required', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], default=True, help_text='If no, anyone with the survey link can respond to it.', verbose_name='invitation required')),
                ('respondent_can_aggregate', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], default=True, help_text="'Yes', will update their networ visual with all users' responses in realtime. 'No' will not.", verbose_name='respondent can aggregate')),
                ('respondent_can_invite', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], default=True, help_text='If Yes, the survey will include question collecting email address. Respondents are responsible for ensuring consent.', verbose_name='respondent can suggest others')),
                ('allow_respondent_topics', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], default=False, help_text='If Yes, respondents will be able to add their own topics.', verbose_name='allow respondent topics')),
                ('respondent_topic_number', models.PositiveSmallIntegerField(default=10, help_text='Up to 10 topics are allowed', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)], verbose_name='respondent topic number')),
                ('allow_respondent_datasets', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], default=False, help_text='If Yes, respondents will be able to add their own datasets. This is not recommended.', verbose_name='allow respondent datasets')),
                ('allow_respondent_entities', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], default=False, help_text='If Yes, respondents will be able to add their own entities.', verbose_name='allow respondent entities')),
                ('allow_respondent_storages', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], default=False, help_text='If Yes, respondents will be able to add their own storages.', verbose_name='allow respondent storages')),
                ('introduction_text', models.TextField(default='', help_text='What text do you want to appear when a respondent begins the survey?', verbose_name='introduction text')),
                ('closing_text', models.TextField(default='', help_text='What text do you want to appear when a respondent ends the survey?', verbose_name='closing text')),
                ('is_active', models.BooleanField(blank=True, default=False, help_text='Is published', verbose_name='is active')),
                ('allow_collect_email', models.BooleanField(default=True, verbose_name='collect email address')),
                ('allow_collect_name', models.BooleanField(default=True, verbose_name='collect name')),
                ('allow_collect_gender', models.BooleanField(default=True, verbose_name='collect gender')),
                ('extras', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, verbose_name='extras')),
                ('creator', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_surveys', related_query_name='created_survey', to=settings.AUTH_USER_MODEL, verbose_name='creator')),
                ('genders', models.ManyToManyField(blank=True, related_name='surveys', related_query_name='survey', to='users.Gender', verbose_name='genders')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='surveys', related_query_name='survey', to='projects.Project', verbose_name='project')),
            ],
            options={
                'verbose_name': 'Survey',
                'verbose_name_plural': 'Surveys',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='modified at')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('extras', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, verbose_name='extras')),
                ('creator', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_survey_topics', related_query_name='created_survey_topic', to=settings.AUTH_USER_MODEL, verbose_name='creator')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topics', related_query_name='topic', to='surveys.Survey', verbose_name='survey')),
            ],
            options={
                'verbose_name': 'Dataset',
                'verbose_name_plural': 'Datasets',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='modified at')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('extras', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, verbose_name='extras')),
                ('creator', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_survey_roles', related_query_name='created_survey_role', to=settings.AUTH_USER_MODEL, verbose_name='creator')),
                ('hierarchy_level', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='roles', related_query_name='role', to='surveys.HierarchyLevel', verbose_name='hierarchy level')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roles', related_query_name='role', to='surveys.Survey', verbose_name='survey')),
            ],
            options={
                'verbose_name': 'Role',
                'verbose_name_plural': 'Roles',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='modified at')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')),
                ('name', models.SlugField(blank=True, verbose_name='field name')),
                ('label', models.CharField(help_text='this will be displayed to user', max_length=255, verbose_name='label')),
                ('type', models.CharField(choices=[('integer', 'integer'), ('decimal', 'decimal'), ('text', 'text')], max_length=50, verbose_name='type')),
                ('options', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, verbose_name='options')),
                ('creator', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_questions', related_query_name='created_question', to=settings.AUTH_USER_MODEL, verbose_name='creator')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', related_query_name='question', to='surveys.Survey', verbose_name='survey')),
            ],
            options={
                'verbose_name': 'Question',
                'verbose_name_plural': 'Questions',
                'unique_together': {('survey', 'name')},
            },
        ),
        migrations.CreateModel(
            name='Logo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='modified at')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('image', models.ImageField(blank=True, null=True, upload_to='surveys/logos', verbose_name='image')),
                ('extras', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, verbose_name='extras')),
                ('creator', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_survey_logos', related_query_name='created_survey_logo', to=settings.AUTH_USER_MODEL, verbose_name='creator')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logos', related_query_name='logo', to='surveys.Survey', verbose_name='survey')),
            ],
            options={
                'verbose_name': 'Logo',
                'verbose_name_plural': 'Logos',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='modified at')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('extras', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, verbose_name='extras')),
                ('creator', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_survey_entities', related_query_name='created_survey_entity', to=settings.AUTH_USER_MODEL, verbose_name='creator')),
                ('hierarchy_level', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='entities', related_query_name='entity', to='surveys.HierarchyLevel', verbose_name='hierarchy level')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entities', related_query_name='entity', to='surveys.Survey', verbose_name='survey')),
            ],
            options={
                'verbose_name': 'Entity',
                'verbose_name_plural': 'Entities',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='DatasetStorage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='modified at')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('extras', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, verbose_name='extras')),
                ('creator', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_survey_dataset_storages', related_query_name='created_survey_dataset_storage', to=settings.AUTH_USER_MODEL, verbose_name='creator')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dataset_storages', related_query_name='dataset_storage', to='surveys.Survey', verbose_name='survey')),
            ],
            options={
                'verbose_name': 'Dataset Storage',
                'verbose_name_plural': 'Dataset Storage',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='DatasetFrequency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='modified at')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')),
                ('name', models.CharField(max_length=255, verbose_name='frequency')),
                ('extras', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, verbose_name='extras')),
                ('creator', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_survey_dataset_frequency', related_query_name='created_survey_dataset_frequencies', to=settings.AUTH_USER_MODEL, verbose_name='creator')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dataset_frequencies', related_query_name='dataset_frequency', to='surveys.Survey', verbose_name='survey')),
            ],
            options={
                'verbose_name': 'Dataset frequency',
                'verbose_name_plural': 'Dataset Frequencies',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='DatasetAccess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='modified at')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('extras', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, verbose_name='extras')),
                ('creator', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_survey_dataset_access', related_query_name='created_survey_dataset_access', to=settings.AUTH_USER_MODEL, verbose_name='creator')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dataset_access', related_query_name='dataset_access', to='surveys.Survey', verbose_name='survey')),
            ],
            options={
                'verbose_name': 'Dataset Access',
                'verbose_name_plural': 'Dataset Access',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='modified at')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('extras', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, verbose_name='extras')),
                ('creator', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_survey_datasets', related_query_name='created_survey_dataset', to=settings.AUTH_USER_MODEL, verbose_name='creator')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='datasets', related_query_name='dataset', to='surveys.Survey', verbose_name='survey')),
                ('topics', models.ManyToManyField(blank=True, related_name='datasets', related_query_name='dataset', to='surveys.Topic', verbose_name='topics')),
            ],
            options={
                'verbose_name': 'Topic',
                'verbose_name_plural': 'Topics',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='DataflowHierarchy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='modified at')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')),
                ('level_name', models.CharField(max_length=128, verbose_name='level name')),
                ('name', models.CharField(max_length=128, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('creator', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_dataflow_hierarchy', related_query_name='created_dataflow_hierarchies', to=settings.AUTH_USER_MODEL, verbose_name='creator')),
                ('hierarchy_level', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hierarchies', related_query_name='hierarchy', to='surveys.HierarchyLevel')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='surveys.DataflowHierarchy', verbose_name='parent')),
                ('project', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='hierarchies', related_query_name='hierarchy', to='projects.Project', verbose_name='project')),
            ],
            options={
                'verbose_name': 'Dataflow Hierarchy',
                'verbose_name_plural': 'Dataflow Hierarchies',
            },
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='modified at')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')),
                ('name', models.SlugField(blank=True, verbose_name='choice value')),
                ('label', models.CharField(help_text='this will be displayed to user', max_length=255, verbose_name='label')),
                ('creator', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_survey_choices', related_query_name='created_survey_choice', to=settings.AUTH_USER_MODEL, verbose_name='creator')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choices', related_query_name='choice', to='surveys.Question', verbose_name='question')),
            ],
            options={
                'verbose_name': 'Choice',
                'verbose_name_plural': 'Choices',
            },
        ),
        migrations.CreateModel(
            name='QuestionGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='modified at')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')),
                ('name', models.CharField(blank=True, max_length=255, verbose_name='name')),
                ('group_number', models.IntegerField(blank=True, null=True, verbose_name='group number')),
                ('creator', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_question_groups', related_query_name='created_question_group', to=settings.AUTH_USER_MODEL, verbose_name='creator')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_groups', related_query_name='question_group', to='surveys.Survey', verbose_name='survey')),
            ],
            options={
                'verbose_name': 'Question Group',
                'verbose_name_plural': 'Question Groups',
                'unique_together': {('survey', 'group_number')},
            },
        ),
    ]
