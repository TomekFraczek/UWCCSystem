import helper_scripts.setup_django

from core.models.MemberModels import Member


def fix_all_group_names(dummy, blank):
    for member in Member.objects.all():
        group_name = member.groups.all()[0].name
        member.group = group_name
        member.save()


if __name__ == "__main__":
    fix_all_group_names()
