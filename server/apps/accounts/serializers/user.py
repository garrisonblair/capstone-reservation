from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from apps.accounts.models.BookerProfile import BookerProfile
from apps.accounts.serializers.privilege_category import PrivilegeCategorySerializer


class UserSerializer(serializers.ModelSerializer):

    booker_profile = serializers.SerializerMethodField()

    def get_booker_profile(self, user):
        return BookerProfileSerializer(user.bookerprofile).data

    class Meta:
        model = User
        fields = ('id',
                  'username',
                  'first_name',
                  'last_name',
                  'email',
                  'booker_profile',
                  'is_superuser',
                  'is_staff',
                  'is_active')


class UserSerializerLogin(UserSerializer):

    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id',
                  'username',
                  'first_name',
                  'last_name',
                  'email',
                  'is_superuser',
                  'is_staff',
                  'is_active',
                  'token')

    def get_token(self, user):
        """
            Get or create token
        """

        token, created = Token.objects.get_or_create(user=user)
        return token.key


class PublicUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id',
                  'username',
                  'first_name',
                  'last_name')


class BookerProfileSerializer(serializers.ModelSerializer):
    privilege_categories = PrivilegeCategorySerializer(many=True)

    class Meta:
        model = BookerProfile
        fields = ('id', 'booker_id', 'secondary_email', 'privilege_categories', 'program', 'graduate_level')
