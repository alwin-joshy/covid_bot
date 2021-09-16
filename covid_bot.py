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
last_checked = tweets[-1].id

@bot.event
async def on_ready():
    test_send.start()

@tasks.loop(seconds=10)
async def test_send():
    tweets = api.user_timeline("NSWHealth", last_checked);
    query = "(NSW recorded [\d,]+ new)|(PUBLIC HEALTH ALERT)"
    for tweet in tweets:
        if (match = re.search(query, tweet.text)):
            await bot.get_channel(int(getenv('COVID_CHANNEL_ID'))).send("https://twitter.com/twitter/statuses/" + tweet.id)

    last_checked = tweets[-1].id

bot.run(getenv('DISCORD_TOKEN'))

