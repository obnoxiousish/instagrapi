import logging
from urllib.parse import urlparse

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from instagrapi.instagrapi.mixins.account import AccountMixin
from instagrapi.instagrapi.mixins.album import DownloadAlbumMixin, UploadAlbumMixin
from instagrapi.instagrapi.mixins.auth import LoginMixin
from instagrapi.instagrapi.mixins.bloks import BloksMixin
from instagrapi.instagrapi.mixins.challenge import ChallengeResolveMixin
from instagrapi.instagrapi.mixins.clip import DownloadClipMixin, UploadClipMixin
from instagrapi.instagrapi.mixins.collection import CollectionMixin
from instagrapi.instagrapi.mixins.comment import CommentMixin
from instagrapi.instagrapi.mixins.direct import DirectMixin
from instagrapi.instagrapi.mixins.explore import ExploreMixin
from instagrapi.instagrapi.mixins.fbsearch import FbSearchMixin
from instagrapi.instagrapi.mixins.fundraiser import FundraiserMixin
from instagrapi.instagrapi.mixins.hashtag import HashtagMixin
from instagrapi.instagrapi.mixins.highlight import HighlightMixin
from instagrapi.instagrapi.mixins.igtv import DownloadIGTVMixin, UploadIGTVMixin
from instagrapi.instagrapi.mixins.insights import InsightsMixin
from instagrapi.instagrapi.mixins.location import LocationMixin
from instagrapi.instagrapi.mixins.media import MediaMixin
from instagrapi.instagrapi.mixins.multiple_accounts import MultipleAccountsMixin
from instagrapi.instagrapi.mixins.note import NoteMixin
from instagrapi.instagrapi.mixins.notification import NotificationMixin
from instagrapi.instagrapi.mixins.password import PasswordMixin
from instagrapi.instagrapi.mixins.photo import DownloadPhotoMixin, UploadPhotoMixin
from instagrapi.instagrapi.mixins.private import PrivateRequestMixin
from instagrapi.instagrapi.mixins.public import (
    ProfilePublicMixin,
    PublicRequestMixin,
    TopSearchesPublicMixin,
)
from instagrapi.instagrapi.mixins.share import ShareMixin
from instagrapi.instagrapi.mixins.signup import SignUpMixin
from instagrapi.instagrapi.mixins.story import StoryMixin
from instagrapi.instagrapi.mixins.timeline import ReelsMixin
from instagrapi.instagrapi.mixins.totp import TOTPMixin
from instagrapi.instagrapi.mixins.track import TrackMixin
from instagrapi.instagrapi.mixins.user import UserMixin
from instagrapi.instagrapi.mixins.video import DownloadVideoMixin, UploadVideoMixin

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Used as fallback logger if another is not provided.
DEFAULT_LOGGER = logging.getLogger("instagrapi")


class Client(
    PublicRequestMixin,
    ChallengeResolveMixin,
    PrivateRequestMixin,
    TopSearchesPublicMixin,
    ProfilePublicMixin,
    LoginMixin,
    ShareMixin,
    TrackMixin,
    FbSearchMixin,
    HighlightMixin,
    DownloadPhotoMixin,
    UploadPhotoMixin,
    DownloadVideoMixin,
    UploadVideoMixin,
    DownloadAlbumMixin,
    NotificationMixin,
    UploadAlbumMixin,
    DownloadIGTVMixin,
    UploadIGTVMixin,
    MediaMixin,
    UserMixin,
    InsightsMixin,
    CollectionMixin,
    AccountMixin,
    DirectMixin,
    LocationMixin,
    HashtagMixin,
    CommentMixin,
    StoryMixin,
    PasswordMixin,
    SignUpMixin,
    DownloadClipMixin,
    UploadClipMixin,
    ReelsMixin,
    ExploreMixin,
    BloksMixin,
    TOTPMixin,
    MultipleAccountsMixin,
    NoteMixin,
    FundraiserMixin,
):
    proxy = None

    def __init__(
        self,
        settings: dict = {},
        proxy: str = None,
        delay_range: list = None,
        logger=DEFAULT_LOGGER,
        **kwargs,
    ):

        super().__init__(**kwargs)

        self.settings = settings
        self.logger = logger
        self.delay_range = delay_range

        self.set_proxy(proxy)

        self.init()

    def set_proxy(self, dsn: str):
        if dsn:
            assert isinstance(
                dsn, str
            ), f'Proxy must been string (URL), but now "{dsn}" ({type(dsn)})'
            self.proxy = dsn
            proxy_href = "{scheme}{href}".format(
                scheme="http://" if not urlparse(self.proxy).scheme else "",
                href=self.proxy,
            )
            self.public.proxies = self.private.proxies = {
                "http": proxy_href,
                "https": proxy_href,
            }
            return True
        self.public.proxies = self.private.proxies = {}
        return False
