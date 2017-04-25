import mock

from django.test import TestCase, override_settings

from transition_utilities.conditional_urls import include_if_app_enabled


class ConditionalURLTests(TestCase):

    @override_settings(
        LEGACY_APP_URLS={'core': True},
        INSTALLED_APPS=['core'],
    )
    @mock.patch('transition_utilities.conditional_urls.include')
    def test_include_if_app_enabled_calls_include(self, mock_include):
        """ Test that an app gets include()ed when all conditions are met """
        include_if_app_enabled('core', None)
        self.assertEqual(mock_include.call_count, 1)

    @override_settings(
        LEGACY_APP_URLS={'core': False},
        INSTALLED_APPS=['core'],
    )
    @mock.patch('transition_utilities.conditional_urls.wagtail_fail_through')
    def test_include_if_app_enabled_false_in_legacy_apps(
            self, mock_wagtail_fail_through):
        """ Test fail-through if LEGACY_APP_URLS[app] is False """
        result = include_if_app_enabled('core', None)
        self.assertEqual(mock_wagtail_fail_through, result)

    @override_settings(LEGACY_APP_URLS={})
    @mock.patch('transition_utilities.conditional_urls.wagtail_fail_through')
    def test_include_if_app_enabled_not_in_legacy_apps(
            self, mock_wagtail_fail_through):
        """ Test fail-through if LEGACY_APP_URLS[app] doesn't exist """
        result = include_if_app_enabled('core', None)
        self.assertEqual(mock_wagtail_fail_through, result)

    @override_settings(
        LEGACY_APP_URLS={'core': True},
        INSTALLED_APPS=[],
    )
    @mock.patch('transition_utilities.conditional_urls.wagtail_fail_through')
    def test_include_if_app_enabled_not_in_installed_apps(
            self, mock_wagtail_fail_through):
        """ Test fail-through if app isn't in INSTALLED_APPS"""
        result = include_if_app_enabled('core', None)
        self.assertEqual(mock_wagtail_fail_through, result)
