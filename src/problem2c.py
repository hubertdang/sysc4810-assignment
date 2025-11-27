from typing import NamedTuple
from pathlib import Path
from argon2 import PasswordHasher
from argon2 import Type as ArgonType

PASSWD_FILE = Path(__file__).parent.parent / 'passwd.txt'

RECORD_DELIMITER = ':'
NUM_RECORD_FIELDS = 2


class UserRecord(NamedTuple):
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


def add_user_record(uname: str, plaintext_passwd: str) -> None:
    """
    Hashes and salts a plaintext password and adds a new user record to the
    password file.
    """
    passwd_hash = ph.hash(plaintext_passwd)  # Argon2id adds salt for you
    record = [uname, passwd_hash]

    with open(PASSWD_FILE, 'a', encoding='utf-8') as passwd_file:
        passwd_file.write(RECORD_DELIMITER.join(record) + '\n')


def get_user_record(uname: str) -> UserRecord | None:
    """
    Retrieves a user record from the password file.
    """
    with open(PASSWD_FILE, 'r', encoding='utf-8') as passwd_file:
        for line in passwd_file:
            stripped_line = line.rstrip('\n')
            if stripped_line.startswith(uname + RECORD_DELIMITER):
                fields = stripped_line.split(RECORD_DELIMITER, maxsplit=1)
                if len(fields) == NUM_RECORD_FIELDS:
                    _, hash_str = fields
                    return UserRecord(uname=uname, hash_str=hash_str)
    return None
