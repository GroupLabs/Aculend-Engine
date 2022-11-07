from models.UserModel import User
import base64
import bcrypt

def register(data, db):
    # Check if email is registered
    user = db["users"].find_one({"email": data["email"]})

    # throw error if exists
    if user is not None:
        raise FileExistsError("Email already registered")

    # assimilate to User class
    user = User(
        name=data["name"],
        email=data["email"],
        password=data["password"],
        avatar="Not set"
    )

    # upload to users collection
    db["users"].insert_one(user.get_dict())

def login():
    # Check if email is registered
    user = db["users"].find_one({"email": data["email"]})

    # throw error if user does not exist
    if user is None:
        raise FileNotFoundError("User not found")

    # check if password is valid
    valid = bcrypt.checkpw(data["pass"], user["password"])

    if not valid:
        raise ConnectionRefusedError("User or password is incorrect")

    # Building JWT
    payload = {
        "id" : user["_id"],
        "name" : user["name"],
        "avatar" : user["avatar"]
    }

    token = ""

    return token

def current_user():
    return

def change_pass(data, db): # Requires testing
    # check if email exists
    user = db["users"].find_one({"email":data["email"]})

    # throw error if not in database
    if user is None:
        raise FileNotFoundError("Email not found")

    # update password
    db["users"].update_one({"email":data["email"]}, {"password":data["pass"]})

def str_to_b64(string):
    message_bytes = string.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    return base64_bytes.decode('ascii')

def send_email(data, db): # Requires testing
    # check if email exists
    user = db["users"].find_one({"email":data["email"]})

    # throw error if not in database
    if user is None:
        raise FileNotFoundError("Email not found")

    # encode email
    encoded_email = str_to_b64(data["email"])

    # build html for email
    email_html = f'Hello! <br/> <a href="{URL}/forgot-password/{encoded_email}">Click here to change your password</a>'

    try:
        requests.post(
            f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
            auth=("api", "{MAILGUN_API_KEY}"),
            data={"from": "no-reply <mailgun@YOUR_DOMAIN_NAME>",
                "to": [data["email"], "YOU@YOUR_DOMAIN_NAME"], # do we want to send this to ourselves as log?
                "subject": "Password Change",
                "html": email_html}
        )
    except:
        print("Unknown error trying to send email")