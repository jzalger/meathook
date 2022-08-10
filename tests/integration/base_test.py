from unittest import TestCase
from meathook_web.meathook_web import meathook as app


class BaseTest(TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()
