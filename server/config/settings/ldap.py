import os

AUTHENTICATION_BACKENDS = [
    "django_python3_ldap.auth.LDAPBackend",
    "django.contrib.auth.backends.ModelBackend"
]

LDAP_AUTH_URL = 'ldaps://faith.encs.concordia.ca'

# Search
LDAP_AUTH_SEARCH_BASE = "DC=ENCS,DC=concordia,DC=ca,OU=_encs,OU=_accounts,OU=_users"
LDAP_AUTH_OBJECT_CLASS = "user"
LDAP_AUTH_USER_FIELDS = {
    "username": "uid",
    "first_name": "givenName",
    "last_name": "sn",
    "email": "userPrincipalName",
}

LDAP_AUTH_CONNECTION_USERNAME = os.getenv('LDAP_USERNAME')
LDAP_AUTH_CONNECTION_PASSWORD = os.getenv('LDAP_PASSWORD')
