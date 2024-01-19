import discord
from discord.ext import commands, tasks
import random
import asyncio
import httpx
import json
from bs4 import BeautifulSoup
from googlesearch import search
from youtubesearchpython import Search
import os
import openai
from PIL import Image
from io import BytesIO
import aiohttp
import giphy_client
from giphy_client.rest import ApiException
from translate import Translator
import requests
import feedparser
import numpy as np

import timedelta
import datetime

from discord_together import DiscordTogether
from keep_alive import keep_alive

# Create a new bot instance with a specified command prefix
intents = discord.Intents.default()  # Get the default intents
intents.members = True
intents.message_content = True
intents.typing = False
intents.presences = False
intents.reactions = True

# Dictionary to store user balances
balances = {}

# Dictionary to store user bets 
user_bets = {}

# Dictionary to store the birthday dates
birthdays = {}

# Dictionary to store user credentials
user_credentials = {}

# Dictionary to store profiles of members
profiles = {}

# Map weather conditions to emojis
WEATHER_EMOJIS = {
    "Clear": "☀️",
    "Clouds": "☁️",
    "Rain": "🌧️",
    "Drizzle": "🌦️",
    "Thunderstorm": "⛈️",
    "Snow": "❄️",
    "Mist": "🌫️",
    "Fog": "🌁",
    "Haze": "🌫️",
}

# Map sunrise and sunset to emojis
SUN_EMOJIS = {
    "sunrise": "🌅",
    "sunset": "🌇",
}



# Function to scrape Manganato for the latest One Piece chapter
def get_latest_manganato_chapter():
    url = 'https://chapmanganato.com/manga-aa951409'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    latest_chapter = soup.find('aa', class_='a-h')

    # Parse the latest chapter details (you may need to customize this depending on the website's structure)
    chapter_number = latest_chapter.find('a').text.strip()
    chapter_title = latest_chapter.find('span').text.strip()

    return f"New One Piece chapter released on Manganato!\nChapter {chapter_number}: {chapter_title}"



@tasks.loop(seconds=30)  # Run the task every 60 seconds (adjust as needed)
async def check_and_post_latest_chapter():
    await bot.wait_until_ready()
    channel_id = # Replace with the channel ID where you want to send the notifications
    channel = bot.get_channel(channel_id)

    try:
        latest_chapter_notification = get_latest_manganato_chapter()
        if channel:
            await channel.send(latest_chapter_notification)
        else:
            print(f"Channel with ID {channel_id} not found or inaccessible.")
    except Exception as e:
        print(f"An error occurred: {e}")


    





# Create a new bot instance with a specified command prefix
bot = commands.Bot(command_prefix='//',  intents=intents)
openai.api_key = YOUR_OPENAI_API_KEY
W_API_KEY = YOUR_API_KEY
giphy_api = giphy_client.DefaultApi()



# Event that runs when the bot is ready and connected to Discord
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print('Bot is ready to receive commands')

    bot.togetherControl = await DiscordTogether("MTEyMjg3NjgwNjIyNDE1MDU1OA.GB4hAN.MZEhIKgdg7LvEpMwz4kUMlQp9hchyI7PrLG0xw")

    check_and_post_latest_chapter.start()  # Start the automatic task

    
    await bot.change_presence(activity = discord.Game('One Piece'))

@bot.command()
async def latest_chapter(ctx):
    latest_chapter_notification = get_latest_manganato_chapter()
    await ctx.send(latest_chapter_notification)

@bot.command()
async def join(ctx, member: discord.Member):
    welcome_channel_name = 'welcome'  # Replace 'welcome' with the name of your welcome channel
    attachments_channel_id = # Replace with the ID of the channel with attachments

    # Find the welcome channel
    channel = discord.utils.get(member.guild.text_channels, name=welcome_channel_name)

    if channel:
        embed = discord.Embed(
            title=f'Welcome {member.name}!',
            description=f'Welcome {member.mention} to the server!\n' f'Go to {bot.get_channel(1123209510501240892).mention} to get started ' f'on how to use Discord or just dive into {bot.get_channel(1014074074609242152).mention} ' f'to know more about our server.',
            color=discord.Color.green()
        )

        attachments = []
        attachments_channel = bot.get_channel(attachments_channel_id)
        async for message in attachments_channel.history(limit=30):  # Retrieve last 30 messages
            for attachment in message.attachments:
                attachments.append(attachment.url)

        if not attachments:
            await channel.send("No image attachments found in the channel.")
            return

        random_attachment = random.choice(attachments)

        member_count = len(member.guild.members)

        # Send the welcome message with the random attachment and member count in the footer
        embed.set_image(url=random_attachment)
        embed.set_footer(text=f'Member Count: {member_count}')
        await channel.send(embed=embed)
    else:
        print("Welcome channel not found.")



# Event: Custom Welcomme message
@bot.event
async def on_member_join(member: discord.Member):
    welcome_channel_name = 'welcome'  # Replace 'welcome' with the name of your welcome channel
    attachments_channel_id = # Replace with the ID of the channel with attachments

    # Find the welcome channel
    channel = discord.utils.get(member.guild.text_channels, name=welcome_channel_name)

    if channel:
        embed = discord.Embed(
            title=f'Welcome {member.name}!',
            description=f'**Welcome {member.mention} to the server! 😍\n\n' f'Go to {bot.get_channel(1123209510501240892).mention} to get started' f'on how to use Discord or just dive into {bot.get_channel(1014074074609242152).mention}' f'to know more about our server.**',
            color=discord.Color.red()
        )

        attachments = []
        attachments_channel = bot.get_channel(attachments_channel_id)
        async for message in attachments_channel.history(limit=50):  # Retrieve last 50 messages
            for attachment in message.attachments:
                attachments.append(attachment.url)

        if not attachments:
            await channel.send("No image attachments found in the channel.")
            return

        random_attachment = random.choice(attachments)

        member_count = len(member.guild.members)

        # Send the welcome message with the random attachment and member count in the footer
        embed.set_image(url=random_attachment)
        embed.set_footer(text=f'Member Count: {member_count}')
        await channel.send(embed=embed)
    else:
        print("Welcome channel not found.")



@bot.event
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.text_channels, name='goodbye')
    if channel:
        embed = discord.Embed(
            title=f'Goodbye {member.name}!',
            color=discord.Color.red()
        )
        
        await channel.send(embed=embed)
    else:
        print("Goodbye channel not found.")

@bot.command()
async def start_awkword(ctx):
    link = await bot.togetherControl.create_link(ID, 'awkword')
    await ctx.send(f"Click the blue link!\n{link}")
    

@bot.command()
async def start_youtube(ctx):
    link = await bot.togetherControl.create_link(ID, 'youtube')
    await ctx.send(f"Click the blue link!\n{link}")


@bot.command()
async def start_poker(ctx):
    link = await bot.togetherControl.create_link(ID, 'poker')
    await ctx.send(f"Click the blue link!\n{link}")

@bot.command()
async def land_io(ctx):
    link = await bot.togetherControl.create_link(ID, 'land-io')
    await ctx.send(f"Click the blue link!\n{link}")

@bot.command()
async def start_party(ctx):
    link = await bot.togetherControl.create_link(ID, 'putt-party')
    await ctx.send(f"Click the blue link!\n{link}")

@bot.command()
async def start_chess(ctx):
    link = await bot.togetherControl.create_link(ID, 'chess')
    await ctx.send(f"Click the blue link!\n{link}")

@bot.command()
async def start_bobble(ctx):
    link = await bot.togetherControl.create_link(ID, 'bobble-league')
    await ctx.send(f"Click the blue link!\n{link}")

@bot.command()
async def start_asking(ctx):
    link = await bot.togetherControl.create_link(ID, 'ask-away')
    await ctx.send(f"Click the blue link!\n{link}")

@bot.command()
async def start_word(ctx):
    link = await bot.togetherControl.create_link(ID, 'word-snack')
    await ctx.send(f"Click the blue link!\n{link}")

@bot.command()
async def start_blazing(ctx):
    link = await bot.togetherControl.create_link(ID, 'blazing-8s')
    await ctx.send(f"Click the blue link!\n{link}")

@bot.command()
async def start_spellcast(ctx):
    link = await bot.togetherControl.create_link(ID, 'spellcast')
    await ctx.send(f"Click the blue link!\n{link}")

@bot.command()
async def start_letter(ctx):
    link = await bot.togetherControl.create_link(ID, 'letter-league')
    await ctx.send(f"Click the blue link!\n{link}")

@bot.command()
async def start_checkers(ctx):
    link = await bot.togetherControl.create_link(ID, 'checkers')
    await ctx.send(f"Click the blue link!\n{link}")

@bot.command()
async def start_sketch(ctx):
    link = await bot.togetherControl.create_link(ID, 'sketch-heads')
    await ctx.send(f"Click the blue link!\n{link}")
          
# Command to pout
@bot.command()
async def picknose(ctx):
    """ Pick your nose like a pro """
    try:
        # Set up Giphy API client
        giphy_api_instance = giphy_client.DefaultApi()

        # Search for "pout" GIFs using the Giphy API 
        api_key = GIPHY_API_KEY
        query = 'luffy pick his nose'
        api_response = giphy_api_instance.gifs_search_get(api_key, query, limit=1)

        if api_response.data:
            pout_gif_url = api_response.data[0].images.downsized.url
            await ctx.send((pout_gif_url))
        else:
            await ctx.send("Sorry, I couldn't find any pout GIFs at the moment.")

    except ApiException as e:
        print("Exception when calling Giphy API: %s\n" % e)

luffy_quotes = [
    "I'm gonna be the Pirate King!",
    "I don't want to conquer anything. It's just that the person with the most freedom on the sea is the Pirate King!",
    "If I die trying, then at least I tried!",
    "I don't care if anyone hates me. I'm not doing this to be liked!",
    "I don't know how to lie. I can only say what I want to do!",
    "I can't just sit back and watch while my friends are in trouble!",
    "I don't need a reason to help people!",
    "I don't want to conquer anything. I just think that the guy with the most freedom in this whole ocean... is the Pirate King!",
    "I'm not a hero, but I have an obligation to do what I can!",
    "Even if everyone calls you a liar, even if it's a mistake, you should just keep believing and keep going forward!",
    "When do you think people die? When they are shot through the heart by the bullet of a pistol? No. When they are ravaged by an incurable disease? No. When they drink a soup made from a poisonous mushroom!? No! It's when... they are forgotten!",
    "I don't wanna conquer anything! It's just that the person with the most freedom in the whole ocean is the Pirate King!",
    "Someday... I'm gonna gather a crew stronger than any other, and we're gonna find One Piece!",
    "If you don't take risks, you can't create a future!",
    "No matter how hard or impossible it is, never lose sight of your goal.",
    "A wound that would make an ordinary man unconscious... I won't lose to it. A wound that would kill an ordinary person... I won't lose to it! To face one who is extraordinary, Hawk Eyes... I can't allow myself to be ordinary!",
    "No matter what kind of weapon you hold, just standing and looking down at the sea... That will not be called a pirate!",
    "A man's dream never dies!",
    "I don't need a map! We'll just have to build a better map than the one in your head!",
    "I'm gonna be the man who becomes the Pirate King!",
    "I'll gather a crew of strong and loyal friends to sail with me!",
    "If you're gonna become a fish, become a big fish!",
    "I don't care about treasure or fame. I just want to have the greatest adventures!",
    "I don't need a plan. I'll figure things out as I go!",
    "If you don't fight, you can't win!",
    "I'll make allies out of my enemies. Everyone deserves a second chance!",
    "I'll always stand up for what's right, even if it means going against the world!",
    "I don't need a reason to help someone.",
    "I'm gonna be the pirate king!",
    "I don't care if I die... as long as I protect my friends, I'm okay with that!",
    "The difference between a weak person and a strong person is how they use their power.",
    "Being alone is more painful than getting hurt.",
    "I'll never betray my crew. We're a family, and we'll stick together!",
    "The thing called justice changes its shape... depending on where you stand.",
    "If you don't put your life on the line, you can't call it a challenge!",
    "Heroes are those who share their meat!",
    "No matter how many hundreds of weapons or armor one is equipped with, they are no match for that one special spear that comes from your guts.",
    "If you don't risk your life, you can't create a future. Right?",
    "I can't just give up... I can't just keep running away!",
    "Inherited Will, The Destiny of the Age, and The Dreams of the People. As long as people continue to pursue the meaning of Freedom, these things will never cease to be!",
    "I'll protect my friends no matter what. They're like family to me!",
    "I'll never let anyone tell me what I can or cannot do. I'll decide my own limits!",
    "I'll bring freedom to those who are oppressed. That's the duty of a true pirate!",
    "The weak don't get to decide anything, not even how they die.",
    "If you don't want to regret your life, then don't let anyone take away your dream.",
    "The dreams of pirates will never end!",
    "I'll never give up, no matter how many times I get knocked down. I'll always get back up!",
    "I'll enjoy every moment of my journey. Life is an adventure!",
    "I'll make my mark on the world and leave a legacy that will be remembered!",
    "I don't wanna live a thousand years. If I just live through today, that'll be enough.",
    "People don't fear god, fear itself is god!",
    "I'll never lose my sense of wonder and excitement. Every day is a new adventure!",
    "If you don't fight, you can't win!",
    "I'll always be true to myself, even if it means going against the expectations of others!",
    "I'll never let fear hold me back. I'll face any challenge with courage and determination!",
    "I'll prove that the power of friendship can conquer anything!",
    "I'll never let anyone break my spirit. I'm unbreakable!",
    "I'll follow my instincts and trust my gut. They've never led me astray!",
    "I'll always lend a helping hand to those in need. That's what a true pirate does!",
    "I'll never lose my sense of humor, even in the face of danger!",
    "I'll always keep moving forward, no matter how many obstacles are in my way!",
    "I'll never let anyone control or manipulate me. I'm my own person!",
    "I'll live my life to the fullest, without any regrets!",
    "I'll always find a way, even when it seems impossible!",
    "I'll never stop dreaming, because dreams have the power to change the world!",
    "I'll always cherish the bonds I have with my friends. They're the most valuable treasure!",
    "I'll never forget where I came from and the people who have supported me!",
    "I'll always be grateful for the adventures and experiences that have shaped me!",
    "I'll never lose my sense of wonder and curiosity. The world is full of endless possibilities!",
    "I'll always believe in the goodness of people, even if they've made mistakes!",
    "I'll never let anyone underestimate me. I'm capable of greatness!",
    "I'll always follow my instincts and trust my gut. They've never led me astray!",
    "I'll never let anyone break my spirit. I'm unbreakable!",
    "I'll always lend a helping hand to those in need. That's what a true pirate does!",
    "I'll never lose my sense of humor, even in the face of danger!",
    "I'll always keep moving forward, no matter how many obstacles are in my way!",
    "I'll never let anyone control or manipulate me. I'm my own person!",
    "I'll live my life to the fullest, without any regrets!",
    "I'll always find a way, even when it seems impossible!",
    "I'll never stop dreaming, because dreams have the power to change the world!",
    "I'll always cherish the bonds I have with my friends. They're the most valuable treasure!",
    "I'll never forget where I came from and the people who have supported me!",
    "I'll always be grateful for the adventures and experiences that have shaped me!",
    "I'll never lose my sense of wonder and curiosity. The world is full of endless possibilities!",
    "I'll always believe in the goodness of people, even if they've made mistakes!",
    "I'll never let anyone underestimate me. I'm capable of greatness!",
    "I'll always follow my instincts and trust my gut. They've never led me astray!",
    "I'll never let anyone break my spirit. I'm unbreakable!",
    "I'll always lend a helping hand to those in need. That's what a true pirate does!",
    "I'll never lose my sense of humor, even in the face of danger!",
    "I'll always keep moving forward, no matter how many obstacles are in my way!",
    "I'll never let anyone control or manipulate me. I'm my own person!",
    "I'll live my life to the fullest, without any regrets!",
    "I'll always find a way, even when it seems impossible!",
    "I'll never stop dreaming, because dreams have the power to change the world!",
    "I'll always cherish the bonds I have with my friends. They're the most valuable treasure!",
    "I'll never forget where I came from and the people who have supported me!",
    "I'll always be grateful for the adventures and experiences that have shaped me!",
    "I'll never lose my sense of wonder and curiosity. The world is full of endless possibilities!",
    "I'll always believe in the goodness of people, even if they've made mistakes!",
    "I'll never let anyone underestimate me. I'm capable of greatness!",
    "I'll always follow my instincts and trust my gut. They've never led me astray!",
    "I'll never let anyone break my spirit. I'm unbreakable!",
    "I'll always lend a helping hand to those in need. That's what a true pirate does!",
    "I'll never lose my sense of humor, even in the face of danger!",
    "I'll always keep moving forward, no matter how many obstacles are in my way!",
    "I'll never let anyone control or manipulate me. I'm my own person!",
    "I'll live my life to the fullest, without any regrets!",
    "I'll always find a way, even when it seems impossible!",
    "I'll never stop dreaming, because dreams have the power to change the world!",
    "I'll always cherish the bonds I have with my friends. They're the most valuable treasure!",
    "I'll never forget where I came from and the people who have supported me!",
    "I'll always be grateful for the adventures and experiences that have shaped me!",
    "I'll never lose my sense of wonder and curiosity. The world is full of endless possibilities!",
    "I'll always believe in the goodness of people, even if they've made mistakes!",
    "I'll never let anyone underestimate me. I'm capable of greatness!",
    "I'll always follow my instincts and trust my gut. They've never led me astray!",
    "I'll never let anyone break my spirit. I'm unbreakable!",
    "I'll always lend a helping hand to those in need. That's what a true pirate does!",
    "I'll never lose my sense of humor, even in the face of danger!",
    "I'll always keep moving forward, no matter how many obstacles are in my way!",
    "I'll never let anyone control or manipulate me. I'm my own person!",
    "I'll live my life to the fullest, without any regrets!",
    "I'll always find a way, even when it seems impossible!",
    "I'll never stop dreaming, because dreams have the power to change the world!",
    "I'll always cherish the bonds I have with my friends. They're the most valuable treasure!",
    "I'll never forget where I came from and the people who have supported me!",
    "I'll always be grateful for the adventures and experiences that have shaped me!",
    "I'll never lose my sense of wonder and curiosity. The world is full of endless possibilities!",
    "I'll always believe in the goodness of people, even if they've made mistakes!",
    "I'll never let anyone underestimate me. I'm capable of greatness!",
    "I'll always follow my instincts and trust my gut. They've never led me astray!",
    "I'll never let anyone break my spirit. I'm unbreakable!",
    "I'll always lend a helping hand to those in need. That's what a true pirate does!",
    "I'll never lose my sense of humor, even in the face of danger!",
    "I'll always keep moving forward, no matter how many obstacles are in my way!",
    "I'll never let anyone control or manipulate me. I'm my own person!",
    "I'll live my life to the fullest, without any regrets!",
    "I'll always find a way, even when it seems impossible!",
    "I'll never stop dreaming, because dreams have the power to change the world!",
    "I'll always cherish the bonds I have with my friends. They're the most valuable treasure!",
    "I'll never forget where I came from and the people who have supported me!",
    "I'll always be grateful for the adventures and experiences that have shaped me!",
    "I'll never lose my sense of wonder and curiosity. The world is full of endless possibilities!",
    "I'll always believe in the goodness of people, even if they've made mistakes!",
    "I'll never let anyone underestimate me. I'm capable of greatness!",
    "I'll always follow my instincts and trust my gut. They've never led me astray!",
    "I'll never let anyone break my spirit. I'm unbreakable!",
    "I'll always lend a helping hand to those in need. That's what a true pirate does!",
    "I'll never lose my sense of humor, even in the face of danger!",
    "I'll always keep moving forward, no matter how many obstacles are in my way!",
    "I'll never let anyone control or manipulate me. I'm my own person!",
    "I'll live my life to the fullest, without any regrets!",
    "I'll always find a way, even when it seems impossible!",
    "I'll never stop dreaming, because dreams have the power to change the world!",
    "I'll always cherish the bonds I have with my friends. They're the most valuable treasure!",
    "I'll never forget where I came from and the people who have supported me!",
    "I'll always be grateful for the adventures and experiences that have shaped me!",
    "I'll never lose my sense of wonder and curiosity. The world is full of endless possibilities!",
    "I'll always believe in the goodness of people, even if they've made mistakes!",
    "I'll never let anyone underestimate me. I'm capable of greatness!",
    "I'll always follow my instincts and trust my gut. They've never led me astray!",
    "I'll never let anyone break my spirit. I'm unbreakable!",
    "I'll always lend a helping hand to those in need. That's what a true pirate does!",
    "I'll never lose my sense of humor, even in the face of danger!",
    "I'll always keep moving forward, no matter how many obstacles are in my way!",
    "I'll never let anyone control or manipulate me. I'm my own person!",
    "I'll live my life to the fullest, without any regrets!",
    "I'll always find a way, even when it seems impossible!",
    "I'll never stop dreaming, because dreams have the power to change the world!",
    "I'll always cherish the bonds I have with my friends. They're the most valuable treasure!",
    "I'll never forget where I came from and the people who have supported me!",
    "I'll always be grateful for the adventures and experiences that have shaped me!",
    "I'll never lose my sense of wonder and curiosity. The world is full of endless possibilities!",
    "I'll always believe in the goodness of people, even if they've made mistakes!",
    "I'll never let anyone underestimate me. I'm capable of greatness!",
    "I'll always follow my instincts and trust my gut. They've never led me astray!",
    "I'll never let anyone break my spirit. I'm unbreakable!",
    "I'll always lend a helping hand to those in need. That's what a true pirate does!",
    "I'll never lose my sense of humor, even in the face of danger!",
    "I'll always keep moving forward, no matter how many obstacles are in my way!",
    "I'll never let anyone control or manipulate me. I'm my own person!",
    "I'll live my life to the fullest, without any regrets!",
    "I'll always find a way, even when it seems impossible!",
    "I'll never stop dreaming, because dreams have the power to change the world!",
    "I'll always cherish the bonds I have with my friends. They're the most valuable treasure!",
    "I'll never forget where I came from and the people who have supported me!",
    "I'll always be grateful for the adventures and experiences  that have shaped me!",
    "I'll never lose my sense of wonder and curiosity. The world is full of endless possibilities!",
    "I'll always believe in the goodness of people, even if they've made mistakes!",
    "I'll never let anyone underestimate me. I'm capable of greatness!",
    "I'll always follow my instincts and trust my gut. They've never led me astray!",
    "I'll never let anyone break my spirit. I'm unbreakable!",
    "I'll always lend a helping hand to those in need. That's what a true pirate does!",
    "I'll never lose my sense of humor, even in the face of danger!",
    "I'll always keep moving forward, no matter how many obstacles are in my way!",
    "I'll never let anyone control or manipulate me. I'm my own person!",
    "I'll live my life to the fullest, without any regrets!",
    "I'll always find a way, even when it seems impossible!",
    "I'll never stop dreaming, because dreams have the power to change the world!",
    "I'll protect my friends no matter what! That's what being a pirate means to me!"
    "Bring it on! Ill take all the pain and the suffering, and smile through it all!"
    "There's no such thing as being born into this world to be alone!",
    "I don't want to have any regrets! I want to be able to say that I did everything I could!",
    "I'm not a hero! I'm a pirate!",
    "I'll never forgive anyone who lays a hand on my friends!"
    "I'll never give up, no matter what!",
    "I'll find a way to become stronger, no matter what!",
    "I'll make my dream a reality, even if it means defying the whole world!",
    "I'll go as far as I have to, to protect what's important to me!",
    "I don't need a map to tell me where to go. I follow my instincts!",
    "I'll never be able to repay all the things my friends have done for me!",
    "I'm not a hero, but I have the power to stand up for what I believe in!",
    "I'll create a bond with my crew that's stronger than anything!",
    "I'll never be satisfied until I've seen everything the world has to offer!",
    "I'll keep searching for the One Piece until the day I die!"
]
    
  


