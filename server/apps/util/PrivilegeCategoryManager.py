from apps.util import ldap_server
from apps.accounts.models.PrivilegeCategory import PrivilegeCategory
from apps.accounts.models import Booker


class PrivilegeCategoryManager:

    def clear_booker_privileges(self, booker_id):
        booker = Booker.objects.get(booker_id=booker_id)
        booker.privilege_categories.clear()
        booker.save()

    def clear_all_booker_privileges(self):
        bookers = Booker.objects.all()
        for booker in bookers:
            self.clear_booker_privileges(booker.booker_id)

    def assign_booker_privileges(self, booker_id):
        booker = Booker.objects.get(booker_id=booker_id)
        privilege_categories = PrivilegeCategory.objects.all()
        courses = ldap_server.get_user_groups(username=booker.user.username)

        self.clear_booker_privileges(booker_id)

        default_category = privilege_categories.get(is_default=True)
        if default_category:
            booker.privilege_categories.add(default_category)

        for category in privilege_categories:
            for course in courses:
                course.lower()
                if category.related_course in course:
                    booker.privilege_categories.add(category)

    def assign_all_booker_privileges(self):
        bookers = Booker.objects.all()
        for booker in bookers:
            self.assign_booker_privileges(booker.booker_id)

