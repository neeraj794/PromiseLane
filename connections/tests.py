from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import PartnerPreFerences
from user_profile.models import MatrimonialProfile


class MatchesViewTests(TestCase):
    def test_matches_view_filters_profiles_by_user_date_of_birth(self):
        user_model = get_user_model()
        current_user = user_model.objects.create_user(
            username='current-user',
            dob='1990-01-01',
        )
        matched_user = user_model.objects.create_user(
            username='matched-user',
            first_name='Matched',
            dob='1995-01-01',
        )
        MatrimonialProfile.objects.create(
            user=matched_user,
            religion='Other',
            education='University',
            occupation='Engineer',
            city='Springfield',
            state='State',
        )
        PartnerPreFerences.objects.create(user=current_user)
        self.client.force_login(current_user)

        response = self.client.get(reverse('matches'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Matched')
