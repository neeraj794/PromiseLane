from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import ProImage
from user_profile.models import MatrimonialProfile


class ProfilePageTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            username='profile-owner',
            password='test-password',
        )
        ProImage.objects.create(user=self.user)
        self.client.force_login(self.user)

    def test_existing_matchmaking_profile_shows_update_action(self):
        MatrimonialProfile.objects.create(
            user=self.user,
            religion='Other',
            education='University',
            occupation='Engineer',
            city='Springfield',
            state='State',
        )

        response = self.client.get(reverse('profile'))

        self.assertContains(response, 'Edit matchmaking profile')
        self.assertContains(response, reverse('update_user_profile'))
        self.assertNotContains(response, 'Complete matchmaking profile')

    def test_missing_matchmaking_profile_shows_create_action(self):
        response = self.client.get(reverse('profile'))

        self.assertContains(response, 'Complete matchmaking profile')
        self.assertContains(response, reverse('create_profile'))

    def test_profile_visibility_can_be_deactivated_and_reactivated(self):
        profile = MatrimonialProfile.objects.create(
            user=self.user,
            religion='Other',
            education='University',
            occupation='Engineer',
            city='Springfield',
            state='State',
        )

        response = self.client.get(reverse('profile'))
        self.assertContains(response, 'Your profile is active')
        self.assertContains(response, 'Deactivate profile')

        response = self.client.post(reverse('toggle_profile_visibility'))
        self.assertRedirects(response, reverse('profile'), fetch_redirect_response=False)
        profile.refresh_from_db()
        self.assertFalse(profile.is_active)

        response = self.client.get(reverse('profile'))
        self.assertContains(response, 'Your profile is hidden')
        self.assertContains(response, 'Your profile is now hidden')
        self.assertContains(response, 'Reactivate profile')

        response = self.client.post(reverse('toggle_profile_visibility'))
        self.assertRedirects(response, reverse('profile'), fetch_redirect_response=False)
        profile.refresh_from_db()
        self.assertTrue(profile.is_active)

        response = self.client.get(reverse('profile'))
        self.assertContains(response, 'Your profile is now visible')

    def test_inactive_matchmaking_profiles_are_not_browsable(self):
        user_model = get_user_model()
        active_user = user_model.objects.create_user(username='active-match')
        inactive_user = user_model.objects.create_user(username='inactive-match')
        for user, is_active in ((active_user, True), (inactive_user, False)):
            MatrimonialProfile.objects.create(
                user=user,
                religion='Other',
                education='University',
                occupation='Engineer',
                city='Springfield',
                state='State',
                is_active=is_active,
            )

        response = self.client.get(reverse('browse_profiles'))

        self.assertContains(response, 'active-match')
        self.assertNotContains(response, 'inactive-match')


class AboutPageTests(TestCase):
    def test_about_page_is_public_and_links_to_registration(self):
        response = self.client.get(reverse('about'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'A thoughtful path to connection')
        self.assertContains(response, reverse('register'))


class NavigationTests(TestCase):
    def test_anonymous_users_see_only_public_navigation_links(self):
        response = self.client.get(reverse('login'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Log In')
        self.assertContains(response, 'Register')
        self.assertContains(response, 'About')
        self.assertNotContains(response, 'My Profile')
        self.assertNotContains(response, 'Sign Out')

    def test_authenticated_users_are_redirected_from_login_to_home(self):
        user_model = get_user_model()
        user = user_model.objects.create_user(username='navigation-user', password='test-password')
        self.client.force_login(user)

        response = self.client.get(reverse('login'))

        self.assertRedirects(response, reverse('home'), fetch_redirect_response=False)

    def test_authenticated_users_see_member_links_and_about(self):
        user_model = get_user_model()
        user = user_model.objects.create_user(username='navigation-user', password='test-password')
        self.client.force_login(user)

        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'My Profile')
        self.assertContains(response, 'Sign Out')
        self.assertContains(response, 'About')
        self.assertNotContains(response, 'Log In')
        self.assertNotContains(response, 'Register')