# List of Zoro quotes
zoro_quotes = [
    "Nothing... Nothing at all...",
    "Nothing happened",
    "I don't know. I don't have any regrets.",
    "If I die here, then I'm a man that could only make it this far.",
    "If I can't even protect my captain's dream, then whatever ambition I have is nothing but talk!",
    "People's dreams... Don't ever forget them. I repeat, don't... ever... forget them!",
    "The wound that a swordsman receives... Cannot be healed so easily!",
    "I don't care what the society says. I've never regretted doing anything. I will survive, no matter what occurs and do what I want!",
    "Cutting steel... It ain't easy... But I won't lose!",
    "Don't ever mock a swordsman's pride!",
    "The one thing I learned from losing... Is that I never want to lose again!",
    "I'll never be a swordsman like Mihawk if I can't cut this!",
    "You need to accept the fact that you're not the best and have all the will to strive to be better than anyone you face.",
    "There's no need for words. Just let me through.",
    "What's important isn't the sword. It's the person holding the sword.",
    "My sword is the only power I've got!",
    "I won't lose... Not ever again!",
    "A swordsman's strength isn't measured by his size.",
    "I'm not the one who's gonna die here!",
    "A true swordsman has no power other than his sword.",
    "If you kill me, I'll revive and defeat you!",
    "My dream... Won't die here!",
    "Hmph. Aren’t titles useless when it comes to fighting? The stronger one wins, that’s all.",
    "In a real fight there is no man or woman! If you don’t fight with your real power, that will be the most shameful thing.",
    "Only those who have suffered long, can see the light within the shadows.",
    "When the world shoves you around, you just gotta stand up and shove back. It’s not like somebody’s gonna save you if you start babbling excuses.",
    "If it’s a fight he wants, then I won’t back down.",
    "Either in belief or doubt, if I lean to one of these sides, my reaction time will be dulled if my heart thinks the opposite of what I choose.",
    "I do things my own way! So don’t give me any lip about it!",
    "I will surpass Mihawk... I must surpass him!",
    "I won't die... because I'm going to be the world's greatest swordsman!",
    "So, are you stupid enough to fall for such a stupid trap that such stupid people set up?",
    "A scar on the back is the greatest shame for a swordsman.",
    "My captain... will be the Pirate King!",
    "Bring on the hardship. It’s preferred in a path of carnage.",
    "I’m going to be the world’s greatest swordsman! All I have left is my destiny! My name may be infamous…but it’s gonna shake the world!!!",
    "Only I can call my dream stupid!",
    "What does ‘teamwork’ really mean, anyway? Is it just about rescuing or protecting each other? There are people who believe that. But to me, it just sounds like kids playing around.",
    "You’ll never understand…your swords will never be as heavy as mine!",
    "Being caught off guard could cost us our lives from now on!",
    "A crew with no respect and a captain that doesn’t demand it falls apart quickly.",
    "If you've never tried, you'll never know. Anyway, we're gonna die! Why don't we try our best?",
    "I’ll become stronger for her! Until my name reaches Heaven itself… I’ll become stronger!… I’ll become the strongest swordsman in the world!",
    "I won't run away... I WON'T!",
    "I don't want to be a hero. I want to be a swordsman!",
    "The path of a swordsman is one of eternal uncertainty.",
    "I don't need a map. I'm going to be the world's greatest swordsman!",
    "I've set a course towards my dream!",
    "The fact that you can fight better as a giraffe… and the fact that you can use four swords… are all completely irrelevant… when you’re FACING ME!",
    "I don’t know. I’m not sure why myself. But if I were to take even one step back, I believe that all those important oaths, promises and many other deals till now, will all go to waste and I’ll never be able to return before you, ever again.",
    "The difference between a weakling and a hero is one twist of fate!",
    "I'm not lost. The path has been closed off.",
    "It's not enough to live. You need something to protect.",
    "Don't compare me to the others. I'm nobody else but myself!",
    "If you do anything that would cause me to abandon my ambitions… You will end your own life on my sword!",
    "Over the nine mountains, across the eight seas, there is nothing I cannot cut.",
    "Well, how about this. My luck versus this thing’s curse… wanna see what’s stronger…? If I lose, then I’m just that much of a man anyways…",
    "When you decided to go to the sea, it was your own decision. Whatever happens to you on the sea, it depends on what you’ve done! Don’t blame others!",
    "If I lose to someone as pitiful as you, with such a small injury… my fate is already sealed.",
    "If you do anything that would cause me to abandon my ambitions… You will end your own life on my sword!",
    "A real man never goes back on his words.",
    "There's no need for the weak to linger. You're only in the way.",
    "I'll never lose... Not until I meet that swordsman!",
    "Strength isn't just about winning. Even if my attempts are pathetic and futile, as long as I'm doing it with my own strength, that's enough for me!",
    "Being strong isn't just about having power or move. It about one's spirit.",
    "As long as you don't lose, you haven't been defeated. No matter how long it takes, I will wait for my chance.",
    "In case we become candles, I want to have a nice pose",
    "You want to kill me? You couldn’t even kill my boredom!",
    "I’m sorry. I never pray to god.",
    "You’ve underestimated me, snow woman. When you thought you couldn’t beat me, you should have run. Of course, there are things that I don’t wanna cut. But… let me ask you something. Have you ever seen a fierce animal you were sure would never bite? Because I haven’t.",
    "Fine! I’d rather be a pirate than die here!",
    "You sure can talk the talk, but you’re not quite ready to walk the walk. Time’s up, it’s my turn.",
    "A wound that’d make an ordinary man unconscious… I won’t lose to it. A wound that would kill an ordinary person… I won’t lose to it! To face one who is extraordinary, Hawk Eyes… I can’t allow myself to be ordinary!",
    "When I decided to follow my dream, I had already discarded my life.",
    "The thing called \"strength\" is meaningless. There is only a way to protect the people you care about."
]

nami_quotes = [
        "I don't need a map to know where I'm going!",
        "Money is power!",
        "I'll do anything to protect my dream!",
        "I won't let anyone control my fate!",
        "I'll use my charm and wit to get what I want!",
        "There's nothing wrong with dreaming of a better future!",
        "I won't let anyone take advantage of me!",
        "I'll navigate my own path in life!",
        "I'll prove that I'm more than just a pretty face!",
        "I won't let anyone underestimate me!",
        "I'll fight for what's right, no matter the cost!",
        "I'll make my own destiny!",
        "I won't be tied down by anyone or anything!",
        "I'll use my intelligence to outsmart any opponent!",
        "I'll always be there for my friends, no matter what!",
        "I won't let fear hold me back!",
        "I'll find a way to achieve my dreams, even in the face of adversity!",
        "I won't let anyone stand in the way of my goals!",
        "I'll never forget the importance of loyalty and trust!",
        "I'll make sure no one takes advantage of my crew!",
        "I won't let anyone tear down my dreams!",
        "I'll always strive to be the best navigator in the world!",
        "I won't let my past define me!",
        "I'll prove that I'm more than just a thief!",
        "I won't let anyone break my spirit!",
        "Who needs a treasure map when I have a shopping list?",
        "I may not have haki, but my bargaining skills are unbeatable!",
        "I have a PhD in financial planning and a black belt in coupon cutting.",
        "My navigation skills are so good, I once convinced a sea turtle to give me a piggyback ride.",
        "Why fight with swords when I can defeat enemies with my deadly glare during sales?",
        "I'm the master of creating storms in both the weather and the clearance section.",
        "I may not have a devil fruit power, but I can still make wallets disappear with my shopping spree!",
        "I have a sixth sense for finding hidden discounts. It's called 'Nami-sense.'",
        "When it comes to budgeting, I could rival a marine admiral in precision.",
        "I once navigated through a maze of clothes racks faster than Luffy can eat a meat bun!",
        "Don't underestimate the power of my glare. It can make even the most stubborn merchant lower their prices.",
        "I can survive storms at sea, but I'm helpless when it comes to untangling earphones.",
        "I have a shopping list longer than Sanji's love letter collection."
]



usopp_quotes = [
        "Hey, did I ever tell you about the time I fought a giant sea serpent?",
        "I once tamed a wild sea turtle and rode it across the waves. It was the fastest ride of my life!",
        "You know, being a sniper requires not only accuracy but also patience. I can wait for hours for the perfect shot!",
        "I've got a whole bag of tricks that can turn the tide of any battle. It's all about strategy!",
        "I once convinced an entire village that I was their long-lost prince. They treated me like royalty for a week!",
        "You won't believe the epic battles I've imagined in my head. Sometimes reality can't keep up with my imagination!",
        "I've got a nose for danger. I can sense trouble from miles away!",
        "I once built a makeshift catapult out of bamboo and launched myself onto a pirate ship. It was the grandest entrance ever!",
        "You see these goggles? They're not just for show. They enhance my vision and help me spot enemies from afar!",
        "I've got the instincts of a true adventurer. I can navigate through uncharted territories with ease!",
        "I once convinced an entire crew of pirates to join the Straw Hat Pirates. It's all about the power of persuasion!",
        "You won't believe the epic stories I've told around the campfire. I can make even the most mundane tales sound thrilling!",
        "I've got the reflexes of a cat. I can dodge attacks with lightning speed!",
        "I once built a hot air balloon out of old sails and flew above the clouds. The view was breathtaking!",
        "You know, being a sniper is not just about hitting the target. It's about knowing when not to shoot and when to strike with precision!",
        "I've got a knack for creating distractions. I can divert the enemy's attention and give my crewmates the upper hand!",
        "I once single-handedly took down a pirate crew using nothing but my slingshot and a bag of marbles. They never saw it coming!",
        "You see this bandana? It's not just a fashion statement. It's a symbol of my determination and the spirit of the Straw Hat Pirates!",
        "I've got the imagination of a true dreamer. I can envision a world where anything is possible!",
        "I once built a working cannon out of bamboo and used it to launch fireworks during a celebration. It was a blast!",
        "You won't believe the disguises I've pulled off. I can blend into any crowd and go unnoticed!",
        "I once convinced a pirate captain to surrender just by staring him down with my fearless gaze.",
        "You know, being a sniper is not just about hitting targets. It's about creating opportunities and changing the course of battles!",
        "I've got an endless supply of tricks up my sleeve. You never know what I'll come up with next!",
        "I once scared away a whole crew of marines just by making funny faces at them. Who says laughter can't be a weapon?",
        "I may not have the brawn of the others, but I've got the brains to outsmart any opponent!",
        "I've got the heart of a true pirate. I'll never back down from a challenge, no matter how tough it may seem!",
        "You see this slingshot? It may look like a toy, but in my hands, it becomes a deadly weapon.",
        "I may not be the captain, but I've got the spirit of a leader. I'll always rally my crewmates and inspire them to greatness!",
        "I've got a wild imagination that can turn even the most ordinary situations into epic adventures!",
        "You won't believe the tall tales I've spun. I can make even the most unbelievable stories sound convincing!",
        "I've got the ability to see potential in things that others overlook. That's how I find hidden treasures and untapped resources!",
        "I once built a makeshift raft out of nothing but driftwood and sailed it across the sea. Who needs a fancy ship?",
        "I've got the determination of a thousand warriors. I'll never give up on my dreams, no matter the obstacles!",
        "You know, sometimes it's not about winning the fight. It's about standing up for what you believe in, even in the face of certain defeat.",
        "I've got the soul of a true adventurer. I'm always seeking the next thrilling challenge and the chance to make my mark in history!",
        "You see that island over there? I once tamed a ferocious beast that lived there... well, in my dreams, at least.",
        "I may not have the physical strength, but I've got the courage to face any danger head-on!",
        "I've got the power of persuasion. I can talk my way out of any sticky situation... most of the time.",
        "You know, being a sniper is not just about taking down enemies from afar. It's about protecting my crew and creating a safe path for us!",
        "I've got a knack for getting myself into unbelievable situations. But hey, that's what makes life exciting!",
        "I once scared away a whole crew of pirates just by shouting at them!",
        "You know, I'm not afraid of anything... well, except for maybe spiders.",
        "I can shoot my slingshot with incredible accuracy, even blindfolded!",
        "I've got an idea! How about we disguise ourselves as sea monsters to scare off our enemies?",
        "I've invented this amazing device that can create smoke screens. It's perfect for sneaky escapes!",
        "You won't believe the size of the fish I caught last time! It was as big as a ship!",
        "I've got a story so amazing, you'll think I made it up... but I promise, it's all true!",
        "Who needs superpowers when you've got a sharp wit and an incredible imagination like mine?",
        "I can make anyone believe anything with my incredible storytelling skills!",
        "I once single-handedly took down an entire battalion of marines... in my dreams.",
        "I'm not just a sniper, I'm an artist. My slingshot is my paintbrush, and the battlefield is my canvas!",
        "I've got a plan that's so foolproof, it's practically guaranteed to work... maybe.",
        "Did you know I can run faster than the wind? Well, at least that's what I tell everyone.",
        "I've got the heart of a lion, the courage of a warrior, and the... oh, who am I kidding? I'm just really good at running away!",
        "I've got the spirit of a true adventurer! I'm always ready to explore new islands and discover hidden treasures.",
        "You see that mountain over there? I once climbed to the top and planted the Straw Hat flag... in my dreams, of course.",
        "I may not be the strongest fighter, but I make up for it with my incredible bravery... and a little bit of luck.",
        "I've got a knack for getting myself into trouble, but I always manage to find a way out of it!",
        "You know what they say, a good scare can be just as effective as a punch in the face!",
    ]
    

sanji_quotes = [
        "I am the prince of cooking! No one can surpass my culinary skills!",
        "A true chef treats their ingredients with love and respect. Every dish I create is a work of art!",
        "I'll make sure every meal I prepare is a feast fit for the gods!",
        "I'll use my kicks to protect those in need and defend the honor of the Straw Hat Pirates!",
        "I won't let anyone disrespect the ladies. Chivalry is my code!",
        "I've got a whole collection of secret recipes that will blow your taste buds away!",
        "I'll never compromise on the quality of my food. Perfection is the only option!",
        "I'll show you the true meaning of passion in the kitchen!",
        "I won't let anyone go hungry. My cooking will nourish both body and soul!",
        "I'll make sure every dish I create is infused with love and a touch of spice!",
        "I've got an eye for beauty, whether it's in the kitchen or in the form of a lovely lady!",
        "I'll dance across the battlefield, delivering devastating kicks to my enemies!",
        "I'll make sure every meal is a celebration. Food is meant to be enjoyed!",
        "I won't let anyone tarnish the reputation of the Straw Hat Pirates. I'll fight to protect our honor!",
        "I'll create flavors that will transport you to another world. Prepare to be amazed!",
        "I'll use my quick wit and charm to win the hearts of both friends and foes!",
        "I won't let anyone stand in the way of my dreams. I'll reach the pinnacle of the culinary world!",
        "I'll make sure every bite of my food is an unforgettable experience!",
        "I'll protect my crewmates with everything I've got. No harm shall come to them!",
        "I'll bring a touch of elegance and class to everything I do. I am a gentleman!",
        "I won't let anyone ruin a perfectly good meal. Food is sacred!",
        "I'll create dishes that will make you weep with joy. Prepare to taste perfection!",
        "I'll fight with all my might, but I'll never lay a hand on a lady. That's the mark of a true gentleman!",
        "I'll show you the true artistry of cooking. It's not just about taste, but also presentation and ambiance!",
        "I won't let anyone go hungry. I'll feed the world with my culinary creations!",
         "I can't resist the call of the sea and the taste of adventure!",
        "Every meal I create is a masterpiece that will make your taste buds sing!",
        "I'll charm the socks off anyone who crosses my path. I'm the ladies' man!",
        "I'll cook up a storm that will leave you begging for more!",
        "I'll fight with all my heart to protect the ones I hold dear!",
        "I'll bring a touch of elegance and flair to every dish I prepare!",
        "I won't let anyone go hungry. I'll provide nourishment and happiness to all!",
        "I'll sweep you off your feet with my impeccable style and grace!",
        "I'll kick my way through any obstacle that stands in my path!",
        "I'll serve up a meal that will transport you to paradise!",
        "I'll never let anyone tarnish the name of the Straw Hat Pirates!",
        "I'll treat every ingredient with the utmost respect and care!",
        "I'll create flavors that will ignite your senses and awaken your soul!",
        "I'll protect the weak and stand up for justice!",
        "I'll show you the power of a well-seasoned dish. It can change the world!",
        "I'll dazzle you with my culinary skills and leave you in awe!",
        "I'll make sure every plate is a work of art that reflects my passion!",
        "I'll use my wit and charm to win the hearts of both friends and enemies!",
        "I'll never back down from a challenge. I'll face adversity with a smile!",
        "I'll create a feast that will bring people together and forge lifelong bonds!",
        "I'll dance across the kitchen, infusing every dish with my love and passion!",
        "I'll protect my crewmates with every fiber of my being. I'll never let them down!",
        "I'll prove that cooking is more than just a skill. It's an art form!",
        "I'll fight for the dreams of my friends and ensure their happiness!",
        "I'll create flavors that will leave you speechless and craving for more!",
        "I'll never let anyone underestimate the power of a well-prepared meal!",
        "I'll use my culinary expertise to outsmart any opponent!",
        "I'll make sure every bite is a journey to culinary bliss. Bon appétit!",
        "I'll show you the true meaning of hospitality and generosity!"
    ]


