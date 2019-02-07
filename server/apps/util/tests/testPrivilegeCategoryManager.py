from django.test import TestCase
from apps.accounts.models.User import User
from apps.accounts.models.PrivilegeCategory import PrivilegeCategory
from apps.util.PrivilegeCategoryManager import PrivilegeCategoryManager


class FakeLDAP:
    data = dict(
        username1=[
            'CN=soen490,DC=Concordia',
            'CN=soen284,DC=Concordia',
            'CN=comp335,DC=Concordia',
            'CN=phys202,DC=Concordia',
            'CN=cse_ugrad,OU=_people_types,OU=_groups,OU=_accounts,OU=_encs,DC=ENCS,DC=concordia,DC=ca',

        ],
        username2=[
            'CN=soen490,DC=Concordia',
            'CN=soen311,DC=Concordia',
            'CN=comp248,DC=Concordia',
            'CN=comp390,DC=Concordia',
            'CN=ece_mthesis,OU=_people_types,OU=_groups,OU=_accounts,OU=_encs,DC=ENCS,DC=concordia,DC=ca',
        ]
    )

    def get_user_groups(self, username):
        return self.data.get(username)


class TestPrivilegeCategoryManager(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='username1', email="user1@gmail", password="abc")
        self.user1.save()

        self.user2 = User.objects.create_user(username='username2', email="user2@gmail", password="123")
        self.user2.save()

        self.category1 = PrivilegeCategory()
        self.category1.name = "Cat 1"
        self.category1.is_default = True
        self.category1.save(bypass_validation=True)

        self.category2 = PrivilegeCategory()
        self.category2.name = "Cat 2"
        self.category2.related_course = 'soen490'
        self.category2.save(bypass_validation=True)

        self.category3 = PrivilegeCategory()
        self.category3.name = "Cat 3"
        self.category3.related_course = 'comp335'
        self.category3.save(bypass_validation=True)

        self.ldap = FakeLDAP()

    def testAssignPrivilegesSuccess(self):
        manager = PrivilegeCategoryManager()
        manager.assign_booker_privileges(self.user1, self.ldap)

        privileges1 = self.user1.bookerprofile.privilege_categories.all()
        self.assertEqual(privileges1.count(), 3)
        self.assertEqual(privileges1[0], self.category1)
        self.assertEqual(privileges1[1], self.category2)
        self.assertEqual(privileges1[2], self.category3)
        self.assertEqual(self.user1.bookerprofile.program, 'cse')
        self.assertEqual(self.user1.bookerprofile.graduate_level, 'ugrad')

        manager.assign_booker_privileges(self.user2, self.ldap)

        privileges2 = self.user2.bookerprofile.privilege_categories.all()
        self.assertEqual(privileges2.count(), 2)
        self.assertEqual(privileges2[0], self.category1)
        self.assertEqual(privileges2[1], self.category2)
        self.assertEqual(self.user2.bookerprofile.program, 'ece')
        self.assertEqual(self.user2.bookerprofile.graduate_level, 'mthesis')

    def testAssignAllPrivilegesSuccess(self):
        manager = PrivilegeCategoryManager()
        manager.assign_all_booker_privileges(self.ldap)
        self.user1.refresh_from_db()
        self.user2.refresh_from_db()

        privileges1 = self.user1.bookerprofile.privilege_categories.all()
        self.assertEqual(privileges1.count(), 3)
        self.assertEqual(privileges1[0], self.category1)
        self.assertEqual(privileges1[1], self.category2)
        self.assertEqual(privileges1[2], self.category3)
        self.assertEqual(self.user1.bookerprofile.program, 'cse')
        self.assertEqual(self.user1.bookerprofile.graduate_level, 'ugrad')

        privileges2 = self.user2.bookerprofile.privilege_categories.all()
        self.assertEqual(privileges2.count(), 2)
        self.assertEqual(privileges2[0], self.category1)
        self.assertEqual(privileges2[1], self.category2)
        self.assertEqual(self.user2.bookerprofile.program, 'ece')
        self.assertEqual(self.user2.bookerprofile.graduate_level, 'mthesis')

    def testAssignPrivilegeLDAPUserDoesNotExist(self):
        self.user1.username = "wrong_username"
        self.user1.save()

        manager = PrivilegeCategoryManager()
        manager.assign_booker_privileges(self.user1, self.ldap)

        privileges1 = self.user1.bookerprofile.privilege_categories.all()
        self.assertEqual(privileges1.count(), 1)
        self.assertEqual(privileges1[0], self.category1)
