from typing import NamedTuple
from pathlib import Path
from argon2 import PasswordHasher
from argon2 import Type as ArgonType

PASSWD_FILE = Path(__file__).parent.parent / 'passwd.txt'

PASSWD_FILE_RECORD_DELIMITER = ':'
NUM_PASSWD_FILE_RECORD_FIELDS = 2


class UserPasswdRecord(NamedTuple):
    uname: str
    hash_str: str


TIME_COST = 2  # Number of iterations
PARALLELISM = 1  # 1 lane
MEMORY_COST_KIB = 19456  # 19 MiB
SALT_LENGTH = 16  # 128-bit salt
HASH_LENGTH = 32  # 256-bit hash

# Argon2id hashing algorithm config (OWASP recommendations)
ph = PasswordHasher(
    time_cost=TIME_COST,
    parallelism=PARALLELISM,
    memory_cost=MEMORY_COST_KIB,
    salt_len=SALT_LENGTH,
    hash_len=HASH_LENGTH,
    type=ArgonType.ID
)


def add_user_passwd_record(uname: str, plaintext_passwd: str) -> None:
    """
    Hashes and salts a plaintext password and adds a new user record to the
    password file.
    """
    hash_str = ph.hash(plaintext_passwd)  # Argon2id adds salt for you
    record = UserPasswdRecord(uname, hash_str)

    with open(PASSWD_FILE, 'a', encoding='utf-8') as passwd_file:
        passwd_file.write(PASSWD_FILE_RECORD_DELIMITER.join(record) + '\n')


def get_user_passwd_record(uname: str) -> UserPasswdRecord | None:
    """
    Retrieves a user record from the password file.

    Returns:
        The user record if it exists.
        None otherwise.
    """
    try:
        with open(PASSWD_FILE, 'r', encoding='utf-8') as passwd_file:
            for line in passwd_file:
                stripped_line = line.rstrip('\n')
                if stripped_line.startswith(uname + PASSWD_FILE_RECORD_DELIMITER):
                    fields = stripped_line.split(
                        PASSWD_FILE_RECORD_DELIMITER, maxsplit=1)
                    if len(fields) == NUM_PASSWD_FILE_RECORD_FIELDS:
                        _, hash_str = fields
                        return UserPasswdRecord(uname, hash_str)
    except FileNotFoundError:
        return None  # Password file gets created when we add the first record
    return None  # Couldn't find a record for this username