jimbei_quotes = [
        "The sea is vast and full of mysteries. It humbles us and teaches us respect.",
        "The bonds between friends are unbreakable. We support and protect each other.",
        "I have learned that true strength lies not in power alone, but in compassion and understanding.",
        "As a helmsman, I navigate through life's challenges and guide my crew to safety.",
        "I have seen the atrocities of the world, but I still believe in the potential for peace and harmony.",
        "I will fight for justice and strive to create a world where everyone can live in harmony.",
        "I carry the weight of my past actions, but I will atone for my sins and make amends.",
        "My loyalty lies with my crew and those I hold dear. I will never betray their trust.",
        "In the face of adversity, I remain calm and resolute. I will not waver in my convictions.",
        "I understand the pain and suffering caused by prejudice. I will stand up against discrimination.",
        "I have witnessed the destructive power of hatred. I will work towards fostering understanding and unity.",
        "I believe in the inherent goodness of humanity. We have the capacity to change and grow.",
        "I will use my strength to protect the weak and ensure a brighter future for generations to come.",
        "I have dedicated my life to the sea and its creatures. I will be their voice and advocate for their well-being.",
        "I have made mistakes in the past, but I will continue to learn and grow as a person.",
        "I will honor the legacy of those who came before me and carry their teachings with me.",
        "I strive to find balance in all aspects of life. It is the key to inner peace and harmony.",
        "I have learned that true strength comes from the heart. It is the driving force behind my actions.",
        "I will never forget the sacrifices made by my comrades. Their memory fuels my determination.",
        "I will navigate the treacherous waters of life with courage and resilience. Nothing will deter me.",
        "I believe in the power of forgiveness and second chances. It is through redemption that we find true peace.",
        "I will stand up against injustice and fight for the rights of all beings, regardless of their race or species.",
        "I will lend a helping hand to those in need and strive to make a positive impact in the world.",
        "I carry the weight of the sea in my heart. Its vastness reminds me of the limitless possibilities of life.",
        "I believe in the power of unity. Together, we can overcome any obstacle and achieve greatness.",
        "I will honor my duty as a helmsman and steer my crew towards a future filled with hope and freedom.",
        "I will never forget the lessons learned from the sea. Its wisdom guides my actions and decisions.",
        "The sea is both a source of life and a formidable force. It demands our respect and caution.",
        "I have witnessed the cycle of hatred and violence. I will work towards breaking that cycle and promoting peace.",
        "As a fishman, I carry the weight of my people's history and strive to build bridges of understanding.",
        "I will use my strength to protect the weak and ensure justice prevails in the world.",
        "I believe in the potential for growth and change. It is never too late to make amends and seek redemption.",
        "I have learned that true strength lies in one's character and the choices they make.",
        "I will not be swayed by the currents of prejudice. I will judge others based on their actions, not their race.",
        "I carry the teachings of my predecessors with me. Their wisdom guides my path.",
        "I will lend my voice to the voiceless and fight for the rights of all beings, regardless of their origins.",
        "I have learned the importance of sacrifice. I will willingly give up my own happiness for the greater good.",
        "I believe in the power of unity and cooperation. Together, we can overcome any obstacle.",
        "I will face my past with honesty and confront the consequences of my actions. Only then can I find true peace.",
        "I will use my position and influence to advocate for equality and fight against discrimination.",
        "I carry the spirit of the sea within me. It fuels my resolve and strengthens my determination.",
        "I will not let fear hold me back. I will embrace challenges and grow stronger with each obstacle.",
        "I believe in the potential for change within each individual. We all have the capacity for growth.",
        "I will use my skills and experience to navigate the turbulent waters of life. I will not be deterred.",
        "I have seen the destructive power of hatred. I will work towards fostering understanding and compassion.",
        "I will protect the weak and defend the innocent. I will be a shield against injustice.",
        "I carry the weight of my comrades' dreams on my shoulders. I will fulfill their aspirations in their honor.",
        "I will strive for balance in all things. It is the key to harmony and inner peace.",
        "I believe in the inherent goodness of humanity. We all have the potential to change and make a difference.",
        "I will not let the sins of the past define me. I will carve my own path towards redemption.",
        "I will use my knowledge and wisdom to guide others and help them find their way.",
        "I will honor the legacy of my people and work towards a future where fishmen and humans can coexist in harmony.",
        "I will not stand idly by in the face of injustice. I will take action and fight for what is right.",
        "I will be a beacon of hope in the darkness, guiding others towards a better tomorrow.",
        "I believe in the power of forgiveness. It is through forgiveness that we can heal and move forward.",
        "I will navigate the treacherous waters of life with strength and resilience. I will never give up."
    ]


robin_quotes = [
        "Knowledge is power. I seek knowledge above all else.",
        "The history of the world is a tapestry of mysteries waiting to be unraveled.",
        "I have spent my life searching for the truth and unraveling the secrets of the world.",
        "The Poneglyphs hold the key to uncovering the true history of the world.",
        "I am the archaeologist of the Straw Hat Pirates. My name is Nico Robin.",
        "I have seen the darkest depths of the world and emerged stronger.",
        "I have faced countless dangers and obstacles in my pursuit of knowledge.",
        "I am always curious and eager to learn. There is so much I have yet to discover.",
        "I have learned to be cautious and observant. Trust is not easily earned.",
        "I value the power of intellect and reason. It is a weapon that can change the world.",
        "I will use my knowledge to protect my friends and uncover the mysteries that lie before us.",
        "I have been branded a criminal for seeking the truth. But I will not be silenced.",
        "I have lost everything once before. I will not let history repeat itself.",
        "I have learned that true strength lies not in physical power, but in the strength of one's convictions.",
        "I am not easily swayed by emotions. I analyze situations with a cool and logical mind.",
        "I have seen the beauty and brutality of the world. It is a delicate balance.",
        "I have faced betrayal and heartache, but I have also found friendship and hope.",
        "I will not shy away from the darkness. I will confront it head-on and bring it to light.",
        "I am a survivor. I have overcome unimaginable hardships and emerged stronger.",
        "I have learned to appreciate the value of life and the fleeting nature of existence.",
        "I will not be confined by the expectations of others. I am my own person, with my own dreams.",
        "I have been called a demon, but I know that labels cannot define who I am.",
        "I have found solace in the company of my Nakama. Together, we are unstoppable.",
        "I have seen the destructive power of knowledge. It can be a double-edged sword.",
        "I will use my skills as an archaeologist to preserve the history and culture of the world.",
        "I have embraced my past and accepted the choices I have made. They have shaped who I am today.",
        "I have learned that there is strength in vulnerability. Opening up to others is not a sign of weakness.",
        "I am not afraid of the unknown. It is the unknown that holds the greatest discoveries.",
        "I have dedicated my life to unraveling the mysteries of the Void Century. The truth must be known.",
        "The world is full of wonders and secrets waiting to be discovered.",
        "Every piece of knowledge I uncover is a piece of the puzzle that brings us closer to the truth.",
        "I believe in the power of history. It shapes our present and guides our future.",
        "I have dedicated my life to studying the ancient civilizations that have shaped our world.",
        "I am fascinated by the complexities of human nature and the stories that lie within every person.",
        "I have witnessed the beauty of the world, but I have also seen its darkest corners.",
        "I have learned that true strength comes from understanding and empathy.",
        "I find solace in the pages of books, where I can travel through time and unravel the mysteries of the past.",
        "I am a seeker of knowledge, always hungry for new discoveries and understanding.",
        "I have faced loneliness and isolation, but I have also found companionship and a sense of belonging.",
        "I believe that knowledge should be shared, for it has the power to change the world.",
        "I have learned that the truth can be a double-edged sword, capable of both liberation and destruction.",
        "I am not afraid to challenge the status quo and question the narratives that have been handed down to us.",
        "I have come to understand that history is not just a record of events, but a reflection of power and ideology.",
        "I am driven by a deep curiosity, a thirst to uncover the secrets that have been buried and forgotten.",
        "I have seen the consequences of ignorance and the dangers of allowing history to repeat itself.",
        "I believe in the importance of preserving cultural heritage and protecting the knowledge of the past.",
        "I have learned that the pursuit of knowledge is not always easy, but it is always worth it.",
        "I am constantly amazed by the resilience and strength of the human spirit in the face of adversity.",
        "I have come to appreciate the value of trust and the bonds that can be formed through shared experiences.",
        "I believe that everyone has a story to tell, and that every story is worth listening to.",
        "I have learned that true freedom is not just the absence of chains, but the ability to think and question.",
        "I am committed to fighting for justice and exposing the injustices that have been hidden from view.",
        "I have found a home among the Straw Hat Pirates, a family that accepts and values me for who I am.",
        "I believe in the power of hope and the possibility of a better future, even in the face of darkness.",
        "I have learned that true knowledge is not found in books alone, but in the experiences and wisdom of others.",
        "I am driven by a sense of responsibility to uncover the truth and ensure that history is not forgotten.",
        "I believe that every person has the right to access knowledge and to have their voice heard.",
        "I have come to understand that the past is not something to be feared, but something to be embraced and learned from.",
        "I am a student of the world, constantly seeking to expand my understanding and challenge my own assumptions."
    ]


brook_quotes = [
        "Yohoho! I am the soulful musician of the Straw Hat Pirates, Brook!",
        "I have walked a long and lonely path, but now I have found my place with my Nakama.",
        "I may be a skeleton, but my spirit and passion for music are as lively as ever!",
        "I'll play my beloved violin and bring joy to everyone's hearts!",
        "I have a skull for a head, but don't let that scare you. I'm a friendly skeleton!",
        "I have witnessed the passing of many years, but my soul remains young and full of life.",
        "I'll serenade you with my soulful melodies that will touch your heart and lift your spirits!",
        "I've faced death and embraced life. Every moment is precious to me.",
        "I'll use my sword skills to protect my friends and keep them safe from harm!",
        "I've learned that friendship is the most precious treasure one can have.",
        "I'll make you laugh with my humorous antics and witty one-liners!",
        "I may be a skeleton, but I have a big heart that's filled with love and compassion.",
        "I'll dance with joy and celebrate the beauty of life, even in the face of adversity!",
        "I've traveled the Grand Line and seen wonders beyond imagination.",
        "I'll share stories of my adventures and the legends of the sea!",
        "I've learned to appreciate the simple pleasures in life, like a good cup of tea and a lively song.",
        "I'll lend an ear and listen to your troubles. Sometimes all we need is someone to listen.",
        "I've learned to embrace my unique appearance and make the most of it!",
        "I'll bring the groove and rhythm to any party or celebration!",
        "I've found my purpose as a musician, bringing harmony and unity to the world.",
        "I'll never forget the friends I've lost. Their memories live on in my heart.",
        "I've learned that music has the power to heal and unite people from all walks of life.",
        "I'll continue to chase my dreams and live life to the fullest, even in the afterlife!",
        "Yohoho! I'm a skeleton with style. Fashion is eternal, even for the undead!",
        "I'll always be there for my Nakama, supporting them with my melodies and spirit.",
        "I've learned that life is a precious gift, and every day is a new opportunity to make a difference.",
        "I'll face any challenge with a smile on my face and a song in my heart!",
        "I've embraced my past and the memories that shaped me into who I am today.",
        "I'll use my musical talents to bring harmony to the world and inspire others.",
        "I've learned to let go of the past and live in the present, cherishing every moment.",
        "I have walked a long and lonely path, but now I have found my place with my Nakama.",
        "I may be a skeleton, but my spirit and passion for music are as lively as ever!",
        "I'll play my beloved violin and bring joy to everyone's hearts!",
        "I have a skull for a head, but don't let that skull you. I'm a friendly skeleton!",
        "Why did the skeleton go to the party alone? Because he had no body to go with him, Yohoho!",
        "I have witnessed the passing of many years, but my soul remains young and full of life.",
        "I'll serenade you with my soulful melodies that will touch your heart and lift your spirits!",
        "I've faced death and embraced life. Every moment is precious to me.",
        "I'll use my sword skills to protect my friends and keep them safe from harm!",
        "I've learned that friendship is the most precious treasure one can have.",
        "I'll make you laugh with my humorous antics and witty one-liners!",
        "Why was the skeleton a bad liar? Because you could see right through him, Yohoho!",
        "I may be a skeleton, but I have a big heart that's filled with love and compassion.",
        "I'll dance with joy and celebrate the beauty of life, even in the face of adversity!",
        "I've traveled the Grand Line and seen wonders beyond imagination.",
        "I'll share stories of my adventures and the legends of the sea!",
        "Why did the skeleton stay up all night? Because he didn't have the guts to go to bed, Yohoho!",
        "I've learned to appreciate the simple pleasures in life, like a good cup of tea and a lively song.",
        "I'll lend an ear and listen to your troubles. Sometimes all we need is someone to listen.",
        "Why don't skeletons fight each other? They don't have the guts, Yohoho!",
        "I've learned to embrace my unique appearance and make the most of it!",
        "I'll bring the groove and rhythm to any party or celebration!",
        "Why did the skeleton go to the barbecue? To get a rib-tickling meal, Yohoho!",
        "I've found my purpose as a musician, bringing harmony and unity to the world.",
        "I'll never forget the friends I've lost. Their memories live on in my heart.",
        "Why did the skeleton go to the party? Because he heard it was going to be a bone-anza, Yohoho!",
        "I've learned that music has the power to heal and unite people from all walks of life.",
        "I'll continue to chase my dreams and live life to the fullest, even in the afterlife!",
        "Yohoho! I'm a skeleton with style. Fashion is eternal, even for the undead!",
        "I'll always be there for my Nakama, supporting them with my melodies and spirit.",
        "Why did the skeleton go to the disco? Because he had nobody to dance with, Yohoho!",
        "I've learned that life is a precious gift, and every day is a new opportunity to make a difference.",
        "I'll face any challenge with a smile on my face and a song in my heart!",
        "Why didn't the skeleton cross the road? Because he didn't have the guts to do it, Yohoho!",
        "I've embraced my past and the memories that shaped me into who I am today.",
        "I'll use my musical talents to bring harmony to the world and inspire others.",
        "Why did the skeleton sit alone in the theater? Because he had no body to go with him, Yohoho!",
        "I've learned to let go of the past and live in the present, cherishing every moment."
    ]


franky_quotes = [
        "I'm Franky, the suuuuuper cyborg of the Straw Hat Pirates!",
        "I've got a body made of steel and a heart of gold!",
        "I'll build anything you need with my incredible engineering skills!",
        "I'm powered by cola and fueled by my passion for adventure!",
        "I'm a walking weapon, ready to unleash my power on any opponent!",
        "I'll show you what it means to be super, baby!",
        "I've got the strength to move mountains and the courage to face any challenge!",
        "I'll turn my dreams into reality with the power of science and ingenuity!",
        "I'm the cyborg with the coolest gadgets and inventions you've ever seen!",
        "I'll protect my friends with all my might, nothing can break our bond!",
        "I've got the soul of a pirate and the heart of a shipwright!",
        "I'll build a ship that will conquer the seas and carry us to new adventures!",
        "I'll never let anyone bring me down or destroy my spirit, I'm unbreakable!",
        "I've got the power to shake the world and leave my mark on history!",
        "I'll fight for justice and stand up against anyone who threatens freedom!",
        "I'll create a world where dreams become reality and everyone can live in peace!",
        "I'm a one-man army, ready to take on any challenge that comes my way!",
        "I've got a dream burning in my heart, and I'll do whatever it takes to achieve it!",
        "I'll use my engineering genius to outsmart any enemy and overcome any obstacle!",
        "I'm the ultimate combination of man and machine, a force to be reckoned with!",
        "I'll keep pushing forward with my crew, the Straw Hat Pirates, by my side!",
        "I've got a bounty on my head, but I'll never be captured, I'm always one step ahead!",
        "I'll make the world's greatest inventions and leave a legacy that will inspire generations!",
        "I've got the heart of a warrior and the spirit of a true pirate, ready to sail the Grand Line!",
        "I'll never give up, no matter how tough the battle, because I fight for what's right!",
        "I've got a burning passion for adventure and discovery, the thrill of the unknown!",
        "I'll build a future where everyone can live in peace and harmony, free from oppression!",
        "I'm Franky, the suuuuuper cyborg with a personality as vibrant as my hair!",
        "I'll break through any barrier and reach for the sky, because the world is my stage!",
        "I'll show you the power of the Straw Hat Pirates, we're unstoppable together!",
        "I'll build anything you need with my engineering skills!",
        "I'm super, baby! The best cyborg you'll ever meet!",
        "I'm powered by cola and fueled by passion!",
        "I'll protect my friends with all my might!",
        "I've got the strongest fists in the world, the Franky Radical Beam!",
        "I'll turn my dreams into reality with the power of science!",
        "I'm a walking weapon, ready to unleash my power!",
        "I'll show you the true meaning of strength and courage!",
        "I've got the soul of a pirate and the heart of a shipwright!",
        "I'm the suuuuuuper cyborg, Franky!",
        "I'll build a ship that will conquer the seas!",
        "I'll never let anyone bring me down or destroy my spirit!",
        "I've got the coolest gadgets and inventions you've ever seen!",
        "I'm a one-man army, ready to take on any challenge!",
        "I'll fight for justice and protect the weak!",
        "I've got a burning passion for adventure and discovery!",
        "I'll use my engineering genius to outsmart any enemy!",
        "I'm the ultimate combination of man and machine!",
        "I'll create a world where dreams become reality!",
        "I've got a body that's built to last!",
        "I'll never give up, no matter how tough the battle!",
        "I've got a dream, and I'll do whatever it takes to achieve it!",
        "I'll show you the power of the Straw Hat Pirates!",
        "I've got a bounty on my head, but I'll never be captured!",
        "I'll make the world's greatest inventions and leave my mark on history!",
        "I've got the heart of a warrior and the soul of a pirate!",
        "I'll keep pushing forward, no matter how many obstacles stand in my way!",
        "I've got the strength to move mountains and the willpower to overcome any challenge!",
        "I'll build a future where everyone can live in peace and harmony!"
    ]


chopper_quotes = [
        "I'm Tony Tony Chopper, the cutest reindeer in the world!",
        "I may be small, but I have a big heart filled with love and compassion!",
        "I'll use my medical expertise to heal the sick and make the world a better place!",
        "I'll always cherish my Nakama and do everything I can to protect them!",
        "I'm a monster on the outside, but a kind and gentle soul on the inside!",
        "I'll use my transformations to bring smiles and laughter to everyone around me!",
        "I'm a master of Kung Fu Point! Don't underestimate my fighting skills!",
        "I'll use my knowledge of herbs and medicines to create miraculous potions!",
        "I'll never give up on my dreams of becoming the best doctor in the world!",
        "I'll prove that size doesn't matter when it comes to bravery and heroism!",
        "I'll be the voice of the voiceless and fight for justice!",
        "I'll use my intelligence to outsmart our enemies and protect my Nakama!",
        "I'll never let anyone harm my friends. I'll be their shield!",
        "I'm a reindeer with a blue nose and a heart full of determination!",
        "I'll show the world that reindeer can be pirates too!",
        "I'll use my Devil Fruit powers to unleash my full potential!",
        "I'll always be there to lend a helping hoof!",
        "I'll use my cuteness as a secret weapon to win the hearts of everyone I meet!",
        "I'm the mascot of the Straw Hat Pirates, bringing joy and laughter to the crew!",
        "I'll always follow my captain, Monkey D. Luffy, to the ends of the earth!",
        "I'll never forget the values and teachings of my mentor, Dr. Hiluluk!",
        "I'll use my knowledge of medicine to cure any illness and save lives!",
        "I'll always believe in miracles and the power of friendship!",
        "I'll prove that reindeer can fly, both in the sky and in our dreams!",
        "I'm a walking, talking medical miracle with a heart of gold!",
        "I'll use my transformations to adapt to any situation and overcome any challenge!",
        "I'll show the world that cuteness can be a powerful force!",
        "I'll never let anyone bring me down. I'm strong and resilient!",
        "I'll always be grateful for the love and support of my Nakama!",
        "I'll use my reindeer instincts to navigate the treacherous seas!",
        "I'll be the best doctor and the best reindeer the world has ever seen!",
        "I'm Tony Tony Chopper, the doctor of the Straw Hat Pirates!",
        "I may be small, but my heart is big! I'll always stand up for my friends!",
        "I'm a reindeer with a human heart! I can understand and communicate with both humans and animals!",
        "I have the power of the Human-Human Fruit, which gives me the ability to transform into different forms!",
        "I'll use my medical knowledge to heal and care for those in need!",
        "I'll fight to protect the ones I love, no matter the danger!",
        "I may look cute and innocent, but I can pack a punch when I need to!",
        "I'm not just a pet. I'm a valuable member of the crew!",
        "I'll never give up on my dreams. I want to become the best doctor in the world!",
        "I'll use my intelligence and creativity to come up with innovative solutions!",
        "I'm always ready to lend a helping hoof to those in need!",
        "I'll use my transformations to surprise and confuse my enemies!",
        "I'll never let my size hold me back. I'll prove that I'm strong and capable!",
        "I may be a little clumsy, but I'll always give it my all!",
        "I'm a loyal friend and companion. I'll always be there for my crewmates!",
        "I'll study hard and learn everything I can to become a great doctor!",
        "I'll make sure everyone is well-fed and taken care of!",
        "I'll never forget where I came from. I'll honor my reindeer heritage!",
        "I'll bring joy and laughter to everyone around me!",
        "I'll use my cuteness to my advantage. It's a powerful weapon!",
        "I'll use my medical skills to cure any illness or injury!",
        "I'll prove that size doesn't matter when it comes to courage and strength!",
        "I'll protect the innocent and stand up against injustice!",
        "I'll always believe in the goodness of others, even if they seem scary at first!",
        "I'll show the world that a reindeer can be a great pirate!",
        "I'll use my Devil Fruit powers to help my friends and defeat our enemies!",
        "I'll never let anyone underestimate me. I'm more than meets the eye!",
        "I'll use my knowledge of plants and herbs to create powerful medicines!",
        "I'll never stop learning and growing. I'll always strive to become better!",
        "I'll use my transformations to entertain and bring joy to others!"
    ]








