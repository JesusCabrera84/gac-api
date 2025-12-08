from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

hash_str = "$argon2id$v=19$m=65536,t=3,p=4$idF67x1DKCVkLAVAiLH2/g$b5QL87kPrKoffgb2iOgli/3ZPx1xDd4ssHcv5UfM1A4"
password = "gac-admin"

try:
    print(f"Verifying hash: {hash_str}")
    result = pwd_context.verify(password, hash_str)
    print(f"Verification result: {result}")
except Exception as e:
    print(f"Error: {e}")
    # Try to identify the hash
    try:
        print(f"Identify: {pwd_context.identify(hash_str)}")
    except Exception as ie:
        print(f"Identify Error: {ie}")
