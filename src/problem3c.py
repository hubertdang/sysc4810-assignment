from problem2c import add_user_passwd_record


if __name__ == "__main__":
    import unittest
    import os
    from problem1c import Role
    from problem2c import PASSWD_FILE, add_user_passwd_record
    from problem3ab import ROLES_FILE, UserRolesRecord, validate_uname, validate_passwd, add_user_roles_record, get_user_roles_record

    class TestEnrolment(unittest.TestCase):
        def setUp(self):
            # Start each test with a fresh, empty roles file
            if ROLES_FILE.exists():
                os.remove(ROLES_FILE)
            ROLES_FILE.touch()

            # Start each test with a fresh, empty password file
            if PASSWD_FILE.exists():
                os.remove(PASSWD_FILE)
            PASSWD_FILE.touch()

        def tearDown(self):
            # Clean up at the end to ensure we don't use a "test" roles.txt
            if ROLES_FILE.exists():
                os.remove(ROLES_FILE)
            ROLES_FILE.touch()

            # Clean up at the end to ensure we don't use a "test" passwd.txt
            if PASSWD_FILE.exists():
                os.remove(PASSWD_FILE)
            PASSWD_FILE.touch()

        def test_validate_uname(self):
            uname = 'hubert dang'
            self.assertEqual(validate_uname(
                uname), 'Usernames must not contain spaces! Backspace and choose again.')

            uname = 'hubertdang1!'
            self.assertEqual(validate_uname(
                uname), 'Usernames must only contain letters and numbers! Backspace and choose again.')

            uname = 'hubertdang123456'
            self.assertEqual(validate_uname(
                uname), 'Usernames must be 6-12 characters long! Backspace and choose again.')

            uname = 'hubertdang'
            add_user_passwd_record(uname, 'asdfQWE123!')
            self.assertEqual(validate_uname(
                uname), 'Username already chosen! Backspace and choose again.')

            uname = 'hubertdang1'
            self.assertTrue(validate_uname(uname))

        def test_validate_passwd(self):
            uname = 'hubertdang'

            passwd = ' asdfQWE123!'
            self.assertEqual(validate_passwd(
                passwd, uname), 'Passwords must not contain spaces! Backspace and choose again. Backspace and choose again.')

            passwd = 'asdfqwe123!'
            self.assertEqual(validate_passwd(
                passwd, uname), 'Passwords must contain at least one upper-case letter! Backspace and choose again.')

            passwd = 'ASDFQWE123!'
            self.assertEqual(validate_passwd(
                passwd, uname), 'Passwords must contain at least one lower-case letter! Backspace and choose again.')

            passwd = 'asdfQWE!'
            self.assertEqual(validate_passwd(
                passwd, uname), 'Passwords must contain at least one numerical digit! Backspace and choose again.')

            passwd = 'asdfQWE123'
            self.assertEqual(validate_passwd(
                passwd, uname), 'Passwords must contain at least one special character from the following: !, @, #, $, %, *, &. Backspace and choose again.')

            passwd = 'aQ1!'
            self.assertEqual(validate_passwd(
                passwd, uname), 'Passwords must be 8-12 characters long! Backspace and choose again.')

            passwd = 'asdfQWE123!@asfAdf$12'
            self.assertEqual(validate_passwd(
                passwd, uname), 'Passwords must be 8-12 characters long! Backspace and choose again.')

            passwd = 'P@ssw0rd'
            self.assertEqual(validate_passwd(passwd, uname),
                             'Password too weak! Backspace and choose again.')

            passwd = 'asdfQWE123!'
            self.assertTrue(validate_passwd(passwd, uname))

        def test_add_get_user_roles_record(self):
            uname = 'hubertdang'
            roles = ['Client', 'Premium Client']
            add_user_roles_record(uname, roles)
            record = get_user_roles_record(uname)
            self.assertEqual(record.uname, uname)
            self.assertIn(Role.CLIENT, record.roles)
            self.assertIn(Role.PREMIUM_CLIENT, record.roles)

            uname = 'johndoe'
            roles = []
            add_user_roles_record(uname, roles)
            record = get_user_roles_record(uname)
            self.assertEqual(record.roles, set())

    unittest.main()