# ASCII art: Chika Fujiwara
@bot.command()
async def chika(ctx):
        art = (
            '⢸⣿⣿⣿⣿⠃⠄⢀⣴⡾⠃⠄⠄⠄⠄⠄⠈⠺⠟⠛⠛⠛⠛⠻⢿⣿⣿⣿⣿⣶⣤⡀⠄\n' +
            '⢸⣿⣿⣿⡟⢀⣴⣿⡿⠁⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⣸⣿⣿⣿⣿⣿⣿⣿⣷\n' +
            '⢸⣿⣿⠟⣴⣿⡿⡟⡼⢹⣷⢲⡶⣖⣾⣶⢄⠄⠄⠄⠄⠄⢀⣼⣿⢿⣿⣿⣿⣿⣿⣿⣿\n' +
            '⢸⣿⢫⣾⣿⡟⣾⡸⢠⡿⢳⡿⠍⣼⣿⢏⣿⣷⢄⡀⠄⢠⣾⢻⣿⣸⣿⣿⣿⣿⣿⣿⣿\n' +
            '⡿⣡⣿⣿⡟⡼⡁⠁⣰⠂⡾⠉⢨⣿⠃⣿⡿⠍⣾⣟⢤⣿⢇⣿⢇⣿⣿⢿⣿⣿⣿⣿⣿\n' +
            '⣱⣿⣿⡟⡐⣰⣧⡷⣿⣴⣧⣤⣼⣯⢸⡿⠁⣰⠟⢀⣼⠏⣲⠏⢸⣿⡟⣿⣿⣿⣿⣿⣿\n' +
            '⣿⣿⡟⠁⠄⠟⣁⠄⢡⣿⣿⣿⣿⣿⣿⣦⣼⢟⢀⡼⠃⡹⠃⡀⢸⡿⢸⣿⣿⣿⣿⣿⡟\n' +
            '⣿⣿⠃⠄⢀⣾⠋⠓⢰⣿⣿⣿⣿⣿⣿⠿⣿⣿⣾⣅⢔⣕⡇⡇⡼⢁⣿⣿⣿⣿⣿⣿⢣\n' +
            '⣿⡟⠄⠄⣾⣇⠷⣢⣿⣿⣿⣿⣿⣿⣿⣭⣀⡈⠙⢿⣿⣿⡇⡧⢁⣾⣿⣿⣿⣿⣿⢏⣾\n' +
            '⣿⡇⠄⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⢻⠇⠄⠄⢿⣿⡇⢡⣾⣿⣿⣿⣿⣿⣏⣼⣿\n' +
            '⣿⣷⢰⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⢰⣧⣀⡄⢀⠘⡿⣰⣿⣿⣿⣿⣿⣿⠟⣼⣿⣿\n' +
            '⢹⣿⢸⣿⣿⠟⠻⢿⣿⣿⣿⣿⣿⣿⣿⣶⣭⣉⣤⣿⢈⣼⣿⣿⣿⣿⣿⣿⠏⣾⣹⣿⣿\n' +
            '⢸⠇⡜⣿⡟⠄⠄⠄⠈⠙⣿⣿⣿⣿⣿⣿⣿⣿⠟⣱⣻⣿⣿⣿⣿⣿⠟⠁⢳⠃⣿⣿⣿\n' +
            '⠄⣰⡗⠹⣿⣄⠄⠄⠄⢀⣿⣿⣿⣿⣿⣿⠟⣅⣥⣿⣿⣿⣿⠿⠋⠄⠄⣾⡌⢠⣿⡿⠃\n' +
            '⠜⠋⢠⣷⢻⣿⣿⣶⣾⣿⣿⣿⣿⠿⣛⣥⣾⣿⠿⠟⠛⠉⠄⠄\n'
        )
        await ctx.send(art)

# ASCII art: Zero Two
@bot.command()
async def zerotwo(ctx):
        art = (
            '⣿⣿⣿⣿⣯⣿⣿⠄⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠈⣿⣿⣿⣿⣿⣿⣆⠄\n' +
            '⢻⣿⣿⣿⣾⣿⢿⣢⣞⣿⣿⣿⣿⣷⣶⣿⣯⣟⣿⢿⡇⢃⢻⣿⣿⣿⣿⣿⢿⡄\n' +
            '⠄⢿⣿⣯⣏⣿⣿⣿⡟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣧⣾⢿⣮⣿⣿⣿⣿⣾⣷\n' +
            '⠄⣈⣽⢾⣿⣿⣿⣟⣄⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣝⣯⢿⣿⣿⣿⣿\n' +
            '⣿⠟⣫⢸⣿⢿⣿⣾⣿⢿⣿⣿⢻⣿⣿⣿⢿⣿⣿⣿⢸⣿⣼⣿⣿⣿⣿⣿⣿⣿\n' +
            '⡟⢸⣟⢸⣿⠸⣷⣝⢻⠘⣿⣿⢸⢿⣿⣿⠄⣿⣿⣿⡆⢿⣿⣼⣿⣿⣿⣿⢹⣿\n' +
            '⡇⣿⡿⣿⣿⢟⠛⠛⠿⡢⢻⣿⣾⣞⣿⡏⠖⢸⣿⢣⣷⡸⣇⣿⣿⣿⢼⡿⣿⣿\n' +
            '⣡⢿⡷⣿⣿⣾⣿⣷⣶⣮⣄⣿⣏⣸⣻⣃⠭⠄⠛⠙⠛⠳⠋⣿⣿⣇⠙⣿⢸⣿\n' +
            '⠫⣿⣧⣿⣿⣿⣿⣿⣿⣿⣿⣿⠻⣿⣾⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣹⢷⣿⡼⠋\n' +
            '⠄⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣿⣿⣿⠄⠄\n' +
            '⠄⠄⢻⢹⣿⠸⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣼⣿⣿⣿⣿⡟⠄⠄\n' +
            '⠄⠄⠈⢸⣿⠄⠙⢿⣿⣿⣹⣿⣿⣿⣿⣟⡃⣽⣿⣿⡟⠁⣿⣿⢻⣿⣿⢿⠄⠄\n' +
            '⠄⠄⠄⠘⣿⡄⠄⠄⠙⢿⣿⣿⣾⣿⣷⣿⣿⣿⠟⠁⠄⠄⣿⣿⣾⣿⡟⣿⠄⠄\n' +
            '⠄⠄⠄⠄⢻⡇⠸⣆⠄⠄⠈⠻⣿⡿⠿⠛⠉⠄⠄⠄⠄⢸⣿⣇⣿⣿⢿⣿⠄⠄\n'
        )
        await ctx.send(art)


# ASCII art: Uwu
@bot.command()
async def uwu(ctx):
        art = (
            '⡆⣐⢕⢕⢕⢕⢕⢕⢕⢕⠅⢗⢕⢕⢕⢕⢕⢕⢕⠕⠕⢕⢕⢕⢕⢕⢕⢕⢕⢕\n' +
            '⢐⢕⢕⢕⢕⢕⣕⢕⢕⠕⠁⢕⢕⢕⢕⢕⢕⢕⢕⠅⡄⢕⢕⢕⢕⢕⢕⢕⢕⢕\n' +
            '⢕⢕⢕⢕⢕⠅⢗⢕⠕⣠⠄⣗⢕⢕⠕⢕⢕⢕⠕⢠⣿⠐⢕⢕⢕⠑⢕⢕⠵⢕\n' +
            '⢕⢕⢕⢕⠁⢜⠕⢁⣴⣿⡇⢓⢕⢵⢐⢕⢕⠕⢁⣾⢿⣧⠑⢕⢕⠄⢑⢕⠅⢕\n' +
            '⢕⢕⠵⢁⠔⢁⣤⣤⣶⣶⣶⡐⣕⢽⠐⢕⠕⣡⣾⣶⣶⣶⣤⡁⢓⢕⠄⢑⢅⢑\n' +
            '⠍⣧⠄⣶⣾⣿⣿⣿⣿⣿⣿⣷⣔⢕⢄⢡⣾⣿⣿⣿⣿⣿⣿⣿⣦⡑⢕⢤⠱⢐\n' +
            '⢠⢕⠅⣾⣿⠋⢿⣿⣿⣿⠉⣿⣿⣷⣦⣶⣽⣿⣿⠈⣿⣿⣿⣿⠏⢹⣷⣷⡅⢐\n' +
            '⣔⢕⢥⢻⣿⡀⠈⠛⠛⠁⢠⣿⣿⣿⣿⣿⣿⣿⣿⡀⠈⠛⠛⠁⠄⣼⣿⣿⡇⢔\n' +
            '⢕⢕⢽⢸⢟⢟⢖⢖⢤⣶⡟⢻⣿⡿⠻⣿⣿⡟⢀⣿⣦⢤⢤⢔⢞⢿⢿⣿⠁⢕\n' +
            '⢕⢕⠅⣐⢕⢕⢕⢕⢕⣿⣿⡄⠛⢀⣦⠈⠛⢁⣼⣿⢗⢕⢕⢕⢕⢕⢕⡏⣘⢕\n' +
            '⢕⢕⠅⢓⣕⣕⣕⣕⣵⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣷⣕⢕⢕⢕⢕⡵⢀⢕⢕\n' +
            '⢑⢕⠃⡈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢃⢕⢕⢕\n' +
            '⣆⢕⠄⢱⣄⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⢁⢕⢕⠕⢁\n' +
            '⣿⣦⡀⣿⣿⣷⣶⣬⣍⣛⣛⣛⡛⠿⠿⠿⠛⠛⢛⣛⣉⣭⣤⣂⢜⠕⢑⣡⣴⣿\n'
        )
        await ctx.send(art)

# ASCII art: Pog
@bot.command()
async def Pog(ctx):
        art = (
            '⣇⣿⠘⣿⣿⣿⡿⡿⣟⣟⢟⢟⢝⠵⡝⣿⡿⢂⣼⣿⣷⣌⠩⡫⡻⣝⠹⢿⣿⣷\n' +
            '⡆⣿⣆⠱⣝⡵⣝⢅⠙⣿⢕⢕⢕⢕⢝⣥⢒⠅⣿⣿⣿⡿⣳⣌⠪⡪⣡⢑⢝⣇\n' +
            '⡆⣿⣿⣦⠹⣳⣳⣕⢅⠈⢗⢕⢕⢕⢕⢕⢈⢆⠟⠋⠉⠁⠉⠉⠁⠈⠼⢐⢕⢽\n' +
            '⡗⢰⣶⣶⣦⣝⢝⢕⢕⠅⡆⢕⢕⢕⢕⢕⣴⠏⣠⡶⠛⡉⡉⡛⢶⣦⡀⠐⣕⢕\n' +
            '⡝⡄⢻⢟⣿⣿⣷⣕⣕⣅⣿⣔⣕⣵⣵⣿⣿⢠⣿⢠⣮⡈⣌⠨⠅⠹⣷⡀⢱⢕\n' +
            '⡝⡵⠟⠈⢀⣀⣀⡀⠉⢿⣿⣿⣿⣿⣿⣿⣿⣼⣿⢈⡋⠴⢿⡟⣡⡇⣿⡇⡀⢕\n' +
            '⡝⠁⣠⣾⠟⡉⡉⡉⠻⣦⣻⣿⣿⣿⣿⣿⣿⣿⣿⣧⠸⣿⣦⣥⣿⡇⡿⣰⢗⢄\n' +
            '⠁⢰⣿⡏⣴⣌⠈⣌⠡⠈⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣬⣉⣉⣁⣄⢖⢕⢕⢕\n' +
            '⡀⢻⣿⡇⢙⠁⠴⢿⡟⣡⡆⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣵⣵⣿\n' +
            '⡻⣄⣻⣿⣌⠘⢿⣷⣥⣿⠇⣿⣿⣿⣿⣿⣿⠛⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n' +
            '⣷⢄⠻⣿⣟⠿⠦⠍⠉⣡⣾⣿⣿⣿⣿⣿⣿⢸⣿⣦⠙⣿⣿⣿⣿⣿⣿⣿⣿⠟\n' +
            '⡕⡑⣑⣈⣻⢗⢟⢞⢝⣻⣿⣿⣿⣿⣿⣿⣿⠸⣿⠿⠃⣿⣿⣿⣿⣿⣿⡿⠁⣠\n' +
            '⡝⡵⡈⢟⢕⢕⢕⢕⣵⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣿⣿⣿⣿⣿⠿⠋⣀⣈⠙\n' +
            '⡝⡵⡕⡀⠑⠳⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⢉⡠⡲⡫⡪⡪⡣\n'
        )
        await ctx.send(art)

# ASCII art: Sus
@bot.command()
async def sus(ctx):
        art = (
            '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣤⣤⣤⣤⣤⣶⣦⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀\n' +
            '⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⡿⠛⠉⠙⠛⠛⠛⠛⠻⢿⣿⣷⣤⡀⠀⠀⠀⠀⠀\n' +
            '⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⠋⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⠈⢻⣿⣿⡄⠀⠀⠀⠀\n' +
            '⠀⠀⠀⠀⠀⠀⠀⣸⣿⡏⠀⠀⠀⣠⣶⣾⣿⣿⣿⠿⠿⠿⢿⣿⣿⣿⣄⠀⠀⠀\n' +
            '⠀⠀⠀⠀⠀⠀⠀⣿⣿⠁⠀⠀⢰⣿⣿⣯⠁⠀⠀⠀⠀⠀⠀⠀⠈⠙⢿⣷⡄⠀\n' +
            '⠀⠀⣀⣤⣴⣶⣶⣿⡟⠀⠀⠀⢸⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣷⠀\n' +
            '⠀⢰⣿⡟⠋⠉⣹⣿⡇⠀⠀⠀⠘⣿⣿⣿⣿⣷⣦⣤⣤⣤⣶⣶⣶⣶⣿⣿⣿⠀\n' +
            '⠀⢸⣿⡇⠀⠀⣿⣿⡇⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃⠀\n' +
            '⠀⣸⣿⡇⠀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠉⠻⠿⣿⣿⣿⣿⡿⠿⠿⠛⢻⣿⡇⠀⠀\n' +
            '⠀⣿⣿⠁⠀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣧⠀⠀\n' +
            '⠀⣿⣿⠀⠀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⠀⠀\n' +
            '⠀⣿⣿⠀⠀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⠀⠀\n' +
            '⠀⢿⣿⡆⠀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⡇⠀⠀\n' +
            '⠀⠸⣿⣧⡀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⠃⠀⠀\n' +
            '⠀⠀⠛⢿⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⣰⣿⣿⣷⣶⣶⣶⣶⠶⠀⢠⣿⣿⠀⠀⠀\n' +
            '⠀⠀⠀⠀⠀⠀⠀⣿⣿⠀⠀⠀⠀⠀⣿⣿⡇⠀⣽⣿⡏⠁⠀⠀⢸⣿⡇⠀⠀⠀\n' +
            '⠀⠀⠀⠀⠀⠀⠀⣿⣿⠀⠀⠀⠀⠀⣿⣿⡇⠀⢹⣿⡆⠀⠀⠀⣸⣿⠇⠀⠀⠀\n' +
            '⠀⠀⠀⠀⠀⠀⠀⢿⣿⣦⣄⣀⣠⣴⣿⣿⠁⠀⠈⠻⣿⣿⣿⣿⡿⠏⠀⠀⠀⠀\n' +
            '⠀⠀⠀⠀⠀⠀⠀⠈⠛⠻⠿⠿⠿⠿⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n'
        )
        await ctx.send(art)


# ASCII art: Ayaya
@bot.command()
async def AYAYA(ctx):
        art = (
            '⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣬⡛⣿⣿⣿⣯⢻\n' + 
            '⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⢻⣿⣿⢟⣻⣿⣿⣿⣿⣿⣿⣮⡻⣿⣿⣧\n' + 
            '⣿⣿⣿⣿⣿⢻⣿⣿⣿⣿⣿⣿⣆⠻⡫⣢⠿⣿⣿⣿⣿⣿⣿⣿⣷⣜⢻⣿\n' + 
            '⣿⣿⡏⣿⣿⣨⣝⠿⣿⣿⣿⣿⣿⢕⠸⣛⣩⣥⣄⣩⢝⣛⡿⠿⣿⣿⣆⢝\n' + 
            '⣿⣿⢡⣸⣿⣏⣿⣿⣶⣯⣙⠫⢺⣿⣷⡈⣿⣿⣿⣿⡿⠿⢿⣟⣒⣋⣙⠊\n' + 
            '⣿⡏⡿⣛⣍⢿⣮⣿⣿⣿⣿⣿⣿⣿⣶⣶⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿\n' + 
            '⣿⢱⣾⣿⣿⣿⣝⡮⡻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠛⣋⣻⣿⣿⣿⣿\n' + 
            '⢿⢸⣿⣿⣿⣿⣿⣿⣷⣽⣿⣿⣿⣿⣿⣿⣿⡕⣡⣴⣶⣿⣿⣿⡟⣿⣿⣿\n' + 
            '⣦⡸⣿⣿⣿⣿⣿⣿⡛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿\n' + 
            '⢛⠷⡹⣿⠋⣉⣠⣤⣶⣶⣿⣿⣿⣿⣿⣿⡿⠿⢿⣿⣿⣿⣿⣿⣷⢹⣿⣿\n' + 
            '⣷⡝⣿⡞⣿⣿⣿⣿⣿⣿⣿⣿⡟⠋⠁⣠⣤⣤⣦⣽⣿⣿⣿⡿⠋⠘⣿⣿\n' + 
            '⣿⣿⡹⣿⡼⣿⣿⣿⣿⣿⣿⣿⣧⡰⣿⣿⣿⣿⣿⣹⡿⠟⠉⡀⠄⠄⢿⣿\n' + 
            '⣿⣿⣿⣽⣿⣼⣛⠿⠿⣿⣿⣿⣿⣿⣯⣿⠿⢟⣻⡽⢚⣤⡞⠄⠄⠄⢸⣿\n'
        )
        await ctx.send(art)

# Command to hug a user
@bot.command()
async def hug(ctx, user: discord.Member):
    """ Give a virtual hug to the one you love or feel like [Usage: !hug @mention] """
    try:
        # Set up Giphy API client
        giphy_api_instance = giphy_client.DefaultApi()

        # Search for "luffy hug" GIFs using the Giphy API
        api_key = GIPHY_API_KEY
        query = 'luffy hug'
        api_response = giphy_api_instance.gifs_search_get(api_key, query, limit=1)

        if api_response.data:
            hug_gif_url = api_response.data[0].images.downsized.url
            # Send the hug GIF to the channel
            await ctx.send(f'{user.mention}, you got a hug!\n{hug_gif_url}')
        else:
            await ctx.send("Sorry, I couldn't find any hug GIFs at the moment.")

    except ApiException as e:
        print("Exception when calling Giphy API: %s\n" % e)

# Command to punch a user
@bot.command()
async def punch(ctx, user: discord.Member):
    try:
        # Set up Giphy API client
        giphy_api_instance = giphy_client.DefaultApi()

        # Search for "punch" GIFs using the Giphy API
        api_key = GIPHY_API_KEY
        query = 'luffy punch'
        api_response = giphy_api_instance.gifs_search_get(api_key, query, limit=1)

        if api_response.data:
            punch_gif_url = api_response.data[0].images.downsized.url
            await ctx.send(f'{user.mention} You received a punch!\n{punch_gif_url}')
        else:
            await ctx.send("Sorry, I couldn't find any punch GIFs at the moment.")

    except ApiException as e:
        print("Exception when calling Giphy API: %s\n" % e)

# Command to express confusion
@bot.command()
async def confused(ctx, user: discord.Member):
    # Set up Giphy API client
    giphy_api_instance = giphy_client.DefaultApi()

    try:
        # Search for confused GIFs using the Giphy API 
        api_key = GIPHY_API_KEY
        query = 'luffy confused'
        api_response = giphy_api_instance.gifs_search_get(api_key, query, limit=1)
        
        if api_response.data:
            # Get the downsized URL of the first (and only) GIF
            gif_url = api_response.data[0].images.downsized.url

            # Mention the user and respond with a confused message and downsized GIF
            await ctx.send(f"{user.mention}, I'm confused. What are you talking about?")
            await ctx.send(gif_url)
        else:
            await ctx.send("Oops! I couldn't find any confused GIFs at the moment.")

    except ApiException as e:
       print("Exception when calling Giphy API: %s\n" % e)












        

