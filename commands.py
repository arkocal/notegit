"""notegit commands"""

import ast
import os

from sh import git, ErrorReturnCode_1, ErrorReturnCode_128

import utils

def add(name, m, **kwargs):
    """Add a new note.

    args:
    ----------
    name: Name of the note
    m: Text, if None, editor will be opened to prompt user."""
    if os.path.isfile(name):
        existing_path = name
        mode = "edit"
    else:
        existing_path = None
        mode = "add"

    if m is None:
        text = utils.get_text_from_editor(existing_path)
    else:
        text = m

    if not text or text.isspace():
        raise ValueError("Aborting due to empty note")

    with open(name, "w") as outfile:
        outfile.write(text.lstrip().rstrip())

    git.add(name)
    try:
        git.commit("-m", "{} {}".format(mode, name))
    except ErrorReturnCode_1:
        raise ValueError("No changes made to note")


def rm(name, **kwargs):
    """Remove a note by name."""
    try:
        git.rm(name)
    except ErrorReturnCode_128:
        raise FileNotFoundError
    git.commit("-m", "rm {}".format(name))


def ls(f, **kwargs):
    """List notes.

    args:
    ----------
    f: Format string.
        %n: Name
        %m: Message (text) short (60 chars)
        %M: Message (text) full
        %le: Last editor
        %led: Last edit date
    """
    notes = [n.rstrip() for n in git("ls-files")]

    if f is None:
        f = "%n\tby %le on %led\n%M\n\n"
    else:
        f = ast.literal_eval("'{}'".format(f))

    name = lambda n: n
    message_short = lambda n: open(n, "r").read()[:60]
    message_long = lambda n: open(n, "r").read()
    last_editor = lambda n: str(git("--no-pager", "log", '--pretty=format:%an',
                                    "-n", "1", "--", n))
    last_edit_date = lambda n: str(git("--no-pager", "log",
                                       '--pretty=format:%ai',
                                       "-n", "1", "--", n))

    formatters = [("%n", name),
                  ("%m", message_short),
                  ("%M", message_long),
                  ("%led", last_edit_date),
                  ("%le", last_editor)
                  ]

    outstr = ""
    for i in notes:
        line = f[:]
        for placeholder, formatter in formatters:
            line = line.replace(placeholder, formatter(i))
        outstr += line
    return outstr
