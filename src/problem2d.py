if __name__ == "__main__":
    import unittest
    import os
    from problem2c import PASSWD_FILE, ph, add_user_record, get_user_record

    class TestPasswdFileUsage(unittest.TestCase):
        def setUp(self):
            # Start each test with a fresh, empty password file
            if PASSWD_FILE.exists():
                os.remove(PASSWD_FILE)
            PASSWD_FILE.touch()

        def tearDown(self):
            # Clean up at the end to ensure we don't use a "test" passwd.txt
            if PASSWD_FILE.exists():
                os.remove(PASSWD_FILE)

        def test_add_get_user_record(self):
            uname = 'hubert'
            plaintext_passwd = 'secret'

            add_user_record(uname, plaintext_passwd)
            stored_user_record = get_user_record(uname)
            self.assertIsNotNone(stored_user_record)

            stored_uname, stored_hash_str = stored_user_record
            self.assertEqual(uname, stored_uname)
            self.assertTrue(ph.verify(stored_hash_str, plaintext_passwd))

            # Retrive the record a 2nd time to verify the 1st didn't corrupt it
            stored_uname, stored_hash_str = stored_user_record
            self.assertEqual(uname, stored_uname)
            self.assertTrue(ph.verify(stored_hash_str, plaintext_passwd))

        def test_get_non_existent_user_record(self):
            uname = 'hubert'
            plaintext_passwd = 'secret'

            stored_user_record = get_user_record(uname)  # Doesn't exist yet
            self.assertIsNone(stored_user_record)

            add_user_record(uname, plaintext_passwd)

            stored_user_record = get_user_record('idontexist')
            self.assertIsNone(stored_user_record)

    unittest.main()
