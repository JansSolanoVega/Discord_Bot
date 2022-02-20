from inspect import BoundArguments
import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import random
from discord.ext.commands.converter import StoreChannelConverter
from discord.ext.commands.core import bot_has_guild_permissions
import requests
import json
import youtube_dl
import os

intents = discord.Intents().all()                                
clientXD = commands.Bot(command_prefix = '*', intents = intents)
sadWords=["sad","depressed","unhappy","suffering"]
MotivationalMessages=["everything will be ok","thats fine","you're a great bot"]

def getQuote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data=json.loads(response.text)
  cita=json_data[0]["q"]+" -Author: "+json_data[0]["a"]
  return cita

@clientXD.command()
async def hello(ctx,arg1,arg2):
  await ctx.send(f'arg1 : {arg1} arg2: {arg2}')

@clientXD.command()
async def helloxd(ctx,*args):
  for arg in args:
    await ctx.send("arg"+str(args.index(arg)+1)+": "+str(arg))
  
@clientXD.command()
async def InfoClient(ctx,*args):
  await ctx.send(ctx.author)
  await ctx.send(ctx.guild)

@clientXD.event
async def on_message(message):
  if message.author==clientXD.user:
    return
  mensaje=message.content

  if mensaje.startswith("ga"):
    await message.channel.send("u're a fucking idiot")
  if "quote" in mensaje:
    await message.channel.send(getQuote())
  if any(i in mensaje for i in sadWords):
    await message.channel.send(random.choice(MotivationalMessages))
  await clientXD.process_commands(message)

@clientXD.event
async def on_ready():
    print("Bot is ready.")

@clientXD.event
async def on_member_join(member):
    print(type(member))
    print(f"{member} ha ingresado al servidor")

@clientXD.event
async def on_member_remove(member):
    print(f"{member} ha salido del servidor")

@clientXD.command()
async def ping(ctx):
    await ctx.send(f"pang {round(clientXD.latency*1000)} ms")

@clientXD.command(aliases=["8ball","test"])
async def _8ball(ctx,*,question):
    responses = ["It is certain.",
                "It is decidedly so.",
                "Without a doubt.",
                "Yes - definitely.",
                "You may rely on it.",
                "As I see it, yes.",
                "Most likely.",
                "Outlook good.",
                "Yes.",
                "Signs point to yes.",
                "Reply hazy, try again.",
                "Ask again later.",
                "Better not tell you now.",
                "Cannot predict now.",
                "Concentrate and ask again.",
                "Don't count on it.",
                "My reply is no.",
                "My sources say no.",
                "Outlook not so good.",
                "Very doubtful.",
                'Chances are low',
                'Wouldnt count on it.',
                'Nope',
                'Try again',
                'Think hard and try again',
                'Go away before I eat your cat',
                'I thought too hard and died.']
    await ctx.send(f"Question: {question}\nAnswer:{random.choice(responses)}")

@clientXD.command()
async def clear(cx,amount=2):
    await cx.channel.purge(limit=amount)

@clientXD.command()
async def join(ctx):
    if ctx.author.voice is None:
      await ctx.send("You are not in a voice channel")
      return
    channel=ctx.author.voice.channel
    if ctx.voice_client is None:#el bot no esta conectado a ningun canal
      await channel.connect()
    else:
      await ctx.voice_client.move_to(channel) 

@clientXD.command()
async def leave(ctx):
    voice_client = ctx.voice_client

    if voice_client is not None:
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

@clientXD.command()
async def play(ctx,url):
  ctx.voice_client.stop()#stop the bot voice
  FFMPEG_OPTIONS={'before_options':'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options':'-vn'}
  YDL_OPTIONS={'format':'bestaudio'}
  voiceBOT=ctx.voice_client
  with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
    info = ydl.extract_info(url,download=False)
    #f = open(r"C:\Users\ZetansSV\Desktop\BOT\creando.txt","a+")
    #f.write(str(info))   
    #f.close()
    #otra forma
    #with open(r"C:\Users\ZetansSV\Desktop\BOT\memoriaTextos.txt","a+") as f:#a is for appending the text at the end of the file(a is also for files that don't exist)
    #  f.write(str(info))
    #  f.write("\n\n")
    url2=info['formats'][0]['url']
    nameSong=info['title']
    source=await discord.FFmpegOpusAudio.from_probe(url2,**FFMPEG_OPTIONS)#** is to show that is a dictionary
    voiceBOT.play(source)
    await ctx.send("**Now playing: **"+str(nameSong))

