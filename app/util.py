from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated='auto')

def hash_password(password: str):
    return password_context.hash(password)

def verify_password(password_enter, password_db:str):
    return password_context.verify(password_enter, password_db)