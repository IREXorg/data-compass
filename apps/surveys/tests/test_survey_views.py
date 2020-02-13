from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase

# from .models import Survey


class SurveyViewTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = AnonymousUser()

    def test_list_view(self):
        """
        Test that we can list instances via the list view.
        """
        pass

    def test_create_view(self):
        """
        Test that we can create an instance via the create view.
        """
        pass

    def test_detail_view(self):
        """
        Test that we can view an instance via the detail view.
        """
        pass

    def test_update_view(self):
        """
        Test that we can update an instance via the update view.
        """
        pass

    def test_delete_view(self):
        """
        Test that we can delete an instance via the delete view.
        """
        pass
