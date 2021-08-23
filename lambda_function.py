import json

from changelog_checker import check_changelog_for_mod

def lambda_handler():
    version, changelog = check_changelog_for_mod("space-exploration")
    print(version)
    print(changelog)


if __name__ == '__main__':
    lambda_handler()
