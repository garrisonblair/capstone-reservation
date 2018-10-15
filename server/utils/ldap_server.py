import ldap3
from django_python3_ldap import ldap
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
