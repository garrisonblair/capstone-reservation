import datetime
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.ldap_server import get_ldap_connection
from apps.accounts.serializers.UserSerializer import UserSerializerLogin
from apps.accounts.models.VerificationToken import VerificationToken


# TODO: Fix timezone
class RegisterView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        """
            Register new user.
        """

        username = request.data.get('username')
        user = None

        # Non-verified user
        User = get_user_model()
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            pass

        if user and not user.is_active:
            print("Non-verified user")
            return Response(status=status.HTTP_302_FOUND)

        # New user from LDAP
        connection = get_ldap_connection()
        user = connection.get_user(username=username)

        if user:
            print("New LDAP user")
            user.is_active = False
            user.save()

            # Create verification token with 1 hour of expiration time
            token = VerificationToken.objects.create(user=user)

            # Send email
            subject = 'Capstone Reservation - Verify your email!'
            verify_url = "{}://{}/#/verify?token={}".format(settings.ROOT_PROTOCOL, settings.ROOT_URL, token)
            context = {
                'verify_url': verify_url,
                'expiration': token.expiration - datetime.timedelta(hours=4)
            }
            html_message = render_to_string('email.html', context)
            plain_message = strip_tags(html_message)

            send_mail(
                subject,
                plain_message,
                settings.EMAIL_HOST_USER,
                [user.email],
                html_message=html_message,
                fail_silently=False,
            )

            return Response(status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)
