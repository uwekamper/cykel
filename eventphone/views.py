# -*- coding: utf-8 -*-
import json
import requests
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)

from .provider import EventPhoneProvider


class EventPhoneOAuth2Adapter(OAuth2Adapter):
    provider_id = EventPhoneProvider.id
    access_token_url = 'https://XXX.com/oauth/token'
    authorize_url = 'https://XXX.com/oauth/authorize'
    profile_url = 'https://api.XXX.com/user/status'
    supports_state = False

    def complete_login(self, request, app, token, **kwargs):
        resp = requests.get(self.profile_url,
                            headers={'Authorization': 'OAuth2 {}'.format(token.token)})
        extra_data = resp.json()
        print(json.dumps(extra_data, indent=4, sort_keys=True))
        return self.get_provider().sociallogin_from_response(request, extra_data)


oauth2_login = OAuth2LoginView.adapter_view(EventPhoneOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(EventPhoneOAuth2Adapter)

