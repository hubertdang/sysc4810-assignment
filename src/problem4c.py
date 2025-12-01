import questionary
from argon2.exceptions import VerifyMismatchError
from problem1c import Operation, get_authorized_operations
from problem2c import ph, get_user_passwd_record
from problem3ab import get_user_roles_record


def login_user_cli():
    """
    Runs a command line interface using the questionary library
    (https://questionary.readthedocs.io/en/stable/pages/quickstart.html) to
    log a user into the system.
    """
    uname = questionary.text('Enter your username: ').ask()
    plaintext_passwd = questionary.password('Enter your password: ').ask()

    user_passwd_record = get_user_passwd_record(uname)
    if user_passwd_record:
        try:
            # raises VerifyMismatchError if verification fails, pass otherwise
            ph.verify(user_passwd_record.hash_str, plaintext_passwd)

            # At this point, user has successfully logged in
            user_roles_record = get_user_roles_record(uname)
            print('\nUsername: ' + uname)

            roles_str = ", ".join(
                sorted(role.value for role in user_roles_record.roles))
            print('Role(s): ' + roles_str)

            print('\nSystem operations:')
            for operation in Operation:
                print('- ' + operation.value)

            authorized_operations = get_authorized_operations(
                user_roles_record.roles)
            print('\nAuthorized operations:')
            for operation in authorized_operations:
                print('- ' + operation.value)

        except VerifyMismatchError:
            print('Login failed! Invalid password!')
    else:
        print('Login failed! Invalid user credentials!')
