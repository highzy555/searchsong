import discord
from discord.ext import commands
import os
import random
from googleapiclient.discovery import build
import nextcord
import sys
from os import system
from nextcord.ext import commands
from flask import Flask, render_template
from threading import Thread
app = Flask('')
@app.route('/')
def home():
  return "bot python is online!"
def index():
  return render_template("index.html")
def run():
  app.run(host='0.0.0.0', port=8080)
def H():
  t = Thread(target=run)
  t.start()

# ตั้งค่า Discord Bot Token
bot_key = os.environ['bot']
TOKEN = bot_key
idchannel = 1235479854519156849
name = [1153965156376776754]
H()

# ตั้งค่า YouTube Data API Key
KEYS = os.environ['key']
DEVELOPER_KEY = KEYS
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

# สร้างบอท
bot = commands.Bot(
    command_prefix='!',
    help_command=None,
    intents=nextcord.Intents.all(),
    strip_after_prefix=True,
    case_insensitive=True, 
)

# สร้างออบเจกต์ YouTube API Client
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)


class searchsongs(nextcord.ui.Modal):
    def __init__(self):
        super().__init__(title='Blackmarket | ค้นหาเพลง', timeout=None, custom_id='bmk-searchsongs')
        self.search = nextcord.ui.TextInput(
            label = 'กรอกเพลงที่ต้องการค้นหา',
            placeholder =f'xxxxxxxxxx',
            style = nextcord.TextInputStyle.short,
            required = True
        )
        self.add_item(self.search)
    async def callback(self, interaction: nextcord.Interaction):
        search = str(self.search.value)
        url, title, thumbnail_url = search_youtube(search)
        channelLog = bot.get_channel(idchannel)
        if (channelLog):
                        embed = nextcord.Embed()
                        embed.description = f'''**Black Market ประวัติการค้นหา**
\n> **ชื่อผู้ใช้งาน** 
\n** <@{interaction.user.id}> **

> **ชื่อที่ค้นหา** 
\n** __{search}__ **

> **ชื่อเพลง**
\n** __{title}__ **

> **ลิ้งค์เพลง** 
\n** __{url}__**
'''
                        embed.set_footer(text=f'BMK - {interaction.user.name}', icon_url=interaction.user.avatar.url)
                        embed.set_thumbnail(url=f"{thumbnail_url}")
                        embed.color = 0x7300ff
                        await channelLog.send(embed=embed)
        if search:
            embed=nextcord.Embed(title="** Black Market! | ค้นหาเพลง**", description=f"**ชื่อที่ค้นหา __{search}__\nเพลงที่ค้นหาเจอ __{title}__\n__{url}__ **")
            embed.set_image(url=f"{thumbnail_url}")
            embed.set_thumbnail(url=f"https://cdn.discordapp.com/attachments/1235224973954650125/1235429965839859784/ed631e9928941f27d409a8dffd18f3b4.jpgw700wp.webp?ex=66345751&is=663305d1&hm=7f94eac89e7605a43112856dcd3b78dffaa7a7072eb947743a0dc8d19c63f3b5&")
            embed.set_footer(text=f'BMK - {interaction.user.name}', icon_url=interaction.user.avatar.url)
            embed.color = 0x7300ff
            await interaction.send(embed=embed, ephemeral=True)
        else:
            await interaction.send(f'{interaction.user.name} ไม่พบเพลง "{search}" บนยูทูป')                        

# ฟังก์ชันค้นหาและสุ่มเพลงจากยูทูป
def search_youtube(query, max_results=10):
    search_response = youtube.search().list(
        q=query,
        type='video',
        part='id,snippet',
        maxResults=max_results
    ).execute()

    # รับลิสต์ไอดีวิดีโอที่ค้นหาได้
    video_ids = [search_result['id']['videoId'] for search_result in search_response['items']]

    # ถ้าไม่มีวิดีโอที่ค้นหาได้ ให้ส่งคืนค่าว่าง
    if not video_ids:
        return None, None

    # สุ่มไอดีวิดีโอ
    random_video_id = random.choice(video_ids)

    # รับข้อมูลของวิดีโอที่สุ่มได้
    video_response = youtube.videos().list(
        id=random_video_id,
        part='snippet'
    ).execute()

    # สร้างลิงก์ยูทูปของวิดีโอที่สุ่มได้
    url = f'https://www.youtube.com/watch?v={random_video_id}'

    return url, video_response['items'][0]['snippet']['title'], video_response['items'][0]['snippet']['thumbnails']['default']['url']



class setupView(nextcord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(
        emoji='<a:selebzmarket:1138497286817722508>',
        label='ค้นหาเพลง',
        custom_id='bmk-searchsongs',
        style=nextcord.ButtonStyle.primary,
        row=1
    )
    async def searchsong(self, button: nextcord.Button, interaction: nextcord.Interaction):
        await interaction.response.send_modal(searchsongs())

@bot.slash_command(
    name='search',
    description='ค้นหาเพลง ตามคำที่คุณค้นหา',
)
async def searchsong(interaction: nextcord.Interaction):
    if (interaction.user.id not in name):
        return await interaction.response.send_message(content='[ERROR] No Permission For Use This Command.', ephemeral=True)
    embed = nextcord.Embed()
    embed.set_image(url='https://cdn.discordapp.com/attachments/1235224973954650125/1235429965839859784/ed631e9928941f27d409a8dffd18f3b4.jpgw700wp.webp?ex=66345751&is=663305d1&hm=7f94eac89e7605a43112856dcd3b78dffaa7a7072eb947743a0dc8d19c63f3b5&')
    embed.title = '** __Black Market! | ระบบค้นหาเพลง__ **'
    embed.description = '**__ใช้งานง่ายเพียงกดปุ่มด้านล่างนี้__**'
    embed.set_footer(text='© 2024 Black Market! All rights reserved')
    embed.color = 0x7300ff 
    await interaction.channel.send(embed=embed, view=setupView())

# คำสั่งสุ่มเพลง
@bot.command()
async def high(ctx, *, query):
    video_url, video_title = search_random_song(query)
    if video_url and video_title:
        await ctx.send(f'** ค้นหา -  __{query}__ : {video_title}\n{video_url} **')
    else:
        await ctx.send(f'** # __ไม่มีวิดีโอที่คุณค้นหาครับ__ **')
        
@bot.event
async def on_ready():
    bot.add_view(setupView())
    system('cls')
    print(f"Bot {bot.user.name} Online!")
    await bot.change_presence(activity=nextcord.Streaming(name="Black Market!", url="https://www.twitch.tv/example_channel"))

# รันบอท
bot.run(TOKEN)
