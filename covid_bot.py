import discord
import tweepy
from dotenv import load_dotenv
from os import getenv
from discord.ext import tasks
from discord.ext import commands
import re 

load_dotenv()

bot = commands.Bot(command_prefix='.')
auth = tweepy.OAuthHandler(getenv("CONSUMER_KEY"), getenv("CONSUMER_SECRET"))
auth.set_access_token(getenv("ACCESS_TOKEN"), getenv("ACCESS_TOKEN_SECRET"))
api = tweepy.API(auth)
tweets = api.user_timeline("NSWHealth")
last_checked = 0
if (len(tweets) > 0):
    last_checked = tweets[0].id

@bot.event
async def on_ready():
    test_send.start()

@tasks.loop(seconds=60)
async def test_send():
    global last_checked
    tweets = api.user_timeline("NSWHealth", since_id=last_checked);
    query = "(NSW recorded [\d,]+ new)|(PUBLIC HEALTH ALERT)"
    for tweet in reversed(tweets):
        if (re.search(query, tweet.text)):
            await bot.get_channel(int(getenv("COVID_CHANNEL_ID"))).send("https://twitter.com/twitter/statuses/" + str(tweet.id))

    if len(tweets) > 0:
        last_checked = tweets[0].id

bot.run(getenv('DISCORD_TOKEN'))