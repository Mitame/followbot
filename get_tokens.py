from mastodon import Mastodon
import os
import getpass

if os.environ.get("OAUTH_CLIENT_ID") == None:
    name = input("App name: ")

    oauth_client_id, oauth_client_secret = Mastodon.create_app(
        name, api_base_url=os.environ["BASE_URL"]
    )
else:
    oauth_client_id = os.environ["OAUTH_CLIENT_ID"]
    oauth_client_secret = os.environ["OAUTH_CLIENT_SECRET"]

api = Mastodon(
    oauth_client_id, oauth_client_secret,
    api_base_url=os.environ["BASE_URL"]
)

print(
    "OAUTH_CLIENT_ID=%s\nOAUTH_CLIENT_SECRET=%s" % (
        oauth_client_id, oauth_client_secret
    )
)

email = input("Email: ")
password = getpass.getpass()
api.log_in(email, password)

print("OAUTH_ACCESS_TOKEN=%s" % api.access_token)

print("Fill in the empty OAUTH_* sections in .env with the values above")
