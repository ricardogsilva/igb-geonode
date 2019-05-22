import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site

from allauth.socialaccount.models import SocialApp


class Command(BaseCommand):
    help = "Setup login via social providers"

    @staticmethod
    def _get_client_id_arg(provider):
        return "{}-client-id".format(provider)

    @staticmethod
    def _get_client_secret_arg(provider):
        return "{}-secret-key".format(provider)

    @staticmethod
    def _get_client_id_env(provider):
        return "{}_OAUTH2_CLIENT_ID".format(provider.upper())

    @staticmethod
    def _get_client_secret_env(provider):
        return "{}_OAUTH2_SECRET_KEY".format(provider.upper())

    @staticmethod
    def get_social_providers():
        providers = []
        for app_info in settings.INSTALLED_APPS:
            if isinstance(app_info, basestring):
                if app_info.startswith("allauth.socialaccount.providers"):
                    provider_module = app_info.rpartition(".")[-1]
                    provider_name = provider_module.partition("_")[0]
                    providers.append((provider_name, provider_module))
        return providers

    def add_arguments(self, parser):
        for provider_name, provider_id in self.get_social_providers():
            client_id_arg = self._get_client_id_arg(provider_name)
            parser.add_argument(
                "--{}".format(client_id_arg),
                help=(
                    "Specify the client id for {}. You may also specify "
                    "the {} environment variable instead".format(
                        provider_name,
                        self._get_client_id_env(provider_name)
                    )
                )
            )
            client_secret_arg = self._get_client_secret_arg(provider_name)
            parser.add_argument(
                "--{}".format(client_secret_arg),
                help=(
                    "Specify the secret key for {}. You may also specify "
                    "the {} environment variable instead".format(
                        provider_name,
                        self._get_client_secret_env(provider_name)
                    )
                )
            )

    def handle(self, *args, **options):
        for provider_name, provider_id in self.get_social_providers():
            client_id_arg = self._get_client_id_arg(
                provider_name).replace("-", "_")
            client_secret_arg = self._get_client_secret_arg(
                provider_name).replace("-", "_")
            client_id = (
                options.get(client_id_arg) or
                os.getenv(self._get_client_id_env(provider_name))
            )
            client_secret = (
                options.get(client_secret_arg) or
                os.getenv(self._get_client_secret_env(provider_name))
            )
            if all((client_id, client_secret)):
                self.stdout.write(
                    "Configuring provider {}...".format(provider_name))
                self._handle_provider(
                    provider_name, provider_id, client_id, client_secret)
            else:
                self.stdout.write(
                    "Provider {} not all params were specified, "
                    "skipping...".format(provider_name)
                )

    def _handle_provider(self, name, id_, client_id, secret_key):
        provider, created = SocialApp.objects.get_or_create(
            name=name.lower(),
            client_id=client_id,
            secret=secret_key,
            provider=id_
        )
        if created:
            # associate with the first site
            provider.sites.add(Site.objects.get_current())
            provider.save()
        else:
            self.stdout.write(
                "Provider {} already exists, skipping...".format(name))
