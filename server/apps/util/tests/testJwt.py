from unittest import TestCase
from apps.accounts.models.User import User
from ..Jwt import *
from django.conf import settings


class TestJwt(TestCase):
    def setUp(self):
        self.booker = User.objects.create_user(username="f_dawigl",
                                               email="fred@email.com",
                                               password="safe_password")  # type: User
        self.booker.save()
        self.token = generate_token(self.booker)

    def tearDown(self):
        return self.booker.delete()

    def testGenerateToken(self):
        try:
            decoded = jwt.decode(self.token, os.environ.get('SECRET_KEY'))
        except jwt.ExpiredSignatureError:
            self.fail('Signature expired')
        self.assertEqual(decoded['user_id'], self.booker.id)
        self.assertEqual(decoded['iat'], decoded['exp'] - 86400)
        self.assertEqual(decoded['iss'], "{}://{}".format(settings.ROOT_PROTOCOL, settings.ROOT_URL))

    def testGetUserFromTokenSuccessful(self):
        user = get_user_from_token(self.token)
        self.assertEqual(user, self.booker)
