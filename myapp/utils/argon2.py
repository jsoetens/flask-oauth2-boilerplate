from passlib.hash import argon2


# Please note that HTTPS is required for sending encrypted data to the server.

# We will be using the Argon2 password hash. Argon2 is a state of the art
# memory-hard password hash, and the winner of the 2013 Password Hashing
# Competition. It has seen active development and analysis in subsequent
# years, and while young, and is intended to replace pbkdf2_sha256,
# bcrypt, and scrypt.

# For those used to the Werkzeug functions generate_password_hash and
# check_password_hash, these are available from this module as
# generate_argon2_hash and check_argon2_hash

# https://passlib.readthedocs.io/en/stable/lib/passlib.hash.argon2.html


def generate_argon2_hash(password, rounds=4):
    """
    Calculates an Argon2 password hash.

    Args:
        param1: password
        param2: number of rounds

    Returns:
        Argon2 password hash.
    """
    # Calculate new salt, a hash
    # h = argon2.hash(password)
    # Generate it with an explicit number of rounds (default 4)
    # print('Calculating Argon2 password hash with {}'.format(str(rounds)))
    hash = argon2.using(rounds=rounds).hash(password)
    return hash


def check_argon2_hash(password, hash):
    """
    Verifies a password with its Argon2 password hash.

    Args:
        param1: password
        param2: argon2 password hash

    Returns:
        True for success, False otherwise
    """
    # Verify the password
    return argon2.verify(password, hash)
