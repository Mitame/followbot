# FollowBot
Some crappy following bot to expand your federated timeline on Mastodon.
Only use 1 per server as there isn't any point in having more.

# Setup
Copy `.env.sample` to `.env` and edit `BASE_URL` to point to your mastodon instance

Run `env $(cat .env | xargs) python3 get_tokens.py` to get OAuth client and access tokens

Run `env $(cat .env | xargs) python3 site.py` to run the site front end so users can say they don't want to be followed.

Run `env $(cat .env | xargs) python3 bot.py` to run the actual bot that follows people
