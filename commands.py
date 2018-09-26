"""notegit commands"""

from sh import git, ErrorReturnCode_1, ErrorReturnCode_128

import utils

def add(name, m, **kwargs):
    """Add a new note.

    args:
    ----------
    name: Name of the note
    m: Text, if None, editor will be opened to prompt user."""
    if m is None:
        text = utils.get_text_from_editor()
    else:
        text = m
    if not text or text.isspace():
        raise ValueError("Aborting due to empty note")

    with open(name, "w") as outfile:
        outfile.write(text.lstrip().rstrip())
    git.add(name)
    try:
        git.commit("-m", "add {}".format(name))
    except ErrorReturnCode_1:
        raise ValueError("No changes made to note")


def rm(name, **kwargs):
    """Remove a note by args.name."""
    try:
        git.rm(name)
    except ErrorReturnCode_128:
        raise FileNotFoundError
    git.commit("-m", "rm {}".format(name))

def ls():
    """List notes."""
    return git("ls-files")
