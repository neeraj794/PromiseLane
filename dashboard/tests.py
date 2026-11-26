from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from user_profile.models import MatrimonialProfile


class BrowseMaritalStatusFilterTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.viewer = user_model.objects.create_user(username='status-filter-viewer')
        self.client.force_login(self.viewer)

        single_user = user_model.objects.create_user(username='single-profile')
        divorced_user = user_model.objects.create_user(username='divorced-profile')
        MatrimonialProfile.objects.create(
            user=single_user,
            religion='Other',
            education='University',
            occupation='Engineer',
            city='Springfield',
            state='State',
            marital_status='Single',
        )
        MatrimonialProfile.objects.create(
            user=divorced_user,
            religion='Other',
            education='University',
            occupation='Engineer',
            city='Springfield',
            state='State',
            marital_status='Divorced',
        )

    def test_browse_filter_uses_marital_status_field(self):
        response = self.client.get(reverse('browse_profiles'), {'marital_status': 'Single'})

        self.assertContains(response, 'single-profile')
        self.assertNotContains(response, 'divorced-profile')
