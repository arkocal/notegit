"""Bunch of utility functions."""

from os import system, environ
from uuid import uuid4

from sh import git, ErrorReturnCode_128

def is_repo():
    """Check whether a git repo exists."""
    try:
        git("status")
    except ErrorReturnCode_128:
        return False
    return True


def create_repo():
    """Create a repo."""
    git("init")


def get_text_from_editor(existing_path=None):
    """Let user enter text using $EDITOR.

    Return an empty string if file is not saved."""
    tmp_file_path = "/tmp/notes_{}".format(uuid4())
    if existing_path is None:
        system("touch {}".format(tmp_file_path))
    else:
        system("cp {} {}".format(existing_path, tmp_file_path))
    system("{} {}".format(environ["EDITOR"], tmp_file_path))
    with open(tmp_file_path, "r") as tmpfile:
        return tmpfile.read()