@clientXD.command()
async def pause(ctx):
  voiceBOT=ctx.voice_client
  if voiceBOT.is_playing():
    voiceBOT.pause()
    await ctx.send("**Paused** ⏸️")
  else:
    await ctx.send("Voice is not playing anything")

@clientXD.command()
async def resume(ctx):
  voiceBOT=ctx.voice_client
  if voiceBOT.is_paused():
    voiceBOT.resume()
    await ctx.send("**Playing** ▶️")
  else:
    await ctx.send("Voice is not paused")

@clientXD.command()
async def loop(ctx):
    """Loops the currently playing song.
    Invoke this command again to unloop the song.
    """

    if not ctx.voice_client.is_playing:
        return await ctx.send('Nothing being played at the moment.')

    # Inverse boolean value to   loop and unloop.
    ctx.voice_client.loop = not ctx.voice_client.loop
    await ctx.message.add_reaction('✅')
    
'''@clientXD.command()
async def loop(ctx,number):
  voiceBOT=ctx.voice_client
  music_being_played=voiceBOT.source
  if voiceBOT.is_playing():
    for i in range(0,int(number)):
      print(music_being_played)
      await voiceBOT.is_playing
      voiceBOT.play(music_being_played) 
      await ctx.send(f"**{number-i} Times left**")
      
  else:
    await ctx.send("No music is being played")
'''


#TicTacToeGame
player1=""
player2=""
playerNow=""
gameIsRunning=False
board=[]
finish=False
symbol=0
winning=[
  [0,1,2],
  [3,4,5],
  [6,7,8],
  [0,3,6],
  [1,4,7],
  [2,5,8],
  [0,4,8],
  [2,4,6],
]

@clientXD.command()
async def tictactoe(ctx, player1XD : discord.Member, player2XD : discord.Member):
  global player1
  global player2
  global gameIsRunning
  global playerNow
  if not gameIsRunning:
    finish=0
    player1=player1XD
    player2=player2XD
    gameIsRunning=True
    global board 
    board=[
      ":white_large_square:",":white_large_square:",":white_large_square:",
      ":white_large_square:",":white_large_square:",":white_large_square:",
      ":white_large_square:",":white_large_square:",":white_large_square:",
    ]
    line=""
    for i in range(len(board)):
      if(i==2 or i==5 or i==8):
        line+=board[i]+" "
        await ctx.send(line)
        line=""
      else:
        line+=board[i]+" "
    
    #who starts?
    personWhoStarts=random.randint(0,1)
    
    if personWhoStarts==1:
      await ctx.send("<@"+str(player1.id)+"> is gonna start")#<@member.id>=@member
      playerNow=player1
    else:
      await ctx.send("<@"+str(player2.id)+"> is gonna start")#<@member.id>=@member
      playerNow=player2

  else:
    await ctx.send("There is a game :sleepy:")

@clientXD.command()
async def place(ctx, number:int):
  global symbol
  global playerNow
  global winning
  global gameIsRunning
  if gameIsRunning==False:
    await ctx.send("The game has finished, please start a new one :video_game:")
    return
  if playerNow==ctx.author:
    is_player_1=(playerNow==player1)
    if board[number-1]==":white_large_square:":
      if(is_player_1):      
        board[number-1]=":regional_indicator_o:"
      else:
        board[number-1]=":regional_indicator_x:"
    else:
      await ctx.send("That is not an available place, please choose a new one!!!!!!")
      return
    line=""
    for i in range(len(board)):
      if(i==2 or i==5 or i==8):
        line+=board[i]+" "
        await ctx.send(line)
        line=""
      else:
        line+=board[i]+" "

    ga=list(a if i==board[number-1] else None for a,i in enumerate(board))
    ra=list()
    for a in ga:
        if a is not None:
            ra.append(a)
    print(ra)
    for element in winning:
      if(all(a in ra for a in element)):
        await ctx.send("<@"+str(playerNow.id)+"> has won")
        gameIsRunning=False
        return 
    if is_player_1:
      await ctx.send("Now it's turn of <@"+str(player2.id)+">")
      playerNow=player2
    else:
      await ctx.send("Now it's turn of <@"+str(player1.id)+">")
      playerNow=player1
  elif ctx.author!=player1 and ctx.author!=player2:
    await ctx.send("You are not playing, fucking idiot")
  else:
    await ctx.send("Is not your turn yet")

clientXD.run("ODY4ODgzNzc4NjQ1NDE4MDM2.YP2JEw.Fxly1qTJg08l1NLU8a6swMhIbTQ")