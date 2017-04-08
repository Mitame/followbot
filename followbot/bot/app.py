from websocket import WebSocketApp
from mastodon import Mastodon
import os
import json
from pprint import pprint
import logging

from ..db import user_table

class App():
    def __init__(self):
        self.mastodon = Mastodon(
            api_base_url=os.environ["BASE_URL"],
            client_id=os.environ["OAUTH_CLIENT_ID"],
            client_secret=os.environ["OAUTH_CLIENT_SECRET"],
            access_token=os.environ["OAUTH_ACCESS_TOKEN"],
        )

    def run(self):
        self.ws = WebSocketApp(
            self.mastodon.api_base_url.replace("https", "wss").replace("http", "ws") \
             + "/api/v1/streaming/" + "?access_token=%s&stream=public" % self.mastodon.access_token,
            on_error = self.on_error,
            on_message = self.on_message,
            on_close = self.on_close
        )

        self.ws.run_forever()

    def follow(self, account):
        try:
            if account["locked"] or "#dnf" in account["note"].lower():
                logging.info("Account %s is locked or has #dnf in their note" % account["acct"])
                return
        except KeyError:
            pass

        user = user_table.find_one({"uid": account["id"]})
        if user:
            logging.info("Already following or told not to follow %s" % account["acct"])
            return

        self.mastodon.account_follow(account["id"])
        logging.info("Now following %s" % account["acct"])

        user_table.insert({
            "acct": account["acct"],
            "uid": account["id"],
            "following": True
        })

    def on_error(self, ws, error):
        pass
        # print(error)

    def on_message(self, ws, message):
        event_data = json.loads(message)
        payload_data = json.loads(event_data["payload"])

        # print("Event: %s" % event_data["event"])
        # pprint(payload_data)

        if event_data["event"] == "update":
            self.follow(payload_data["account"])

            for account in payload_data["mentions"]:
                # Get all the account info
                accts = self.mastodon.account_search(account["acct"])
                if len(accts) == 0:
                    self.follow(account)
                else:
                    self.follow(accts[0])

    def on_close(self, ws):
        print("WS CLOSED")