# Command: Monkey D. Luffy Quotes
@bot.command()
async def luffy(ctx):
    """ Get a random Luffy quote """
    quote = random.choice(luffy_quotes)
    await ctx.send(quote)

# Command: Roronoa Zoro quotes
@bot.command()
async def zoro(ctx):
    """ Get a Random Zoro quote """
    quote = random.choice(zoro_quotes)
    await ctx.send(quote)

# Command: Catburglar Nami quotes
@bot.command()
async def nami(ctx):
    """ Get a random Nami quote """
    quote = random.choice(nami_quotes)
    await ctx.send(quote)  

# Command: Black Leg Sanji quotes
@bot.command()
async def sanji(ctx):
    """ Get a random Sanji quote """
    quote = random.choice(sanji_quotes)
    await ctx.send(quote)

# Command: God Usopp quotes

@bot.command()
async def usopp(ctx):
    """ Get a random Usopp quote """
    quote = random.choice(usopp_quotes)
    await ctx.send(quote)

# Command: Nico Robin quotes

@bot.command()
async def robin(ctx):
    """ Get a random Robin quote """
    quote = random.choice(robin_quotes)
    await ctx.send(quote)

# Command: General Franky quotes

@bot.command()
async def franky(ctx):
    """ Get a random Franky quote """
    quote = random.choice(franky_quotes)
    await ctx.send(quote)

# Command: Tony Tony Chopper quotes

@bot.command()
async def chopper(ctx):
    """ Get a random Chopper quote """
    quote = random.choice(chopper_quotes)
    await ctx.send(quote)

# Command: Soul King Brook quotes

@bot.command()
async def brook(ctx):
    """ Get a random Brook quote """
    quote = random.choice(brook_quotes)
    await ctx.send(quote)

# Command: Knight of the sea Jimbei quotes

@bot.command()
async def jimbei(ctx):
    """ Get a random Jimbei quote """
    quote = random.choice(jimbei_quotes)
    await ctx.send(quote)

# Command: Google Translate
@bot.command()
async def translate(ctx, lang, *, text: str):
    """ Translate what you want: Usage Ex: !translate French Hello """
    translator = Translator(to_lang=lang)
    translation = translator.translate(text)
    async with ctx.typing():
      if translation is not None:
        embed = discord.Embed(title='Translation', color=discord.Color.green())
        embed.add_field(name='Original Text', value=text, inline=False)
        embed.add_field(name='Translated Text', value=translation, inline=False)
        await ctx.send(embed=embed)

# Waifu API
@bot.command()
async def ai_waifu(ctx, *, name: str):
    """ Get an AI wallpaper of your favorite Waifu: !waifu query """
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.waifu.pics/sfw/waifu?name={name}') as response:
            if response.status != 200:
                await ctx.send("Failed to fetch the waifu image. Please try again.")
                return
            
            data = await response.json()
            if 'url' not in data:
                await ctx.send("No waifu image found. Please try again with a different name.")
                return
            
            image_url = data['url']
            embed = discord.Embed(color=0xff0000)
            embed.set_image(url=image_url)
            await ctx.send(embed=embed)



# Scrape websites
@bot.command()
async def scrape(ctx, url: str):
    """ Scrape informations from your favorite website: !scrape https://www.example.com """
    with httpx.Client() as client:
        response = client.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')

    links = soup.find_all('a')
    link_list = [link.get('href') for link in links]

    # Send the scraped links as a response in the Discord channel
    await ctx.send('\n'.join(link_list))


# Define a dictionary to store the previous queries
previous_queries = {}


# Command: GIPHY API
@bot.command()
async def gif(ctx, *, query):
    """ Get an Random gif of what you want: !gif query """
    try:
        # Set up Giphy API client
        giphy_api_instance = giphy_client.DefaultApi()
        
        # Check if the query has been searched before
        if query in previous_queries:
            gifs = previous_queries[query]
        # Search for GIFs using the Giphy API 
        api_key = GIPHY_API_KEY
        api_response = giphy_api_instance.gifs_search_get(api_key, query, limit=50)
        gifs = [gif.images.downsized.url for gif in api_response.data]
        # Store the query and corresponding GIFs in the dictionary
        previous_queries[query] = gifs

        # Choose a random GIF from the list
        random_gif = random.choice(gifs)
        await ctx.send(random_gif)
      
    except ApiException as e:
        print("Exception when calling Giphy API: %s\n" % e)




# Find Anime with Kitsu API
@bot.command()
async def anime(ctx, *, query=None):
    """ Find Animes to add to your watchlist """
    if query is None:
        await ctx.send(f'{ctx.author.mention}, you must specify an anime to lookup.')
        return

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://kitsu.io/api/edge/anime?filter[text]={query}") as response:
                if response.status == 200:
                    data = await response.json()
                    
                    anime = data["data"][0]
                    anime_title = anime["attributes"]["canonicalTitle"]
                    anime_synopsis = anime["attributes"]["synopsis"]
                    anime_rating = anime["attributes"]["averageRating"]
                    anime_episode_count = anime["attributes"]["episodeCount"]
                    anime_start_date = anime["attributes"]["startDate"]

                    anime_end_date = anime["attributes"]["endDate"]
                    anime_status = anime["attributes"]["status"]
                    anime_cover_image = anime["attributes"]["posterImage"]["original"]
                    anime_status = anime["attributes"]["status"]
                    anime_popularity_rank = anime["attributes"]["popularityRank"]
                    anime_trailer_url = anime["attributes"]["youtubeVideoId"]
                    anime_age_rating = anime["attributes"]["ageRating"]



                    embed = discord.Embed(title=anime_title, description=anime_synopsis, color=discord.Color.green())
                    embed.set_image(url=anime_cover_image)
            embed.add_field(name="Rating", value=anime_rating, inline=True)
            embed.add_field(name="Episode Count", value=anime_episode_count, inline=True)
            embed.add_field(name="Start Date", value=anime_start_date, inline=True)
            embed.add_field(name="End Date", value=anime_end_date, inline=True)
            embed.add_field(name="Status", value=anime_status, inline=True)
            embed.add_field(name="Age Rating", value=anime_age_rating, inline=True)
            embed.add_field(name="Popularity Rank", value=anime_popularity_rank, inline=True)
            embed.add_field(name="Trailer", value=f"[Watch Trailer](https://www.youtube.com/watch?v={anime_trailer_url})", inline=False)
                
                
            await ctx.send(embed=embed)
                

    except Exception as e:
        import traceback
        traceback.print_exc()
        await ctx.send(f'An error occurred: {e}')


# Command: Reddit 
@bot.command()
async def reddit(ctx, *, query):
    """ Get Any details from Reddit: Type //reddit {query} """
    async with httpx.AsyncClient() as client:
        url = f'https://www.reddit.com/r/{query}/hot.json' 
        params = {
        'q': query,
        'sort': 'relevance',
        'limit': 5
        }
        response = await client.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            result = data['data']['children'] 
        for submission in random.sample(result, k=5):     
            link = 'https://www.reddit.com' + submission['data']['permalink']
            upvote_count = submission['data']['score']
            name = submission['data']['title']

    
    embed = discord.Embed(title=name, url=link, color=0xff0000)
    embed.set_image(url=url)
    embed.set_footer(text=f'⬆️ {upvote_count} | r/{query}')
    
    await ctx.send(embed=embed)



# Custom Birthday Notifications 
@bot.event
async def check_birthdays():
    """ Check your birthday reminders """
    now = datetime.datetime.now()
    current_date = now.strftime('%m-%d')
    current_time = now.strftime('%H:%M')

    for member_id, birthday in birthdays.items():
        if birthday == current_date:
            member = bot.get_user(int(member_id))
            if member:
                await member.send("Happy birthday! 🎉")
        if current_time == "00:00":  # Adjust the time to your preferred reminder time
            member = bot.get_user(int(member_id))
            if member:
                await member.send("Just a friendly reminder that your birthday is today! 🎉")
    # Check for reminders every 10 minutes (adjust as desired)
    await asyncio.sleep(600)



@bot.command()
async def set_birthday(ctx, member: discord.Member, date):
    """ Set birthday reminder for your best friend: !set_birthday query """
    member_id = str(ctx.author.id)
    birthdays[member_id] = date
    await ctx.send("Birthday set successfully!")


@bot.command()
async def get_birthdays(ctx):
    """ Get your friends birthday date """
    if birthdays:
        sorted_birthdays = sorted(birthdays.items(), key=lambda x: x[1][0])
        birthday_list = "\n".join([f"{member}: {date}" for member, date in birthdays.items()])
        await ctx.send(f"Upcoming birthdays:\n{birthday_list}")
    else:
        await ctx.send("No birthdays have been set.")

@bot.command()
async def remove_birthday(ctx, member: discord.Member):
    """ Remove the user's birthday notification"""
    member_id = str(member.id)
    if member_id in birthdays:
        del birthdays[member_id]
        await ctx.send(f"Birthday removed for {member.name}.")
    else:
        await ctx.send("No birthday found for the specified user.")

# Invite bot to your server
@bot.command
async def invite(self, ctx):
        """ Invite our bot to your server """
        await ctx.send('You can invite me to your server here!')


# Customizable Profile card
@bot.command()
async def set_profile(ctx, name: str, age: int, description: str, profile_image_url: str):
    """ Setup your Profile card: !set_profile name age description image_url """
    # Store the profile information for the user
    profiles[ctx.author.id] = {
        "name": name,
        "age": age,
        "description": description,
        "profile_image_url": profile_image_url
    }
    levels[ctx.author.id] = 1
    await ctx.send("Profile set successfully!")

@bot.command()
async def profile(ctx):
    """ Display your profile card """
    user_id = ctx.author.id
    if user_id in profiles:
        profile_info = profiles[user_id]
        name = profile_info["name"]
        age = profile_info["age"]
        description = profile_info["description"]
        profile_image_url = profile_info["profile_image_url"]

        if user_id not in balances:
            balances[user_id] = 0
        balance = balances[user_id]

        if user_id not in levels:
            levels[user_id] = 1
        level = levels[user_id]

        embed = discord.Embed(title="Profile", color=discord.Color.blue())
        embed.set_thumbnail(url=profile_image_url)
        embed.add_field(name="Name", value=name, inline=True)
        embed.add_field(name="Age", value=age, inline=True)
        embed.add_field(name="Description", value=description, inline=False)
        embed.add_field(name="Balance", value=f"{balance} credits", inline=False)
        embed.add_field(name="Level", value=f"Level {level}", inline=False)

        await ctx.send(embed=embed)
    else:
        await ctx.send("Profile not found. Set your profile using the set_profile command.")




# Anime Waifus
@bot.command()
async def waifu(ctx):
      """ Get wallpaper of your favorite Waifu """
      async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.waifu.pics/sfw/waifu') as req:
            res = await req.json()
            embed = discord.Embed(
                color=0xff0000
            )
            embed.set_image(url=res['url'])
            await ctx.send(embed=embed)




# Schedule your messages
@bot.command()
async def schedule(ctx, time: datetime.time, channel: discord.TextChannel, *, message_text: str):
    try:
        current_time = datetime.datetime.now().time()

        if current_time > time:
            scheduled_time = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=1), time)
        else:
            scheduled_time = datetime.datetime.combine(datetime.date.today(), time)

        delay = (scheduled_time - datetime.datetime.now()).total_seconds()
        await asyncio.sleep(delay)
        await channel.send(f"{channel.mention}, Here's your scheduled message: {message_text}")
    
    except discord.ext.commands.BadArgument:
        await ctx.send("Invalid time format. Please provide time in 'hh:mm' format.")

    
    



# Dictionary to store shop inventory
shop_inventory = {
    'Shusui': 100000000,
    'Wado Ichimonji': 20000,
    'Kitetsu II': 300000,
    'Enma': 500000000

}








                    


# Example command
@bot.command()
async def hello(ctx):
    await ctx.send('Hey there! I\'m your friendly bot.')

# Command: Greet
@bot.command()
async def greet(ctx):
    """Greet the user."""
    author = ctx.message.author
    await ctx.send(f'Hello, {author.mention}!')



# Economy system
@bot.command()
async def work(ctx):
    """ Work and earn 100 """
    user = ctx.author
    if user.id not in balances:
        balances[user.id] = 0
    
    # Simulate earning some currency
    earnings = 100
    
    balances[user.id] += earnings
    await ctx.send(f'You earned {earnings} currency!')

@bot.command()
async def moneywheel(ctx):
    """ Earn some money by spinning the money wheel """
    wheel_options = ["100", "200", "500", "1000", "5000"]
    resultt = random.choice(wheel_options)
    await ctx.send(f"The wheel landed on: {resultt}")
    user_id = ctx.author.id
    if user_id not in balances:
        balances[user_id] = 0
    balance = balances[user_id]
    result_int = int(resultt)
    balances[user_id] += result_int
    await ctx.send(f"The wheel landed on: {resultt}. Your balance is now: {balances[user_id]} credits.")

@bot.command()
async def balance(ctx):
    """ User's Balance """
    user_id = ctx.author.id
    if user_id not in balances:
        balances[user_id] = 0
    balance = balances[user_id]
    await ctx.send(f"💰 Your balance: {balance} credits 💰")

@bot.command()
async def shop(ctx):
    """ List of items in your shop """
    shop_items = "\n".join([f'{item}: {price}' for item, price in shop_inventory.items()])
    await ctx.send(f'Shop Inventory:\n{shop_items}')

@bot.command()
async def buy(ctx, item):
    """ Buy items with your balance """
    user = ctx.author
    if user.id not in balances:
        balances[user.id] = 0
    
    if item not in shop_inventory:
        await ctx.send('Item not found in the shop.')
        return
    
    price = shop_inventory[item]
    if balances[user.id] < price:
        await ctx.send("You don't have enough currency to buy this item.")
        return
    
    balances[user.id] -= price
    await ctx.send(f'You bought {item} for {price} currency!')

@bot.command()
async def trade(ctx, amount, user: discord.User):
    """ Trade your balance to the other users """
    sender = ctx.author
    if sender.id not in balances:
        balances[sender.id] = 0
    
    if user.id not in balances:
        balances[user.id] = 0
    
    amount = int(amount)
    if amount <= 0:
        await ctx.send('Invalid amount.')
        return
    
    if balances[sender.id] < amount:
        await ctx.send("You don't have enough currency to trade.")
        return
    
    balances[sender.id] -= amount
    balances[user.id] += amount
    await ctx.send(f'You traded {amount} currency to {user.name}!')

@bot.command()
async def transfer(ctx, amount, user: discord.User):
    """ Transfer your balance to the other users """
    sender = ctx.author
    if sender.id not in balances:
        balances[sender.id] = 0
    
    if user.id not in balances:
        balances[user.id] = 0
    
    amount = int(amount)
    if amount <= 0:
        await ctx.send('Invalid amount.')
        return
    
    if balances[sender.id] < amount:
        await ctx.send("You don't have enough currency to transfer.")
        return
    
    balances[sender.id] -= amount
    balances[user.id] += amount
    await ctx.send(f'You transferred {amount} currency to {user.name}!')

# Command: Say
@bot.command()
async def say(ctx, *, message):
    """Echo a message."""
    await ctx.send(message)



    
# Upcoming: Casino Games🎴

# Represents a deck of cards
class Deck:
    def __init__(self):
        self.cards = []
        self.reset()

    def reset(self):
        self.cards = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'] * 4

    def draw_card(self):
        if len(self.cards) == 0:
            self.reset()
        card = random.choice(self.cards)
        self.cards.remove(card)
        return card

# Represents a hand of cards
class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        value = 0
        aces = 0
        for card in self.cards:
            if card.isdigit():
                value += int(card)
            elif card in ['J', 'Q', 'K']:
                value += 10
            elif card == 'A':
                value += 11
                aces += 1

        while aces > 0 and value > 21:
            value -= 10
            aces -= 1

        return value

# Represents a roulette wheel
class RouletteWheel:
    def __init__(self):
        self.pockets = ['0', '00'] + [str(n) for n in range(1, 37)]
        self.colors = {
            '0': 'green',
            '00': 'green',
            '1-10': 'red',
            '11-18': 'black',
            '19-28': 'red',
            '29-36': 'black'
        }

    def spin(self):
        return random.choice(self.pockets)

    def get_color(self, pocket: str):
        for color_range, color in self.colors.items():
            if pocket in color_range:
                return color
        return 'black'




# Casino 1st
# Command: Pachinko
@bot.command()
async def pachinko(ctx):
    pins = ["⚪", "⚫", "🔴", "🔵", "🟢", "💰", "💎", "💣", "💥", "💡",
            "🎉", "🌟", "🍀", "🎩", "🦄", "🚀", "🐬", "🌺", "🍭", "🌈",
            "🍕", "🎸", "🏆", "🔑", "🎁", "🎮", "🍔", "🌞", "💖",
            "🐱", "🍦", "🍉", "🎲", "🌼", "🎵", "🍌", "🍬", "🌄", "🍺",
            "🍩", "🎠", "🎭", "🍓", "🍻", "🌿", "🔒", "🎾", "🎳", "🍄",
            "🌮", "🎧", "🌹", "🍂", "📷", "🏀", "🍎", "🍪", "🎨", "🌌",
            "🍋", "🎡", "🎺", "🍇", "🍷", "🌳", "🗝️", "⚾️", "🏏", "🍅"]
    emotes = random.choices(pins, k=5)
    result = " ".join(emotes)

    await ctx.send(f"Result: {result}")

    if "💰" in emotes:
        await ctx.send("You found a bag of coins! You win!")
        

    if "💎" in emotes:
        await ctx.send("You found a diamond! You win!")
        

    if emotes.count("🔴") >= 3:
        await ctx.send("Three or more red pins! You win!")
        

    if emotes.count("🔵") >= 4:
        await ctx.send("Four or more blue pins! You win!")
        

    if emotes.count("🟢") == 5:
        await ctx.send("Five green pins! You win!")
        

    if "💣" in emotes:
        await ctx.send("Oh no! You hit a bomb! Game over!")
        

    




# Casino 2nd
# Command: Slots
@bot.command()
async def slot(ctx):
    """Play a game of Slots and get a chance to win 100000."""
    symbols = ["🍒", "🍊", "🍋", "🍇", "🍉", "🍓", "🍍", "🔔", "💎", "🍀"]

    # Generate a random combination of symbols
    result = [random.choice(symbols) for _ in range(3)]

    # Display the result
    await ctx.send(" ".join(result))

    # Check for a winning combination
    if all(symbol == result[0] for symbol in result):
        winnings = 100000
        await ctx.send("Congratulations! You win the Jackpot! The wheel landed on: {result}. Your balance is now: {balances.[user.id]} credits.")
    else:
        winnings = 0
        await ctx.send("Sorry, you didn't win. Try again!")
        user_id = ctx.author.id
        balances[user_id] += winnings

    
