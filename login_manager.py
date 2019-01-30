import database_common
import bcrypt


@database_common.connection_handler
def read_hash(cursor, name):
    cursor.execute("""
                    SELECT user_password FROM "user"
                    WHERE user_name LIKE %(name)s;""", {'name': name})
    hash_pw = cursor.fetchone()
    return hash_pw


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)
