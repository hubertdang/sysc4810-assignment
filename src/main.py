from problem3ab import enrol_user_cli


if __name__ == '__main__':
    import questionary
    from problem3ab import enrol_user_cli
    from problem4c import login_user_cli

    SIGNUP_OPTION = 'Signup'
    LOGIN_OPTION = 'Login'
    QUIT_OPTION = 'Quit'

    while (True):
        print()
        option = questionary.select('Please select an option', choices=[
                                    SIGNUP_OPTION, LOGIN_OPTION, QUIT_OPTION]).ask()

        if option == SIGNUP_OPTION:
            enrol_user_cli()
        elif option == LOGIN_OPTION:
            login_user_cli()
        elif option == QUIT_OPTION:
            break