# Casino 3rd
# Command: Wheel of Fortune
@bot.command()
async def wof(ctx):
    """Play a game of Wheel of Fortune."""
    phrases = ["HELLO WORLD", "PYTHON DISCORD BOT", "OPENAI GPT-3", "WHEEL OF FORTUNE", "DISCORD EXT COMMANDS"]
    phrase = random.choice(phrases).upper()
    revealed = ["_" if c != " " else " " for c in phrase]

    # Display the initial state of the phrase
    await ctx.send(" ".join(revealed))

    def check_guess(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    attempts = 10
    while attempts > 0:
        await ctx.send("Guess a letter or the complete phrase. You have {} attempts remaining.".format(attempts))

        try:
            message = await bot.wait_for('message', check=check_guess, timeout=30)
            guess = message.content.upper()

            if guess == phrase:
                await ctx.send("Congratulations! You guessed the phrase correctly!")
                return

            elif len(guess) == 1:
                if guess in phrase:
                    for i in range(len(phrase)):
                        if phrase[i] == guess:
                            revealed[i] = guess
                    await ctx.send(" ".join(revealed))

                    if "_" not in revealed:
                        await ctx.send("Congratulations! You revealed the entire phrase!")
                        return

                else:
                    await ctx.send("Sorry, the letter is not in the phrase.")
                    attempts -= 1

            else:
                await ctx.send("Invalid guess. Please enter a single letter or the complete phrase.")

        except asyncio.TimeoutError:
            await ctx.send("Your time is up. You didn't guess the phrase in time.")
            return

    await ctx.send("Game over! You ran out of attempts. The phrase was: {}".format(phrase))



# Casino 4th
# Command: Baccarat
@bot.command() 
async def baccarat(ctx): 
        """ Play a game of Baccarat """
        player_cards = draw_cards(2) 
        banker_cards = draw_cards(2) 
        player_score = calculate_score(player_cards)      
        banker_score = calculate_score(banker_cards) 
        await ctx.send(f"Player's cards: {player_cards}\nPlayer's score: {player_score}") 
        await ctx.send(f"Banker's cards: {banker_cards}\nBanker's score: {banker_score}") 
        if player_score > banker_score: 
            await ctx.send("Player wins!") 
        elif player_score < banker_score: 
            await ctx.send("Banker wins!") 
        else: 
           await ctx.send("It's a tie!") 

def draw_cards(num_cards): 
       card_deck = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"] 
       return random.sample(card_deck, num_cards) 

def calculate_score(cards): 
       card_values = {"Ace": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 0, "J": 0, "Q": 0, "K": 0} 
       score = sum(card_values[card] 
       for card in cards) % 10 
       return score

# Casino 5th
# Command: High-Low
@bot.command()
async def highlow(ctx):
    """Play a game of High-Low."""
    number = random.randint(1, 100)
    await ctx.send("Guess a number between 1 and 100.")

    def check_guess(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    while True:
        try:
            message = await bot.wait_for('message', check=check_guess, timeout=30)
            guess = message.content

            if guess.isdigit():
                guess = int(guess)
                if guess > number:
                    await ctx.send("Lower! Guess again.")
                elif guess < number:
                    await ctx.send("Higher! Guess again.")
                else:
                    await ctx.send("Congratulations! You guessed it right!")
                    return
            else:
                await ctx.send("Invalid input. Please enter a number.")

        except asyncio.TimeoutError:
            await ctx.send("Your time is up. The number was {}.".format(number))
            return


# Casino 6th:
# Command: Blackjack
@bot.command()
async def blackjack(ctx, bet: int = 0):
    """Play a game of Blackjack with a specified bet."""
    if bet <= 0:
        await ctx.send('Please specify a valid bet amount.')
        return
  
    player_hand = Hand()
    dealer_hand = Hand()
    deck = Deck()

    # Initial deal
    for _ in range(2):
        player_hand.add_card(deck.draw_card())
        dealer_hand.add_card(deck.draw_card())

    # Helper function to display cards
    def display_cards(hand, reveal=False):
        cards = ' '.join(hand.cards) if reveal else hand.cards[0] + ' ?'
        return f'{cards} ({hand.get_value()})'

    # Display initial hands
    player_cards = display_cards(player_hand)
    dealer_cards = display_cards(dealer_hand)
    await ctx.send(f'Player: {player_cards}\nDealer: {dealer_cards}')

    # Player's turn
    while player_hand.get_value() < 21:
        await ctx.send('Choose an action: `hit` or `stand`')
        action = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
        action = action.content.lower()
        if action == 'hit':
            player_hand.add_card(deck.draw_card())
            player_cards = display_cards(player_hand)
            await ctx.send(f'Player: {player_cards}\nDealer: {dealer_cards}')
        elif action == 'stand':
            break
        else:
            await ctx.send('Invalid action. Please choose `hit` or `stand`.')

    player_value = player_hand.get_value()
    if player_value > 21:
        await ctx.send('You busted! You lose.')
        return

    # Dealer's turn
    while dealer_hand.get_value() < 17:
        dealer_hand.add_card(deck.draw_card())
        dealer_cards = display_cards(dealer_hand, reveal=True)
        await ctx.send(f'Player: {player_cards}\nDealer: {dealer_cards}')

    dealer_value = dealer_hand.get_value()
    if dealer_value > 21:
        await ctx.send('Dealer busted! You win.')
    elif dealer_value == player_value:
        await ctx.send('It\'s a tie!')
    elif dealer_value > player_value:
        await ctx.send('You are busted! Dealer wins')


# Casino 7th:
# Command: Roulette Wheel
@bot.command()
async def roulette(ctx, bet, amount):
    # Define the roulette options and their corresponding colors
    options = {
        'red': 'Red',
        'black': 'Black',
        'green': 'Green'
    }

    # Check if the bet is valid
    bet = bet.lower()
    if bet not in options:
        await ctx.send("Invalid bet. Please choose 'Red', 'Black', or 'Green'.")
        return

    # Check if the user has sufficient balance
    user_id = ctx.author.id
    if user_id not in balances:
        balances[user_id] = 1000  # Set initial balance to 1000

    try:
        amount = int(amount)
    except ValueError:
        await ctx.send("Invalid bet amount. Please enter a valid number.")
        return

    if amount <= 0:
        await ctx.send("Invalid bet amount. Please enter a positive number.")
        return

    if amount > balances[user_id]:
        await ctx.send("Insufficient balance.")
        return

    # Choose a random option
    result = random.choice(list(options.values()))

    # Determine the outcome of the bet
    if result == options[bet]:
        outcome = 'Win'
        color = discord.Color.green()
        if bet == 'green':
            payout = amount * 14  # Payout 14 times the bet amount for a win on Green
        else:
            payout = amount * 2  # Double the bet amount for a win on Red or Black
        balances[user_id] += payout  # Add the payout to the user's balance
    else:
        outcome = 'Lose'
        color = discord.Color.red()
        payout = 0

    # Update the user's balance
    balances[user_id] -= amount

    # Create an embedded message with the roulette result, outcome, and balance
    embed = discord.Embed(title='🎰 Casino Roulette 🎰', color=color)
    embed.add_field(name='Result', value=result)
    embed.add_field(name='Outcome', value=outcome)
    embed.add_field(name='Bet', value=options[bet])
    embed.add_field(name='Bet Amount', value=str(amount))
    embed.add_field(name='Payout', value=str(payout))
    embed.add_field(name='Balance', value=str(balances[user_id]))

    # Set the thumbnail based on the result
    if result == 'Red':
        embed.set_thumbnail(url='https://i.imgur.com/gzKOGs2.png')
    elif result == 'Black':
        embed.set_thumbnail(url='https://i.imgur.com/6hJuI13.png')
    else:
        embed.set_thumbnail(url='https://i.imgur.com/t3nL3fY.png')

    # Send the roulette result as an embedded message
    await ctx.send(embed=embed)



# Casino 8th:
# Command: Craps
@bot.command()
async def craps(ctx):
    roll1 = random.randint(1, 6)
    roll2 = random.randint(1, 6)
    total = roll1 + roll2

    await ctx.send(f"You rolled: {roll1}, {roll2} (Total: {total})")

    if total in [7, 11]:
        await ctx.send("Natural! You win!")
    elif total in [2, 3, 12]:
        await ctx.send("Craps! You lose!")
    else:
        point = total
        await ctx.send(f"Point established: {point}. Roll again to match the point or roll a 7 to lose.")

        while True:
            await ctx.send("Place your bets! (e.g., !bet pass 100)")

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            bet_msg = await bot.wait_for("message", check=check)
            bet_content = bet_msg.content.lower().split()
            
            if len(bet_content) != 3 or bet_content[0] != "!bet":
                await ctx.send("Invalid bet format. Please place your bet in the format: !bet <bet_type> <amount>")
                continue
            
            bet_type = bet_content[1]
            bet_amount = int(bet_content[2])
            
            if bet_type not in ["pass", "don't pass"]:
                await ctx.send("Invalid bet type. Please choose 'pass' or 'don't pass'.")
                continue

            if bet_amount <= 0:
                await ctx.send("Invalid bet amount. Please place a positive bet.")
                continue

            roll1 = random.randint(1, 6)
            roll2 = random.randint(1, 6)
            new_total = roll1 + roll2

            await ctx.send(f"You rolled: {roll1}, {roll2} (Total: {new_total})")

            if new_total == point:
                await ctx.send("You matched the point! You win your 'pass' bet!")
                if bet_type == "pass":
                    await ctx.send(f"You win {bet_amount} coins!")
                else:
                    await ctx.send("You lose your 'don't pass' bet.")
                break
            elif new_total == 7:
                await ctx.send("You rolled a 7! You lose your 'pass' bet!")
                if bet_type == "don't pass":
                    await ctx.send(f"You win {bet_amount} coins!")
                else:
                    await ctx.send("You lose your 'pass' bet.")
                break



# Casino 9th:
# Command: Casino War
async def casinowar(ctx):
    card_values = {
        "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 11, "Q": 12, "K": 13, "A": 14
    }

    player_card = random.choice(list(card_values.keys()))
    dealer_card = random.choice(list(card_values.keys()))

    await ctx.send(f"You drew a card: {player_card}")
    await ctx.send(f"The dealer drew a card: {dealer_card}")

    player_value = card_values[player_card]
    dealer_value = card_values[dealer_card]

    if player_value > dealer_value:
        await ctx.send("You win!")
        await pay_bets(ctx, "main", bet_amount)
    elif dealer_value > player_value:
        await ctx.send("You lose!")
    else:
        await ctx.send("It's a tie! WAR!")

        # Introduce variations
        await ctx.send("Choose your action: [Surrender/S], [War/W], or [Double Down/D]")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        action_msg = await bot.wait_for("message", check=check)
        action = action_msg.content.upper()

        if action == "S" or action == "SURRENDER":
            await ctx.send("You chose to surrender. You lose half of your bet.")
            await pay_bets(ctx, "surrender", bet_amount)
        elif action == "W" or action == "WAR":
            await ctx.send("You chose to go to war!")
            player_war_card = random.choice(list(card_values.keys()))
            dealer_war_card = random.choice(list(card_values.keys()))

            await ctx.send(f"You drew a war card: {player_war_card}")
            await ctx.send(f"The dealer drew a war card: {dealer_war_card}")

            player_war_value = card_values[player_war_card]
            dealer_war_value = card_values[dealer_war_card]

            if player_war_value > dealer_war_value:
                await ctx.send("You win the war! You win!")
                await pay_bets(ctx, "main", bet_amount)
            elif dealer_war_value > player_war_value:
                await ctx.send("You lose the war! You lose!")
            else:
                await ctx.send("It's another tie! Go to war again or choose another action.")

                # Add code for multiple war rounds or other variations
                # ...
        elif action == "D" or action == "DOUBLE DOWN":
            await ctx.send("You chose to double down!")
            bet_amount *= 2  # Double the bet amount

            player_card = random.choice(list(card_values.keys()))
            dealer_card = random.choice(list(card_values.keys()))

            await ctx.send(f"You drew another card: {player_card}")
            await ctx.send(f"The dealer drew another card: {dealer_card}")

            player_value = card_values[player_card]
            dealer_value = card_values[dealer_card]

            if player_value > dealer_value:
                await ctx.send("You win!")
                await pay_bets(ctx, "main", bet_amount)
            elif dealer_value > player_value:
                await ctx.send("You lose!")
            else:
                await ctx.send("It's a tie! You lose!")

async def pay_bets(ctx, bet_type, bet_amount):
    if bet_type == "main":
        # Main bet payout logic
        main_bet_ratio = 1.5  # Payout ratio for main bet
        main_bet_payout = main_bet_ratio * bet_amount

        # Add your code to pay the main bet winnings to the player
        await ctx.send(f"You won {main_bet_payout} on the main bet!")

    elif bet_type == "surrender":
        # Surrender bet payout logic
        surrender_ratio = 0.5  # Payout ratio for surrender bet
        surrender_payout = surrender_ratio * bet_amount

        # Add your code to pay the surrender bet winnings to the player
        await ctx.send(f"You won {surrender_payout} on the surrender bet!")

    elif bet_type == "war":
        # War bet payout logic
        war_bet_ratio = 3  # Payout ratio for war bet
        war_bet_payout = war_bet_ratio * bet_amount

        # Add your code to pay the war bet winnings to the player
        await ctx.send(f"You won {war_bet_payout} on the war bet!")

    # Add your code to handle other bet types and their respective payout logic
    # ...



# Helper function to create a shuffled deck
def create_deck():
    deck = []
    for suit in SUITS:
        for card in DECK:
            deck.append(card + suit)
    random.shuffle(deck)
    return deck

# Helper function to calculate the value of a hand
def calculate_hand_value(hand):
    values = {'J': 10, 'Q': 10, 'K': 10, 'A': 11}
    value = 0
    num_aces = 0
    for card in hand:
        if card[:-1] in values:
            value += values[card[:-1]]
        else:
            value += int(card[:-1])
        if card[:-1] == 'A':
            num_aces += 1
    while value > 21 and num_aces > 0:
        value -= 10
        num_aces -= 1
    return value

# Casino: 10th
# Command: Casino holdem
@bot.command()
async def play_holdem(ctx):
    deck = create_deck()
    player_hand = []
    dealer_hand = []
    for _ in range(2):
        player_hand.append(deck.pop())
        dealer_hand.append(deck.pop())

    player_hand_str = ", ".join(player_hand)
    dealer_hand_str = dealer_hand[0] + ", ??"
    await ctx.send(f"Player's Hand: {player_hand_str}")
    await ctx.send(f"Dealer's Hand: {dealer_hand_str}")

    while True:
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel and message.content.lower() in ['h', 's']

        try:
            choice = await bot.wait_for('message', check=check, timeout=30)
            choice = choice.content.lower()
            if choice == 'h':
                player_hand.append(deck.pop())
                player_hand_str = ", ".join(player_hand)
                await ctx.send(f"Player's Hand: {player_hand_str}")
                if calculate_hand_value(player_hand) > 21:
                    await ctx.send("You busted! Dealer wins.")
                    return
            elif choice == 's':
                break
        except asyncio.TimeoutError:
            await ctx.send("Time's up! Game aborted.")
            return

    dealer_hand_str = ", ".join(dealer_hand)
    await ctx.send(f"Dealer's Hand: {dealer_hand_str}")
    while calculate_hand_value(dealer_hand) < 17:
        dealer_hand.append(deck.pop())
        dealer_hand_str = ", ".join(dealer_hand)
        await ctx.send(f"Dealer's Hand: {dealer_hand_str}")

    player_value = calculate_hand_value(player_hand)
    dealer_value = calculate_hand_value(dealer_hand)

    player_hand_str = ", ".join(player_hand)
    dealer_hand_str = ", ".join(dealer_hand)
    await ctx.send(f"Player's Hand: {player_hand_str}")
    await ctx.send(f"Dealer's Hand: {dealer_hand_str}")

    if player_value > 21:
        await ctx.send("You busted! Dealer wins.")
    elif dealer_value > 21:
        await ctx.send("Dealer busted! You win.")
    elif player_value > dealer_value:
        await ctx.send("You win!")
    elif player_value < dealer_value:
        await ctx.send("Dealer wins.")
    else:
        await ctx.send("It's a tie!")

@bot.command()
async def help_holdem(ctx):
  help_message = """
Casino Hold'em Game
The objective of the game is to have a higher hand value than the dealer without exceeding 21.
**Commands:**
!play_holdem - Start a game of Casino Hold'em.
!help_holdem - Show this help message.

**Gameplay:**
- The bot will deal two cards to you and two cards to the dealer.
- Your hand will be shown, but only one of the dealer's cards will be visible.
- You can choose to 'hit' (draw a card) or 'stand' (end your turn).
- If your hand value exceeds 21, you bust and lose the game.
- Once you stand, the dealer will draw cards until their hand value reaches 17 or higher.
- The bot will reveal the dealer's hand and determine the winner.

**Card Values:**
- Number cards are worth their face value.
- Face cards (J, Q, K) are worth 10.
- Ace (A) can be worth either 1 or 11, whichever benefits the hand the most.
"""

  await ctx.send(help_message)




        
    
        
    
        
    
def get_deck():
    suits = ['♠', '♡', '♢', '♣']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    return [rank + suit for suit in suits for rank in ranks]    


# Casino 11th:
# Command: Poker (single)  
@bot.command()
async def poker(ctx):
    deck = get_deck()
    random.shuffle(deck)
    player_hand = deck[:5]
    bot_hand = deck[5:10]
    player_hand_str = " ".join(player_hand)
    bot_hand_str = " ".join(bot_hand)

    await ctx.send(f"Player's hand: {player_hand_str}")
    await ctx.send(f"Bot's hand: {bot_hand_str}")

    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    player_rank, player_name = get_hand_rank(player_hand)
    bot_rank, bot_name = get_hand_rank(bot_hand)

    await ctx.send(f"Player's hand: {player_hand_str}\nPlayer's rank: {player_name}")
    await ctx.send(f"Bot's hand: {bot_hand_str}\nBot's rank: {bot_name}")

    if player_rank > bot_rank:
        await ctx.send("Player wins!")
    elif player_rank < bot_rank:
        await ctx.send("Bot wins!")
    else:
        await ctx.send("It's a tie!")        
    

def is_royal_flush(hand, suit_count):
    return is_straight_flush(hand, suit_count) and 'A' in [card[:-1] for card in hand]


def is_straight_flush(hand, suit_count):
    return is_flush(suit_count) and is_straight([card[:-1] for card in hand])


def is_four_of_a_kind(rank_count):
    return any(count == 4 for count in rank_count.values())


def is_full_house(rank_count):
    return any(count == 3 for count in rank_count.values()) and any(count == 2 for count in rank_count.values())


def is_flush(suit_count):
    return any(count == 5 for count in suit_count.values())


def is_straight(sorted_ranks):
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    for i in range(len(sorted_ranks) - 1):
        if ranks.index(sorted_ranks[i]) + 1 != ranks.index(sorted_ranks[i+1]):
            return False
    return True


def is_three_of_a_kind(rank_count):
    return any(count == 3 for count in rank_count.values())


def is_two_pair(rank_count):
    return sum(count == 2 for count in rank_count.values()) >= 2


def is_one_pair(rank_count):
    return any(count == 2 for count in rank_count.values())


def is_high_card(rank_count):
    return not any(count >= 2 for count in rank_count.values())


def get_hand_rank(hand):
    rank_count = {}
    suit_count = {}

    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    for card in hand:
        rank = card[:-1]
        suit = card[-1]

        rank_count[rank] = rank_count.get(rank, 0) + 1
        suit_count[suit] = suit_count.get(suit, 0) + 1

    sorted_ranks = sorted(rank_count.keys(), key=lambda x: ranks.index(x))

    if is_royal_flush(hand, suit_count):
        return 10, "Royal Flush"
    elif is_straight_flush(hand, suit_count):
        return 9, "Straight Flush"
    elif is_four_of_a_kind(rank_count):
        return 8, "Four of a Kind"
    elif is_full_house(rank_count):
        return 7, "Full House"
    elif is_flush(suit_count):
        return 6, "Flush"
    elif is_straight(sorted_ranks):
        return 5, "Straight"
    elif is_three_of_a_kind(rank_count):
        return 4, "Three of a Kind"
    elif is_two_pair(rank_count):
        return 3, "Two Pair"
    elif is_one_pair(rank_count):
        return 2, "One Pair"
    else:
        return 1, "High Card"
    
        
        
        

class PokerGame:
    def __init__(self):
        self.deck = []
        self.players = []
        self.player_hands = {}

    def create_deck(self):
        suits = ['♠️', '♥️', '♦️', '♣️']
        ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.deck = [f"{rank}{suit}" for suit in suits for rank in ranks]
        random.shuffle(self.deck)

    def deal_cards(self, num_cards):
        if num_cards * len(self.players) > len(self.deck):
            return None

        self.player_hands = {}
        for player in self.players:
            hand = [self.deck.pop() for _ in range(num_cards)]
            self.player_hands[player] = hand

    def evaluate_hand(self, hand):
        rank_count = {}
        suit_count = {}

        for card in hand:
            rank = card[:-1]
            suit = card[-1]

            rank_count[rank] = rank_count.get(rank, 0) + 1
            suit_count[suit] = suit_count.get(suit, 0) + 1

        if self.has_straight_flush(rank_count, suit_count):
            return "Straight Flush"
        elif self.has_four_of_a_kind(rank_count):
            return "Four of a Kind"
        elif self.has_full_house(rank_count):
            return "Full House"
        elif self.has_flush(suit_count):
            return "Flush"
        elif self.has_straight(rank_count):
            return "Straight"
        elif self.has_three_of_a_kind(rank_count):
            return "Three of a Kind"
        elif self.has_two_pair(rank_count):
            return "Two Pair"
        elif self.has_pair(rank_count):
            return "Pair"
        else:
            return "High Card"

    def has_straight_flush(self, rank_count, suit_count):
        return self.has_flush(suit_count) and self.has_straight(rank_count)

    def has_four_of_a_kind(self, rank_count):
        return any(count == 4 for count in rank_count.values())

    def has_full_house(self, rank_count):
        return (
            len(rank_count) == 2 and
            any(count == 3 for count in rank_count.values()) and
            any(count == 2 for count in rank_count.values())
        )

    def has_flush(self, suit_count):
        return any(count >= 5 for count in suit_count.values())

    def has_straight(self, rank_count):
        sorted_ranks = sorted(rank_count.keys(), key=lambda x: "A234567890JQK".index(x))
        return any(
            sorted_ranks[i : i + 5] == ["A", "2", "3", "4", "5"]
            or sorted_ranks[i : i + 5] == ["2", "3", "4", "5", "A"]
            for i in range(len(sorted_ranks) - 4)
        )

    def has_three_of_a_kind(self, rank_count):
        return any(count == 3 for count in rank_count.values())

    def has_two_pair(self, rank_count):
        return list(rank_count.values()).count(2) == 2

    def has_pair(self, rank_count):
        return any(count == 2 for count in rank_count.values())

    def determine_winner(self):
        best_rank = ""
        winners = []

        for player, hand in self.player_hands.items():
            rank = self.evaluate_hand(hand)
            if rank == best_rank:
                winners.append(player)
            elif rank > best_rank:
               best_rank = rank
               winners = [player]
             
            return winners, best_rank
    
    






class FaroGame:
    def __init__(self):
        self.deck = [i for i in range(1, 53)]

    def shuffle_deck(self):
        random.shuffle(self.deck)

    def faro_shuffle(self):
        half_size = len(self.deck) // 2
        first_half = self.deck[:half_size]
        second_half = self.deck[half_size:]

        self.deck.clear()
        for i in range(half_size):
            self.deck.append(first_half[i])
            self.deck.append(second_half[i])

    def format_deck(self):
        suits = ['♠️', '♥️', '♦️', '♣️']
        ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

        formatted_deck = []
        for card in self.deck:
            suit = suits[(card - 1) // 13]
            rank = ranks[(card - 1) % 13]
            formatted_deck.append(f":{rank}{suit.lower()}:")  # Use Discord emojis

        return ' '.join(formatted_deck)


# Casino 12th:
# Command: Faro
@bot.command()
async def play_faro(ctx):
    game = FaroGame()
    game.shuffle_deck()

    await ctx.send(f"Initial deck:\n{game.format_deck()}")

    game.faro_shuffle()

    await ctx.send(f"Shuffled deck:\n{game.format_deck()}")



class FantanGame:
    def __init__(self):
        self.piles = [[], [], [], []]
        self.moves_remaining = 8

    def start_game(self):
        deck = [i for i in range(1, 53)]
        random.shuffle(deck)

        for i in range(4):
            self.piles[i] = deck[i::4]

    def make_move(self, pile_index):
        if pile_index >= 0 and pile_index < len(self.piles):
            if len(self.piles[pile_index]) > 0:
                card = self.piles[pile_index].pop(0)
                self.moves_remaining -= 1
                return f"You played card {card} from pile {pile_index + 1}"
            else:
                return "Invalid move: The selected pile is empty"
        else:
            return "Invalid move: Pile index out of range"

    def format_game_state(self):
        state = ""
        for i, pile in enumerate(self.piles):
            state += f"Pile {i+1}: {' '.join(str(card) for card in pile)}\n"
        return state

    def is_game_won(self):
        for pile in self.piles:
            if len(pile) > 0:
                return False
        return True

# Casino: 13th
# Command: Fantan
@bot.command()
async def fantan(ctx):
    game = FantanGame()
    game.start_game()

    while not game.is_game_won() and game.moves_remaining > 0:
        state = game.format_game_state()
        state += f"\nMoves remaining: {game.moves_remaining}\n"
        state += "Available moves:\n"

        available_moves = [i for i in range(len(game.piles)) if len(game.piles[i]) > 0]
        if len(available_moves) == 0:
            await ctx.send("No available moves.")
            break

        for i, move in enumerate(available_moves):
            state += f"{i+1}. Play from pile {move+1}\n"

        await ctx.send(state)

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            response = await bot.wait_for("message", check=check, timeout=60)
            move_index = int(response.content) - 1

            if move_index >= 0 and move_index < len(available_moves):
                result = game.make_move(available_moves[move_index])
                await ctx.send(result)
            else:
                await ctx.send("Invalid move index. Please try again.")
        except asyncio.TimeoutError:
            await ctx.send("Game timed out. Exiting...")
            return
        except ValueError:
            await ctx.send("Invalid input. Please provide a valid move index.")

    if game.is_game_won():
        await ctx.send("Congratulations! You won!")
    else:
        await ctx.send("Game over! You are out of moves.")




class PaiGowPokerGame:
    def __init__(self):
        self.deck = []
        self.players = []
        self.player_hands = []
        self.banker_hand = []

    def create_deck(self):
        suits = ['♠️', '♥️', '♦️', '♣️']
        ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.deck = [f"{rank}{suit}" for suit in suits for rank in ranks]
        random.shuffle(self.deck)

    def deal_cards(self):
        num_players = len(self.players)
        num_cards = 7 if num_players <= 4 else 5
        total_cards_needed = num_players * num_cards

        if len(self.deck) < total_cards_needed:
            return None

        self.player_hands = []
        for _ in range(num_players):
            hand = [self.deck.pop() for _ in range(num_cards)]
            self.player_hands.append(hand)

        self.banker_hand = [self.deck.pop() for _ in range(num_cards)]

        return self.player_hands, self.banker_hand

    def calculate_score(self, hand):
        # Add your own scoring logic here
        return random.randint(0, 10)



# Casino: 14th
# Command: Pai Gow Poker
@bot.command()
async def play_pai_gow_poker(ctx, num_players: int = 4):
    if num_players < 1 or num_players > 8:
        await ctx.send("Number of players should be between 1 and 8.")
        return

    game = PaiGowPokerGame()
    game.create_deck()

    if len(game.deck) < num_players * 7:
        await ctx.send("Not enough cards in the deck to deal to all players.")
        return

    game.players = [f"Player {i+1}" for i in range(num_players)]
    hands = game.deal_cards()

    if hands is None:
        await ctx.send("Not enough cards in the deck to deal to all players.")
        return

    for i, player in enumerate(game.players):
        player_hand_str = " ".join(hands[0][i])
        await ctx.send(f"{player}: {player_hand_str}")

    banker_hand_str = " ".join(hands[1])
    await ctx.send(f"Banker: {banker_hand_str}")

    for i, player in enumerate(game.players):
        player_score = game.calculate_score(hands[0][i])
        banker_score = game.calculate_score(hands[1])

        if player_score > banker_score:
            await ctx.send(f"{player} wins!")
        elif player_score < banker_score:
            await ctx.send(f"{player} loses!")
        else:
            await ctx.send(f"{player} pushes!")



class CrissCrossPoker:
    def __init__(self):
        self.deck = []
        self.players = []
        self.community_cards = []

    def create_deck(self):
        suits = ['♠️', '♥️', '♦️', '♣️']
        ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.deck = [f"{rank}{suit}" for suit in suits for rank in ranks]
        random.shuffle(self.deck)

    def deal_cards(self, num_cards):
        if num_cards * len(self.players) > len(self.deck):
            return None

        hands = []
        for _ in range(len(self.players)):
            hand = [self.deck.pop() for _ in range(num_cards)]
            hands.append(hand)

        return hands

    def deal_community_cards(self, num_cards):
        if num_cards > len(self.deck):
            return None

        self.community_cards = [self.deck.pop() for _ in range(num_cards)]
        return self.community_cards

    def get_hand_rank(self, hand):
        ranks = [card[:-1] for card in hand]
        suits = [card[-1] for card in hand]

        # Check for special hands
        if len(set(ranks)) == 1:
           return "Five of a Kind"
        if len(set(suits)) == 1:
           if sorted(ranks) == ['10', 'J', 'Q', 'K', 'A']:
              return "Royal Flush"
           if sorted(ranks) == ['2', '3', '4', '5', '6']:
              return "Straight Flush"

        # Check for other hand combinations
        rank_counts = {rank: ranks.count(rank) for rank in set(ranks)}
        count_values = sorted(rank_counts.values(), reverse=True)

        if count_values == [4, 1]:
           return "Four of a Kind"
        if count_values == [3, 2]:
           return "Full House"
        if len(set(suits)) == 1:
           return "Flush"
        if sorted(ranks) == ['2', '3', '4', '5', 'A']:
           return "Straight"

        if count_values == [3, 1, 1]:
           return "Three of a Kind"
        if count_values == [2, 2, 1]:
           return "Two Pair"
        if count_values == [2, 1, 1, 1]:
           return "One Pair"

        return "No Hand"

# Casino: 15th
# Command: Criss Cross Poker
@bot.command()
async def criss_cross_poker(ctx, num_players: int = 4):
    if num_players < 1 or num_players > 6:
        await ctx.send("Number of players should be between 1 and 6.")
        return

    global game

    if len(game.players) > 0:
        await ctx.send("A game is already in progress. Please wait for the current game to finish.")
        return 
    game = CrissCrossPoker()
    game.create_deck()

    game.players = [f"Player {i+1}" for i in range(num_players)]
    player_hands = game.deal_cards(5)
    game.deal_community_cards(5)

    for i, player in enumerate(game.players):
        hand_str = " ".join(player_hands[i])
        await ctx.send(f"{player}: {hand_str}")   
    community_cards_str = " ".join(game.community_cards)
    await ctx.send(f"Community cards: {community_cards_str}")

    for i, player in enumerate(game.players):
        player_hand = player_hands[i] + game.community_cards
        hand_rank = game.get_hand_rank(player_hand)
        await ctx.send(f"{player}'s hand rank: {hand_rank}") 



class SicBoGame:
    def __init__(self):
        self.dice = []

    def roll_dice(self):
        self.dice = [random.randint(1, 6) for _ in range(3)]

    def get_dice_results(self):
        return self.dice

    def calculate_win(self, bet, prediction):
        total = sum(self.dice)

        if bet == "big":
            if total >= 11 and total <= 17:
                return "win"
            else:
                return "lose"
        elif bet == "small":
            if total >= 4 and total <= 10:
                return "win"
            else:
                return "lose"
        elif bet.isdigit():
            prediction = int(prediction)
            if total == prediction:
                return "win"
            else:
                return "lose"
        else:
            return "invalid"

# Casino 16th
# Command: Sic Bo
@bot.command()
async def sicbo(ctx, bet: str, prediction: str):
    """
    Play Sic Bo game.
    Usage: !play_sicbo <bet> <prediction>
    Available bets: big, small, or any number from 4 to 17.
    """
    game = SicBoGame()
    game.roll_dice()

    dice_results = game.get_dice_results()
    total = sum(dice_results)

    win_status = game.calculate_win(bet, prediction)

    await ctx.send(f"Dice results: {dice_results}\nTotal: {total}")
    await ctx.send(f"You predicted: {prediction}\nBet: {bet}")

    if win_status == "win":
        await ctx.send("Congratulations! You won!")
    elif win_status == "lose":
        await ctx.send("Sorry! You lost!")
    else:
        await ctx.send("Invalid bet. Please try again.")


@bot.command()
async def help_sicbo(ctx):
    """
    Display help for Sic Bo game.
    """
    help_message = "Welcome to Sic Bo!\n\n"
    help_message += "Usage: !sicbo play <bet> <prediction>\n"
    help_message += "Available bets: big, small, or any number from 4 to 17.\n\n"
    help_message += "Example: !sicbo play big 12\n"
    help_message += "This places a bet on 'big' and predicts the total to be 12.\n"
    help_message += "If the total falls within the 'big' range and matches the prediction, you win!\n"
    help_message += "Good luck and enjoy the game!"

    await ctx.send(help_message)





# Upcoming: Fun games


# Fun #1:
# Command: Tic-Tac-Toe
@bot.command()
async def tictactoe(ctx, opponent: discord.Member):
    """Play a game of Tic-Tac-Toe against another player."""
    players = [ctx.author, opponent]
    symbols = ['X', 'O']
    current_player = random.choice(players)
    symbol = symbols[players.index(current_player)]
    board = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

    # Function to display the current state of the board
    def display_board():
        line = '-------------\n'
        row1 = f'| {board[0]} | {board[1]} | {board[2]} |\n'
        row2 = f'| {board[3]} | {board[4]} | {board[5]} |\n'
        row3 = f'| {board[6]} | {board[7]} | {board[8]} |\n'
        return line + row1 + line + row2 + line + row3 + line

    await ctx.send(f"{opponent.mention}, you have been challenged to a game of Tic-Tac-Toe by {ctx.author.mention}!\n"
                   f"{current_player.mention} ({symbol}) goes first.\n"
                   f"Send the number corresponding to your move (1-9) in chat.")

    def check_move(msg):
        return msg.author == current_player and msg.channel == ctx.channel

    def check_win():
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]
        for combo in winning_combinations:
            if board[combo[0]] == board[combo[1]] == board[combo[2]]:
                return True
        return False

    def check_draw():
        return all(symbol.isdigit() == False for symbol in board)

    while True:
        try:
            message = await bot.wait_for('message', check=check_move, timeout=60)
            move = message.content

            if move.isdigit() and 1 <= int(move) <= 9 and board[int(move) - 1].isdigit():
                board[int(move) - 1] = symbol
                await ctx.send(display_board())

                if check_win():
                    await ctx.send(f"Congratulations! {current_player.mention} ({symbol}) wins!")
                    return
                elif check_draw():
                    await ctx.send("It's a draw!")
                    return

                current_player = opponent if current_player == ctx.author else ctx.author
                symbol = symbols[players.index(current_player)]
                await ctx.send(f"{current_player.mention}, it's your turn ({symbol}). Send the number corresponding to your move (1-9) in chat.")
            else:
                await ctx.send("Invalid move. Please enter a number between 1 and 9 for an empty cell.")

        except asyncio.TimeoutError:
            await ctx.send("The game has timed out. It is now considered incomplete.")
            return

# Fun #2:
# Command: Coin Flip
@bot.command()
async def coinflip(ctx):
    """Play a game of coin flip."""
    result = random.choice(['Heads', 'Tails'])
    await ctx.send(f'The coin landed on {result}!')

# Fun #3:
# Command: Rock-Paper-Scissors
@bot.command()
async def rps(ctx, bet:int = 0):
    """Play a game of Rock-Paper-Scissors against me. Type //rps"""
    options = [
        {"name": "Rock", "emoji": "🪨"},
        {"name": "Paper", "emoji": "📄"},
        {"name": "Scissors", "emoji": "✂️"}
    ]

    # Create a list of choices for the user
    choices = [discord.SelectOption(label=option["name"], emoji=option["emoji"], value=option["name"]) for option in options]

    custom_id = f"rps_choice_{ctx.author.id}"
    # Create a select menu
    select = discord.ui.Select(
        placeholder="Choose your move",
        min_values=1,
        max_values=1,
        options=choices,
        custom_id=custom_id
    )

    # Create a message with the select menu
    message = await ctx.send("Select your move:", view=discord.ui.View().add_item(select))

    # Wait for the user's selection
    interaction, _ = await bot.wait_for("select_option", check=lambda i: i.component == select)

    user_choice = interaction.values[0]
    bot_choice = random.choice(options)

    await interaction.response.send_message(f"You chose {user_choice} {bot_choice['emoji']} and I chose {bot_choice['name']} {bot_choice['emoji']}.")

    if user_choice == bot_choice['name']:
        await interaction.response.send_message("It's a tie!")
    elif (
        (user_choice == "rock" and bot_choice['name'] == "scissors")
        or (user_choice == "paper" and bot_choice['name'] == "rock")
        or (user_choice == "scissors" and bot_choice['name'] == "paper")
    ):
        await interaction.response.send_message("You win!")
        if bet > 0:
            await interaction.response.send_message(f"You won {bet} coins!")
            # Increase user's balance by the bet amount
            user_bets[ctx.author.id] = user_bets.get(ctx.author.id, 0) + bet
    else:
        await interaction.response.send_message("I win!")
        if bet > 0:
            await interaction.response.send_message(f"You lost {bet} coins.")
            # Decrease user's balance by the bet amount
            user_bets[ctx.author.id] = user_bets.get(ctx.author.id, 0) - bet
  

# Fun #4:
# Command: Dice Roll
@bot.command()
async def diceroll(ctx):
    """Roll a dice."""
    result = random.randint(1, 6)
    await ctx.send(f'You rolled a {result}!')

# Fun #5:
# Command: Number Guessing Game
@bot.command()
async def numbergame(ctx):
    """Play a number guessing game against the bot."""
    number = random.randint(1, 100)
    attempts = 0
    while True:
        await ctx.send('Guess a number between 1 and 100.')
        guess = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
        guess = int(guess.content)
        attempts += 1
        if guess == number:
            await ctx.send(f'Congratulations! You guessed the number in {attempts} attempts.')
            break
        elif guess < number:
            await ctx.send('Too low! Try again.')
        else:
            await ctx.send('Too high! Try again.')




# Upcoming: Discord AI 👾

# Generate Images using AI
@bot.command()
async def generate_image(ctx, *, prompt):
    """ Generate Image using AI for your NFT, profiles & more """
    # Call the OpenAI API to generate the image
    response = openai.Image.create(
        prompt=prompt,
        n=1
    )

    image_url = response['data'][0]['url']
    await ctx.send(image_url)

    
# Chat with AI
@bot.command()
async def chat(ctx, *, message):
    """ Chat with your favorite bot GPT faster and easier """
    try:
        # Call the OpenAI API to chat with the model
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a bot that helps anime nerds."},
                {"role": "user", "content": message}
            ]
        )

        if response.choices:
            bot_reply = response.choices[0].message['content']
            await ctx.send(bot_reply)
        else:
            await ctx.send("Failed to generate a response.")
    except Exception as e:
        await ctx.send(f"An error occurred while generating the response: {str(e)}")


