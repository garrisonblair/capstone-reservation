import ldap3
from django_python3_ldap import ldap
from django_python3_ldap import utils
from django_python3_ldap.conf import settings


def get_ldap_connection():
    """
        Get LDAP server connection.

        Returns:
            Connection instance.
    """

    if settings.LDAP_AUTH_USE_TLS:
        auto_bind = ldap3.AUTO_BIND_TLS_BEFORE_BIND
    else:
        auto_bind = ldap3.AUTO_BIND_NO_TLS

    try:
        server = ldap3.Server(
            settings.LDAP_AUTH_URL,
            allowed_referral_hosts=[("*", True)],
            get_info=ldap3.NONE,
            connect_timeout=settings.LDAP_AUTH_CONNECT_TIMEOUT,
        ),

        connection = ldap3.Connection(
            server,
            user=settings.LDAP_AUTH_CONNECTION_USERNAME,
            password=settings.LDAP_AUTH_CONNECTION_PASSWORD,
            auto_bind=auto_bind,
            raise_exceptions=True,
            receive_timeout=settings.LDAP_AUTH_RECEIVE_TIMEOUT,
        )
        return ldap.Connection(connection)
    except Exception as ex:
        print("LDAP connect failed: {ex}".format(ex=ex))

    return None


def get_user(**kwargs):
    """
    Returns the user with the given identifier.

    The user identifier should be keyword arguments matching the fields
    in settings.LDAP_AUTH_USER_LOOKUP_FIELDS.
    """
    connection = get_ldap_connection()
    if connection._connection.search(
            search_base=settings.LDAP_AUTH_SEARCH_BASE,
            search_filter=utils.format_search_filter(kwargs),
            search_scope=ldap3.SUBTREE,
            attributes=ldap3.ALL_ATTRIBUTES,
            get_operational_attributes=True,
            size_limit=5,
    ):

        for response in connection._connection.response:
            if response["attributes"]["name"][0] == kwargs["username"]:
                return connection._get_or_create_user(response)
    return None


def search_user(**kwargs):
    connection = get_ldap_connection()
    if connection._connection.search(
        search_base=settings.LDAP_AUTH_SEARCH_BASE,
        search_filter=ldap.format_search_filter(kwargs),
        search_scope=ldap3.SUBTREE,
        attributes=ldap3.ALL_ATTRIBUTES,
        get_operational_attributes=True,
        size_limit=1
    ):

        for response in connection._connection.response:
            if response["attributes"]["name"][0] == kwargs["username"]:
                return response
    return None


def get_user_groups(**kwargs):
    response = search_user(**kwargs)
    if response:
        return response.get('attributes').get('memberOf')
    return None
