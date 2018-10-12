import os

AUTHENTICATION_BACKENDS = [
    "django_python3_ldap.auth.LDAPBackend",
    "django.contrib.auth.backends.ModelBackend"
]

LDAP_AUTH_URL = 'ldaps://0.0.0.0:636'
LDAP_AUTH_USE_TLS = False

# Search
LDAP_AUTH_SEARCH_BASE = "DC=ENCS,DC=concordia,DC=ca"
LDAP_AUTH_OBJECT_CLASS = 'user'
LDAP_AUTH_USER_FIELDS = {
    "username": "uid",
    "first_name": "givenName",
    "last_name": "sn",
    "email": "userPrincipalName",
}

LDAP_AUTH_USER_LOOKUP_FIELDS = ("username", )
LDAP_AUTH_SYNC_USER_RELATIONS = "django_python3_ldap.utils.sync_user_relations"
LDAP_AUTH_FORMAT_SEARCH_FILTERS = "django_python3_ldap.utils.format_search_filters"

# Timeouts
LDAP_AUTH_CONNECT_TIMEOUT = 60
LDAP_AUTH_RECEIVE_TIMEOUT = 60

# LDAP Server Type Config
LDAP_AUTH_FORMAT_USERNAME = "django_python3_ldap.utils.format_username_active_directory_principal"
LDAP_AUTH_ACTIVE_DIRECTORY_DOMAIN = "encs.concordia.ca"

# Credentials
LDAP_AUTH_CONNECTION_USERNAME = os.environ.get('LDAP_USERNAME')
LDAP_AUTH_CONNECTION_PASSWORD = os.environ.get('LDAP_PASSWORD')

