import re
import sys

LINK_REGEX = "#[0-9]+"
MERGE_REGEX = "Merge"


def validate_commit_message():
    """ Make sure commit message has is linked to an issue. """

    try:
        script, commit_msg = sys.argv

        link_match = re.search(LINK_REGEX, commit_msg)
        merge_match = re.search(MERGE_REGEX, commit_msg, re.IGNORECASE)

        if link_match is not None or merge_match is not None:
            return 0
    except Exception as e:
        print("ERROR")
        print(e)

    print("Commit message does not link to an issue and isn't a merge commit")
    return 1


if __name__ == '__main__':
    sys.exit(validate_commit_message())
