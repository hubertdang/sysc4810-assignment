import questionary
from typing import NamedTuple
from pathlib import Path
from functools import partial
from problem1c import Role
from problem2c import add_user_passwd_record, get_user_passwd_record

UNAME_MIN_LEN = 6
UNAME_MAX_LEN = 12

PASSWD_MIN_LEN = 8
PASSWD_MAX_LEN = 12

SPECIAL_CHARACTERS = set('!@#$%*&')

WEAK_PASSWD_FILE = Path(__file__).parent.parent / 'weak_passwd.txt'

ROLES_FILE = Path(__file__).parent.parent / 'roles.txt'

ROLES_FILE_RECORD_DELIMITER = ':'
NUM_ROLES_FILE_RECORD_FIELDS = 2


class UserRolesRecord(NamedTuple):
    uname: str
    roles: set[Role]


def validate_uname(uname: str) -> bool | str:
    """
    Validates a username. Usernames are unique, 6-12 characters long, contain
    only upper and lower-case letters, numerical digits, and no spaces.

    Returns:
        True if the username is valid.
        String error message (for questionary library) otherwise.
    """
    if ' ' in uname:
        return 'Usernames must not contain spaces! Backspace and choose again.'
    if not uname.isalnum():
        return 'Usernames must only contain letters and numbers! Backspace and choose again.'
    if len(uname) < UNAME_MIN_LEN or len(uname) > UNAME_MAX_LEN:
        return 'Usernames must be 6-12 characters long! Backspace and choose again.'
    if get_user_passwd_record(uname) is not None:
        return 'Username already chosen! Backspace and choose again.'
    return True


def is_weak(passwd: str) -> bool:
    """
    Checks if a password is "weak" by going through the weak password file and
    checking if there is a match.
    """
    with open(WEAK_PASSWD_FILE, 'r', encoding='utf-8') as weak_passwd_file:
        for line in weak_passwd_file:
            weak_passwd = line.rstrip('\n')
            if passwd == weak_passwd:
                return True
    return False


def validate_passwd(passwd: str, uname: str) -> bool | str:
    """
    Validates a password. Passwords are unique, 8-12 characters long, and must
    include at least one upper-case letter, one lower-case letter, one numerical
    digit, and one special character from the following: !, @, #, $, %, *, &.
    Additionally, Passwords must not match a password found on a list of common
    weak passwords, and passwords matching the username must be prohibited.

    Returns:
        True if the password is valid.
        String error message (for questionary library) otherwise.
    """
    if ' ' in passwd:
        return 'Passwords must not contain spaces! Backspace and choose again. Backspace and choose again.'
    if not any(char.isupper() for char in passwd):
        return 'Passwords must contain at least one upper-case letter! Backspace and choose again.'
    if not any(char.islower() for char in passwd):
        return 'Passwords must contain at least one lower-case letter! Backspace and choose again.'
    if not any(char.isdigit() for char in passwd):
        return 'Passwords must contain at least one numerical digit! Backspace and choose again.'
    if not any(char in SPECIAL_CHARACTERS for char in passwd):
        return 'Passwords must contain at least one special character from the following: !, @, #, $, %, *, &. Backspace and choose again.'
    if len(passwd) < PASSWD_MIN_LEN or len(passwd) > PASSWD_MAX_LEN:
        return 'Passwords must be 8-12 characters long! Backspace and choose again.'
    if passwd == uname:
        return 'Passwords cannot be the same as your username! Backspace and choose again.'
    if is_weak(passwd):
        return 'Password too weak! Backspace and choose again.'

    return True


def add_user_roles_record(uname: str, roles: list[str]) -> None:
    """
    Adds a record to the user roles file containing a username and their roles.
    """
    with open(ROLES_FILE, 'a', encoding='utf-8') as roles_file:
        # Roles are stored as comma-separated strings
        roles_str = ','.join(roles)
        fields = [uname, roles_str]
        roles_file.write(ROLES_FILE_RECORD_DELIMITER.join(fields) + '\n')


def get_user_roles_record(uname: str) -> UserRolesRecord | None:
    """
    Retrieves a user record from the user roles file.

    Returns:
        The user record if it exists.
        None otherwise.
    """
    try:
        with open(ROLES_FILE, 'r', encoding='utf-8') as passwd_file:
            for line in passwd_file:
                stripped_line = line.rstrip('\n')
                if stripped_line.startswith(uname + ROLES_FILE_RECORD_DELIMITER):
                    fields = stripped_line.split(
                        ROLES_FILE_RECORD_DELIMITER, maxsplit=1)
                    if len(fields) == NUM_ROLES_FILE_RECORD_FIELDS:
                        _, roles_str = fields
                        if roles_str:
                            # Convert comma-separated string into set of roles
                            roles = {Role(role)
                                     for role in roles_str.split(',')}
                        else:
                            roles = set()  # Handle a user having no roles
                        return UserRolesRecord(uname=uname, roles=roles)
    except FileNotFoundError:
        return None  # Roles file gets created when we add the first record
    return None  # Couldn't find a record for this username


def enrol_user_cli():
    """
    Runs a command line interface using the questionary library
    (https://questionary.readthedocs.io/en/stable/pages/quickstart.html) to
    enrol a user into the system.
    """
    chosen_uname = questionary.text(
        'Choose a username: ', validate=validate_uname, validate_while_typing=False).ask()

    # Stick the chosen username into the password validate function
    validate_passwd_with_uname = partial(validate_passwd, uname=chosen_uname)

    chosen_passwd = questionary.password(
        'Choose a password: ', validate=validate_passwd_with_uname, validate_while_typing=False).ask()

    add_user_passwd_record(chosen_uname, chosen_passwd)

    # Prompt user to select role(s) based on Role enum from problem 1.c)
    role_prompt = questionary.checkbox(
        'Select role(s)',
        choices=[role.value for role in Role],
        instruction='(Use arrow keys to move, <space> to select, <Enter> to submit)')

    selected_roles = role_prompt.ask()
    add_user_roles_record(chosen_uname, selected_roles)
