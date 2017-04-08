from ..db import user_table
from mastodon import Mastodon
import os
from pprint import pprint

STATE_ALREADY_UNFOLLOWED = 0
STATE_UNFOLLOWED = 1
STATE_ADDED_NOFOLLOW = 3
STATE_NOTFOUND = 4

mastodon_client = Mastodon(
    api_base_url=os.environ["BASE_URL"],
    client_id=os.environ["OAUTH_CLIENT_ID"],
    client_secret=os.environ["OAUTH_CLIENT_SECRET"],
    access_token=os.environ["OAUTH_ACCESS_TOKEN"]
)

def user_unfollow(acct):
    acct = acct.strip("@")
    user = user_table.find_one({"acct": acct})
    if user:
        if user["following"]:
            mastodon_client.account_unfollow(user["uid"])

            user_table.update_one(user, {"$set": {"following": False}})

            return STATE_UNFOLLOWED
        else:
            # They're not being followed already
            return STATE_ALREADY_UNFOLLOWED

    # Add them to the DNF list
    accounts = mastodon_client.account_search(acct)
    if len(accounts) == 0:
        return STATE_NOTFOUND

    user_table.insert({
        "acct": accounts[0]["acct"],
        "uid":  accounts[0]["id"],
        "following": False
    })

    return STATE_ADDED_NOFOLLOW