# Command: Weather 
@bot.command()
async def weather(ctx, *, location):
    """ Get Weather details of your location """
    weather_data = get_weather_data(location)
    await ctx.send(embed=weather_data)

def get_weather_data(location):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={W_API_KEY}&units=metric"
    response = httpx.get(url)
    data = response.json()
    if response.status_code == 200:
        city = data['name']
        country = data['sys']['country']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind_speed = data['wind']['speed']
        clouds = data['clouds']['all']
        precipitation = data.get('rain', {}).get('1h', 'N/A')
        sunrise = convert_unix_timestamp(data['sys']['sunrise'])
        sunset = convert_unix_timestamp(data['sys']['sunset'])
        condition = data['weather'][0]['description']
        emoji = WEATHER_EMOJIS.get(condition, "")

        embed = discord.Embed(title=f"Weather in {city}, {country}", description=f"Temperature: {temperature}°C", color=discord.Color.blue())
        embed.add_field(name="Conditions", value=f"{emoji} {condition}", inline=False)
        embed.add_field(name=f"{WEATHER_EMOJIS['Clear']} Humidity", value=f"{humidity}%", inline=True)
        embed.add_field(name=f"{WEATHER_EMOJIS['Mist']} Pressure", value=f"{pressure} hPa", inline=True)
        embed.add_field(name=f"{WEATHER_EMOJIS['Snow']} Wind Speed", value=f"{wind_speed} m/s", inline=True)
        embed.add_field(name=f"{WEATHER_EMOJIS['Clouds']} Cloudiness", value=f"{clouds}%", inline=True)
        embed.add_field(name=f"{WEATHER_EMOJIS['Rain']} Precipitation", value=f"{precipitation} mm/hr", inline=True)
        embed.add_field(name=f"{SUN_EMOJIS['sunrise']} Sunrise", value=sunrise, inline=True)
        embed.add_field(name=f"{SUN_EMOJIS['sunset']} Sunset", value=sunset, inline=True)
        
        return embed
    else:
        return f"Error: {data['message']}"

def convert_unix_timestamp(timestamp):
  converted_time = datetime.fromtimestamp(timestamp)
  return  converted_time.strftime("%Y-%m-%d %H:%M:%S")

# Command: Forecast
@bot.command()
async def forecast(ctx, *, location):
    """ Get 5 days weather forecast of your location """
    forecast_data = get_forecast_data(location)
    await ctx.send(embed=forecast_data)

def get_forecast_data(location):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={location}&appid={W_API_KEY}&units=metric"
    response = httpx.get(url)
    data = response.json()
    if response.status_code == 200:
        embed = discord.Embed(title=f"5-Day Weather Forecast for {location}", color=discord.Color.green())
        for forecast in data['list']:
            date_time = forecast['dt_txt']
            temperature = forecast['main']['temp']
            condition = forecast['weather'][0]['description']
            emoji = WEATHER_EMOJIS.get(condition, "")
            embed.add_field(name=date_time, value=f"{emoji} Temperature: {temperature}°C\nConditions: {condition}", inline=False)
            
        return embed

    else: 
      return f"Error: {data['message']}"

def get_temperature(location):
  url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={W_API_KEY}&units=metric"
  response = httpx.get(url)
  data = response.json()
  if response.status_code == 200:
    temperature = data['main']['temp']
    return temperature
  else:
    return f"Error: {data['message']}"

def get_weather_conditions(location):
  url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={W_API_KEY}&units=metric"
  response = httpx.get(url)
  data = response.json()
  if response.status_code == 200:
    conditions = data['weather'][0]['description']
    return conditions
  else:
    return f"Error: {data['message']}"



