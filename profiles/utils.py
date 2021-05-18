import uuid

def get_random_code():
    # get string of uuid.uuid5(), idk what that is, up to 8 character, replace dash with whitespace and lowercase all characters
    # if uuid5 doesn't work use uuid4
    code = str(uuid.uuid4())[:8].replace('-', '').lower()
    return code