from allauth.account.models import EmailAddress
from allauth.socialaccount.providers.base import AuthAction, ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


class EventPhoneAccount(ProviderAccount):

    def get_screen_name(self):
        name = "Unknown"
        profile = self.account.extra_data.get('profile')
        if profile is not None:
            name = profile.get('name', 'Screenname unavailable')
        return name

    def get_podio_email(self):
        name = "Unknown"
        user = self.account.extra_data.get('user')
        if user is not None:
            name = user.get('mail', 'E-mail unavailable')
        return name

    # def get_XXX_user_id(self):
    #     profile = self.account.extra_data.get('profile')
    #     if profile is not None:
    #         uid = profile.get('user_id', None)
    #         return uid
    #     return None

    def get_profile_url(self):
        ret = None
        podio_user_id = self.get_podio_user_id()
        if podio_user_id is not None:
            # TODO: exchange this
            ret = 'https://eventphone.com/users/%s' % podio_user_id
        return ret

    def get_avatar_url(self):
        ret = None
        profile_image_url = self.account.extra_data['profile']['image']['thumbnail_link']
        return profile_image_url

    def to_str(self):
        screen_name = self.get_screen_name()
        return screen_name or super(EventPhoneAccount, self).to_str()


class EventPhoneProvider(OAuth2Provider):
    id = 'eventphone'
    name = 'Eventphone'
    account_class = EventPhoneAccount

    def get_auth_url(self, request, action):
        if action == AuthAction.REAUTHENTICATE:
            url = 'https://eventphone.com/oauth/authorize'
        else:
            url = 'https://eventphone.com/oauth/authorize'
        return url

    def extract_uid(self, data):
        return data['user']['user_id']

    def extract_common_fields(self, data):
        name = data['profile']['name']
        try:
            first_name, last_name = name.split(' ', 1)
        except:
            first_name = name
            last_name = None
        return {
            'first_name': first_name,
            'last_name': last_name,
            'email': data['user']['mail']
        }

    def extract_email_addresses(self, data):
        """
        This gets the email and stores it into the users and returns an email instance.

        [EmailAddress(email='john@doe.org',
                      verified=True,
                      primary=True)]
        """
        address = data['user']['mail']
        return [EmailAddress(email=address, verified=True, primary=True)]


provider_classes = [EventPhoneProvider]