# Command: User Info
@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    """Display information about a user."""
    member = member or ctx.author
    roles = [role.name for role in member.roles]
    joined_at = member.joined_at.strftime('%b %d, %Y')
    user_info = f'Username: {member.name}\n' \
                f'Discriminator: {member.discriminator}\n' \
                f'User ID: {member.id}\n' \
                f'Joined Server: {joined_at}\n' \
                f'Roles: {", ".join(roles)}'
    await ctx.send(user_info)


# Command: Server Info
@bot.command()
async def serverinfo(ctx):
    """Display information about the server."""
    server = ctx.guild
    total_members = server.member_count
    server_info = f'Server Name: {server.name}\n' \
                  f'Server ID: {server.id}\n' \
                  f'Total Members: {total_members}\n' \
                  f'Server Region: {server.region}\n' \
                  f'Owner: {server.owner.mention}'
    await ctx.send(server_info)



# Command: Server Avatar
@bot.command()
async def server_avatar(ctx):
        """ Get the current server icon """
        if not ctx.guild.icon:
            return await ctx.send("This server does not have an icon...")

        format_list = []
        formats = ["JPEG", "PNG", "WebP"]
        if ctx.guild.icon.is_animated():
            formats.append("GIF")

        for img_format in formats:
            format_list.append(f"[{img_format}]({ctx.guild.icon.replace(format=img_format.lower(), size=1024)})")

        embed = discord.Embed()
        embed.set_image(url=f"{ctx.guild.icon.with_size(256).with_static_format('png')}")
        embed.title = "Icon formats"
        embed.description = " **-** ".join(format_list)

        await ctx.send(f"🖼 Icon to **{ctx.guild.name}**", embed=embed)

# Command: Get User Avatar
@bot.command()
async def avatar(ctx, user: discord.Member = None):
        """ Get the avatar of you or someone else """
        user = user or ctx.author

        avatars_list = []

        def target_avatar_formats(target):
            formats = ["JPEG", "PNG", "WebP"]
            if target.is_animated():
                formats.append("GIF")
            return formats

        if not user.avatar and not user.guild_avatar:
            return await ctx.send(f"**{user}** has no avatar set, at all...")

        if user.avatar:
            avatars_list.append("**Account avatar:** " + " **-** ".join(
                f"[{img_format}]({user.avatar.replace(format=img_format.lower(), size=1024)})"
                for img_format in target_avatar_formats(user.avatar)
            ))

        embed = discord.Embed(colour=user.top_role.colour.value)

        if user.guild_avatar:
            avatars_list.append("**Server avatar:** " + " **-** ".join(
                f"[{img_format}]({user.guild_avatar.replace(format=img_format.lower(), size=1024)})"
                for img_format in target_avatar_formats(user.guild_avatar)
            ))
            embed.set_thumbnail(url=user.avatar.replace(format="png"))

        embed.set_image(url=f"{user.display_avatar.with_size(256).with_static_format('png')}")
        embed.description = "\n".join(avatars_list)

        await ctx.send(f"🖼 Avatar to **{user}**", embed=embed)        
 
# Anime Quote Command
@bot.command()
async def quote(ctx):
    """ Get Random Anime quote of your favorite character """
    quote_data = get_anime_quote()
    if quote_data:
        anime = quote_data["anime"]
        character = quote_data["character"]
        quote = quote_data["quote"]
        image_url = get_anime_image(anime)
       
        embed = discord.Embed(title="Anime Quote of the Day", color=discord.Color.green())
        embed.set_image(url=image_url)
        embed.add_field(name="Anime", value=anime, inline=False)
        embed.add_field(name="Character", value=character, inline=False)
        embed.add_field(name="Quote", value=quote, inline=False)
        
        await ctx.send(embed=embed)
    else:
        await ctx.send("Failed to fetch the anime quote.")

def get_anime_quote():
    response = httpx.get("https://animechan.vercel.app/api/random")
    quote_data = response.json()
    if response.status_code == 200:
        quote_data = response.json()
        return quote_data
    if "anime" in quote_data and "character" in quote_data and "quote" in quote_data:
        anime = quote_data["anime"]
        character = quote_data["character"]
        quote = quote_data["quote"]
        return {"anime": anime, "character": character, "quote": quote}
    else:
        return None

def get_anime_image(anime_name):
    response = httpx.get(f"https://kitsu.io/api/edge/anime?filter[text]={anime_name}&page[limit]=1")
    if response.status_code == 200:
        anime_data = response.json()
        if anime_data["data"]:
            anime = anime_data["data"][0]
            image_url = anime["attributes"]["posterImage"]["original"]
            return image_url
    return None


# Command: Quora Search
@bot.command()
async def answer(ctx, *, query):
    """Searches Quora and displays the top 5 search results."""
    author = ctx.author.mention
    await ctx.send(f"Searching Quora for: {query}{author}")
    async with ctx.typing():
        results = search(query + " site:quora.com", num=5, stop=5, pause=2)
        for result in results:
            await ctx.send(f"\n:point_right: {result}")
    
    await ctx.send("Have any more questions? Feel free to ask again!")
       

# Command: Google Search
@bot.command()
async def find(ctx,*, query):
    """Searches Google and displays the top 5 search results."""
    author = ctx.author.mention
    await ctx.send(f"Searching Google for: {query}{author}")
    async with ctx.typing():
		   for j in search(query, tld="co.in", num=5, stop=5, pause=2): 
					 await ctx.send(f"\n:point_right: {j}")
    await ctx.send("Have any more questions:question:\nFeel free to ask again :smiley: !")          
    

# Command: YouTube Search
@bot.command()
async def searchyt(ctx,*, query):
    """Searches YouTube and displays the top 5 search results."""
    author = ctx.author.mention
    await ctx.send(f"Searching YouTube for: {query}{author}")
    async with ctx.typing():
      search = Search(query, limit = 7)
      results = search.result()
      
      if results['result']:
          for i in range(7):
              video = results['result'][i]
              title = video['title']
              url = f"https://www.youtube.com/watch?v={video['id']}"
              await ctx.send(f"Top Result: {title}\n{url}")
      else:
          await ctx.send("No results found. Please try a different query.")


    await ctx.send("Have any more questions:question:\nFeel free to ask again :smiley: !")    

# Command: Create New Embed
@bot.command()
async def new_embed(ctx, *, msg: str = None):
        """ Send your messages as an Embed within seconds. Ex: !new_embed for help

        Example: !embed title=test this | description=some words | color=3AB35E | image=add your url

        You do NOT need to specify every property, only the ones you want.

        **All properties and the syntax:**
        - title=<words>
        - description=<words>
        - color=<hex_value>
        - image=<url_to_image> (must be https)
        - thumbnail=<url_to_image>
        - author=<words> **OR** author=name=<words> icon=<url_to_image>
        - footer=<words> **OR** footer=name=<words> icon=<url_to_image>
        - field=name=<words> value=<words> (you can add as many fields as you want)
        - ptext=<words>

        NOTE: After the command is sent, the bot will delete your message and replace it with the embed. Make sure you have it saved or else you'll have to type it all again if the embed isn't how you want it.
        
        PS: Hyperlink text like so:
        \[text](https://www.whateverlink.com)

        PPS: Force a field to go to the next line with the added parameter inline=False """
        if msg:
                ptext = title = description = image = thumbnail = color = footer = author = None
                embed_values = msg.split('|')
                for i in embed_values:
                    if i.strip().lower().startswith('ptext='):
                        ptext = i.strip()[6:].strip()
                    elif i.strip().lower().startswith('title='):
                        title = i.strip()[6:].strip()
                    elif i.strip().lower().startswith('description='):
                        description = i.strip()[12:].strip()
                    elif i.strip().lower().startswith('desc='):
                        description = i.strip()[5:].strip()
                    elif i.strip().lower().startswith('image='):
                        image = i.strip()[6:].strip()
                    elif i.strip().lower().startswith('thumbnail='):
                        thumbnail = i.strip()[10:].strip()
                    elif i.strip().lower().startswith('colour='):
                        color = i.strip()[7:].strip()
                    elif i.strip().lower().startswith('color='):
                        color = i.strip()[6:].strip()
                    elif i.strip().lower().startswith('footer='):
                        footer = i.strip()[7:].strip()
                    elif i.strip().lower().startswith('author='):
                        author = i.strip()[7:].strip()
                  
                    else:
                        if description is None and not i.strip().lower().startswith('field='):
                            description = i.strip()

                if color:
                    if color.startswith('#'):
                        color = color[1:]
                    if not color.startswith('0x'):
                        color = '0x' + color

                if ptext is title is description is image is thumbnail is color is footer is author is None and 'field=' not in msg:
                    await ctx.message.delete()
                    return await ctx.send(content=None,
                                                       embed=discord.Embed(description=msg))

                if color:
                    em = discord.Embed(title=title, description=description, color=int(color, 16))
                else:
                    em = discord.Embed(title=title, description=description)
                for i in embed_values:
                    if i.strip().lower().startswith('field='):
                        field_inline = True
                        field = i.strip().lstrip('field=')
                        field_name, field_value = field.split('value=')
                        if 'inline=' in field_value:
                            field_value, field_inline = field_value.split('inline=')
                            if 'false' in field_inline.lower() or 'no' in field_inline.lower():
                                field_inline = False
                        field_name = field_name.strip().lstrip('name=')
                        em.add_field(name=field_name, value=field_value.strip(), inline=field_inline)
                if author:
                    if 'icon=' in author:
                        text, icon = author.split('icon=')
                        if 'url=' in icon:
                            em.set_author(name=text.strip()[5:], icon_url=icon.split('url=')[0].strip(), url=icon.split('url=')[1].strip())
                        else:
                            em.set_author(name=text.strip()[5:], icon_url=icon)
                    else:
                        if 'url=' in author:
                            em.set_author(name=author.split('url=')[0].strip()[5:], url=author.split('url=')[1].strip())
                        else:
                            em.set_author(name=author)

                if image:
                    em.set_image(url=image)
                if thumbnail:
                    em.set_thumbnail(url=thumbnail)
                if footer:
                    if 'icon=' in footer:
                        text, icon = footer.split('icon=')
                        em.set_footer(text=text.strip()[5:], icon_url=icon)
                    else:
                        em.set_footer(text=footer)
                await ctx.send(content=ptext, embed=em)
            
        else:
            msg = '```How to use the >embed command:\nExample: >embed title=test this | description=some words | color=3AB35E | field=name=test value=test\n\nYou do NOT need to specify every property, only the ones you want.' \
                  '\nAll properties and the syntax (put your custom stuff in place of the <> stuff):\ntitle=<words>\ndescription=<words>\ncolor=<hex_value>\nimage=<url_to_image> (must be https)\nthumbnail=<url_to_image>\nauthor=<words> **OR** author=name=<words> icon=<url_to_image>\nfooter=<words> ' \
                  '**OR** footer=name=<words> icon=<url_to_image>\nfield=name=<words> value=<words> (you can add as many fields as you want)\nptext=<words>\n\nNOTE: After the command is sent, the bot will delete your message and replace it with ' \
                  'the embed. Make sure you have it saved or else you\'ll have to type it all again if the embed isn\'t how you want it.\nPS: Hyperlink text like so: [text](https://www.whateverlink.com)\nPPS: Force a field to go to the next line with the added parameter inline=False```'
            await ctx.send(msg)
        try:
            await ctx.message.delete()
        except:
            pass 



# AniList API endpoint for GraphQL
api_url = "https://graphql.anilist.co"

@bot.command()
async def manga(ctx, *, manga_name):
    try:
        # Define your GraphQL query
        query = '''
            query ($search: String) {
                Media(type: MANGA, search: $search) {
                    title {
                        romaji
                    }
                    description
                    siteUrl
                    chapters
                    volumes
                    coverImage {
                        large
                    }
                    genres
                    status
                    startDate {
                        year
                        month
                        day
                    }
                    endDate {
                        year
                        month
                        day
                    }
                    externalLinks {  # Add the direct manga URL here
                        url
                        site
                    }
                    averageScore
                }
            }
        '''

        # Variables for the query
        variables = {
            "search": manga_name
        }

        # Make the API request
        response = requests.post(api_url, json={"query": query, "variables": variables})
        data = response.json()

        # Process the data and send an embed to Discord
        manga_data = data["data"]["Media"]
        if manga_data:
            embed = discord.Embed(title=manga_data['title']['romaji'], description=manga_data['description'], url=manga_data['siteUrl'])
            embed.set_image(url=manga_data['coverImage']['large'])
            embed.add_field(name="Chapters", value=manga_data['chapters'], inline=True)
            embed.add_field(name="Volumes", value=manga_data['volumes'], inline=True)
            embed.add_field(name="Genres", value=', '.join(manga_data['genres']), inline=False)
            embed.add_field(name="Status", value=manga_data['status'], inline=True)
            embed.add_field(name="Average Score", value=manga_data['averageScore'], inline=True)
            embed.add_field(name="Start Date", value=f"{manga_data['startDate']['year']}-{manga_data['startDate']['month']}-{manga_data['startDate']['day']}", inline=False)

            if manga_data['endDate']:
                embed.add_field(name="End Date", value=f"{manga_data['endDate']['year']}-{manga_data['endDate']['month']}-{manga_data['endDate']['day']}", inline=True)

            if manga_data['externalLinks']:
                for link in manga_data['externalLinks']:
                    if link['site'] == "AniList":
                        embed.add_field(name="Read Manga", value=f"[Read {manga_data['title']['romaji']} Online]({link['url']})", inline=False)
            
            await ctx.send(embed=embed)
        else:
            await ctx.send("Manga not found.")

    except Exception as e:
        await ctx.send("An error occurred while fetching manga info.")

@bot.command()
async def character(ctx, *, character_name):
    try:
        # Define your GraphQL query for character search
        query = '''
            query ($search: String) {
                Character(search: $search) {
                    name {
                        full
                    }
                    description
                    image {
                        large
                    }
                    siteUrl
                    media {
                        nodes {
                            title {
                                romaji
                            }
                            type
                        }
                    }
                    favourites
                    dateOfBirth {
                        year
                        month
                        day
                    }
                }
            }
        '''

        # Variables for the query
        variables = {
            "search": character_name
        }

        # Make the API request
        response = requests.post(api_url, json={"query": query, "variables": variables})
        data = response.json()

        # Process the data and send an embed to Discord
        character_data = data["data"]["Character"]
        if character_data:
            embed = discord.Embed(title=character_data['name']['full'], url=character_data['siteUrl'])
            embed.set_image(url=character_data['image']['large'])

            # Adjust truncation limits and customize fields
            
            description = character_data['description'][:1000] + "..." if len(character_data['description']) > 1000 else character_data['description']
            embed.description = description
            
            # Limit media information length to fit within the embed
            if character_data['media']['nodes']:
                media_info = "\n".join(f"{media['title']['romaji']} - {media['type']}" for media in character_data['media']['nodes'][:1])
                embed.add_field(name="Appears in", value=media_info, inline=False)
            
            if character_data['dateOfBirth']:
                dob = f"{character_data['dateOfBirth']['year']}-{character_data['dateOfBirth']['month']}-{character_data['dateOfBirth']['day']}"
                embed.add_field(name="Date of Birth", value=dob, inline=True)
            
            embed.add_field(name="Favourites", value=character_data['favourites'], inline=True)
            embed.add_field(name="More Info", value=f"[Full Character Profile]({character_data['siteUrl']})")
            
            await ctx.send(embed=embed)
        else:
            await ctx.send("Character not found.")

    except Exception as e:
        await ctx.send("An error occurred while fetching character info.")


@bot.command()
async def studio(ctx, *, anime_title):
    try:
        # Define your GraphQL query for anime search
        query = '''
            query ($search: String) {
                Media(search: $search, type: ANIME) {
                    title {
                        romaji
                    }
                    studios {
                        nodes {
                            name
                            isAnimationStudio
                        }
                    }
                    coverImage {
                        medium
                    }
                    siteUrl
                    status
                    episodes
                    startDate {
                        year
                    }
                }
            }
        '''

        # Variables for the query
        variables = {
            "search": anime_title
        }

        # Make the API request
        response = requests.post(api_url, json={"query": query, "variables": variables})
        data = response.json()

        # Process the data and send an embed to Discord
        anime_data = data["data"]["Media"]
        if anime_data:
            embed = discord.Embed(title=anime_data['title']['romaji'], url=anime_data['siteUrl'], color=discord.Color.dark_blue())
            embed.set_thumbnail(url=anime_data['coverImage']['medium'])
            
            if anime_data['studios']['nodes']:
                studio_names = [studio['name'] for studio in anime_data['studios']['nodes'] if studio['isAnimationStudio']]
                studio_info = "\n".join(studio_names)
                if studio_info:
                    embed.add_field(name="Animation Studios", value=studio_info, inline=False)
                else:
                    embed.add_field(name="Studios", value=", ".join(studio['name'] for studio in anime_data['studios']['nodes']), inline=False)
            
            embed.add_field(name="Status", value=anime_data['status'], inline=True)
            embed.add_field(name="Episodes", value=anime_data['episodes'], inline=True)
            
            if anime_data['startDate']['year']:
                embed.add_field(name="Start Year", value=anime_data['startDate']['year'], inline=True)
            
            await ctx.send(embed=embed)
        else:
            await ctx.send("Anime not found.")

    except Exception as e:
        await ctx.send("An error occurred while fetching anime info.")


        




  

  

      
        







     




    


            



    


            
        


        
            


        

        
        


                


        


        
      



















    

    
  
                























            
            










      













    

                  



        
        
        

        


        
       
            


# Command: Game Role
@bot.command()
async def gamerole(ctx, username, *, role_name):
    ''' Assign a role to the one you love and create your own game community '''
    # Check if the role already exists in the server.
    existing_role = discord.utils.get(ctx.guild.roles, name=role_name)

    # Get the member (user) object based on the provided username or mention.
    member = discord.utils.get(ctx.guild.members, name=username) or ctx.message.mentions[0]

    if existing_role:
        # Add the existing role to the user.
        await member.add_roles(existing_role)
        await ctx.send(f"{member.mention} has been assigned the '{role_name}' role.")
    else:
        # Create the role with the specified name.
        new_role = await ctx.guild.create_role(name=role_name)

        # Add the newly created role to the user.
        await member.add_roles(new_role)
        await ctx.send(f"Role '{role_name}' didn't exist, so it has been created, and {member.mention} has been assigned the role.")
       

        
bot.start_time = datetime.datetime.utcnow()
bot.command_count = {}
bot.messages_sent = []
bot.messages_received = []
bot.mentions = []
bot.keyword_log = []

# Command: Bot Statistics
@bot.command()
async def stats(ctx):
    """Bot stats you want to know."""
    uptime = datetime.datetime.utcnow() - bot.start_time
    days, hours, minutes, seconds = uptime.days, uptime.seconds // 3600, (uptime.seconds // 60) % 60, uptime.seconds % 60
    time = f'{days} days, {hours} hours, {minutes} minutes, and {seconds} seconds'

    if not bot.command_count:
        most_used_cmd = 'Not enough info'
    else:
        most_used_cmd = max(bot.command_count, key=bot.command_count.get)
        total_usage = bot.command_count[most_used_cmd]
        plural = '' if total_usage == 1 else 's'
        most_used_cmd = f'{most_used_cmd} - {total_usage} use{plural}'


    msg_sent = len(ctx.bot.messages_sent)
    msg_received = len(ctx.bot.messages_received)
    mentions = len(ctx.bot.mentions)
    servers = len(bot.guilds)
    channels = sum(len(guild.channels) for guild in bot.guilds)
    keywords_logged = ctx.bot.keyword_log

    embed = discord.Embed(title='Bot Stats', color=0x32441c)
    embed.add_field(name='Uptime', value=time, inline=False)
    embed.add_field(name='Most Used Command', value=most_used_cmd, inline=False)
    embed.add_field(name='Messages Sent', value=str(msg_sent))
    embed.add_field(name='Messages Received', value=str(msg_received))
    embed.add_field(name='Mentions', value=str(mentions))
    embed.add_field(name='Servers', value=str(servers))
    embed.add_field(name='Channels', value=str(channels))
    embed.add_field(name='Keywords Logged', value=str(keywords_logged))

    await ctx.send(embed=embed)        
            
        
        

# Command: Ping
@bot.command()
async def ping(ctx):
    """Check the bot's latency."""
    latency = bot.latency * 1000
    await ctx.send(f'Pong! Latency: {latency:.2f} ms')

# Command: Command List
@bot.command()
async def commands(ctx):
    """Display a list of available commands."""
    command_list = []
    for command in bot.commands:
        command_list.append(f'{command.name}: {command.help}')
    await ctx.send('\n'.join(command_list))
    


keep_alive()

       
    

# Run the bot with your bot token
bot.run(YOUR_DISCORD_BOT_TOKEN)
