import discord
import asyncio
from discord.ext import commands
import re
import os
from bs4 import BeautifulSoup
import requests


client = discord.Client()
bot = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print('Logged on as', client.user)


@bot.listen() #@client.event
async def on_message(message):
    # don't respond to ourselves
    #print(message.content)
    if message.author == client.user:
        return
    else:
        try:
            print(message.channel.id)
            link_regex = re.findall("http[s]?://(pi?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", str(message.content))
            print(link_regex)

            if len(link_regex) > 0 and message.channel.id != 865098188893585418 and message.channel.id != 850780391752466462 and message.channel.id != 857347995309178910 and message.channel.id != 850783338830888990:
            #if link_regex in message: # and message.channel.id != 877242893658636340:
                channel = bot.get_channel(877242893658636340)
                await channel.send(f'{str(message.author)[0:-5]} just shared this link!')
                await channel.send(link_regex[0])
                await message.delete()

            if len(link_regex) == 0:
                print("no links ")
                return


        except Exception as e:
            await message.delete()
            print(e)
            message.channel.id = 863322592835796992


token = ""

@bot.command()
async def love(x):
    await x.send(f'I love  {str(x.author)[0:-5]}')
    await x.send("<:smew_yeah:851238239883755530>")

from Y import YTDLSource

''''''
import youtube_dl
global q
q = []

@bot.command(pass_context=True)
async def guess(ctx, m):
    import random
    r = random.randrange(0,10)
    print(r)
    print(r)
    await ctx.send(f"{m}")
    if m == str(r):
        await ctx.send(f'!!  :) :D :) yay {str(ctx.author)[0:-5]} wins!!')
        return
    else:
        await ctx.send(f"{r}")
        '''
        x = input("guess a 4 digit number: ")
        print("try again")
        '''

@bot.command(pass_context=True)
async def start(ctx):
    channel = ctx.message.author.voice.channel
    global voice
    voice = await channel.connect()
   
import time

@bot.command()
async def ping(ctx):
    btime = time.time()
    p = os.system("ping -c 1 discord")
    dtime = time.time() - btime
    await ctx.send(f'Pong! :ping_pong: Response time: {round(dtime*1000,2)}ms')

@bot.command()
async def ip(ctx):
    import requests
    import socket
    import time
    from requests import get

    # await ctx.send('getting weather data')
    local_ip = socket.gethostbyname(socket.gethostname())
    print('local ip:', local_ip)

    start_time = time.time()
    # print(start_time)

    public_ip = get('https://api.ipify.org').text
    print('public ip:', public_ip)
    await ctx.send(f'{public_ip}')

    ip_data = get('http://ip-api.com/json/' + public_ip).text
    print(type(ip_data), ip_data)
    
@bot.command(pass_context=True)
async def wiki(ctx, wiki_query):
    site = "https://en.wikipedia.org/wiki/"+str(wiki_query)
    print(site)
    r = requests.get(site, timeout=10)
    soup = BeautifulSoup(r.content, 'html.parser')
    #ctx.send(soup.find_all(""))
    c = soup.find_all("p")
    print(str(c))

    link_regex = re.findall("http[s]?://(pi?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", str(c))
    print(link_regex)
    for x in c:
        #await ctx.delete()
        await ctx.send(str(x)[0:2000])
    #await ctx.send(f'{str(c)[0:1000]}')#[0:2000])
#await ctx.send(str(c)[2000:4000])

@bot.command(pass_context=True)
async def queue(ctx, youtube_url):
    if youtube_url not in q:
        q.append(youtube_url)

@bot.command(pass_context=True)
async def stop(ctx):
    voice.stop()

@bot.command(pass_context=True)
async def pause(ctx):
    voice.pause()

@bot.command(pass_context=True)
async def resume(ctx):
    voice.resume()

@bot.command(pass_context=True)
async def fs(ctx):
    print(q)
    q.pop(0)
    print("after pop",q)
    voice.stop()
    x = await YTDLSource.from_url(q[0], loop=bot.loop)
    voice.play(x)

@bot.command(pass_context=True)
async def p(ctx, *song):

    if "https" in song:
        q.append(song)
        return

    if len(q) > 1:
        q.pop(0)

    song = " ".join(song[:])
    site = 'https://www.youtube.com/results?search_query=' + str(song)
    print(site)
    r = requests.get(site, timeout=5)

    soup = BeautifulSoup(r.content, 'html.parser')
    regex = re.findall("/watch\?+\w+=+\w{11}", str(soup))  # ("^watch?v=\w+{11}", soup)

    first_result = 'https://www.youtube.com' + regex[0]

    if first_result not in q:
        q.append(first_result)

    voice.stop()
    x = await YTDLSource.from_url(first_result, loop=bot.loop)
    x.volume = 0.2

    voice.play(x)
    '''
    voice.stop()
    x = await YTDLSource.from_url(first_result, loop=bot.loop)
    voice.play(x)
    '''
@bot.command(pass_context=True)
async def play(ctx):
    x = await YTDLSource.from_url(q[0], loop=bot.loop)
    voice.play(x)

bot.run(token)
bot.add_listener(on_message)
client.run(token)
