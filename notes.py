"""A simple note taking program based on Git."""

import argparse

import commands
import error_code
import utils

def is_valid_args(args):
    if args.command in ["add", "rm"] and args.name is None:
        return False
    return True


if __name__ == "__main__":

    if not utils.is_repo():
        if not input("No repository. Create? [Y/n] ").lower() in ["n", "no"]:
            utils.create_repo()
            print("Created repository.")
        else:
            print("Exiting...")
            exit(error_code.NO_REPO)

    parser = argparse.ArgumentParser(description="Git backed note taking")
    parser.add_argument("command", metavar="command", type=str,
                        choices=["add", "rm", "ls"])
    parser.add_argument("name", metavar="name", type=str, nargs="?",
                        help="Name of the note, required for add and rm")
    parser.add_argument("-m", metavar="-m", type=str)
    args = parser.parse_args()

    if not is_valid_args(args):
        print("Invalid arguments, run --help for help")
        exit(error_code.INVALID_ARGUMENT)

    if args.command == "add":
        try:
            commands.add(**vars(args))
        except ValueError as v:
            print(str(v))
            exit(error_code.ADD_FAIL)

    elif args.command == "rm":
        try:
            commands.rm(**vars(args))
        except FileNotFoundError:
            print("No such note")
            exit(error_code.NO_NOTE)

    elif args.command == "ls":
        print(commands.ls(), end="")
