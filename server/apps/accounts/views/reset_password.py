import datetime

from ..models.User import User

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
from datetime import timedelta

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models.VerificationToken import VerificationToken


# TODO: Fix timezone
class ResetPasswordView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        """
            Reset user password.
        """

        username = request.data.get('username')

        # Non-verified user
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if user:

            if not VerificationToken.objects.filter(user=user).exists():
                # Create verification token with 1 hour of expiration time
                token = VerificationToken.objects.create(user=user)
            else:
                token = VerificationToken.objects.get(user=user)
                token.expiration = timezone.now() + timedelta(hours=1)
                token.save()

            # Send email
            subject = 'Capstone Reservation - Reset your password'
            verify_url = "{}://{}/#/verifyReset/{}".format(settings.ROOT_PROTOCOL, settings.ROOT_URL, token)

            context = {
                'verify_url': verify_url,
                'expiration': token.expiration - datetime.timedelta(hours=4)
            }
            html_message = render_to_string('password_reset.html', context)
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

        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
