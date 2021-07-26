import discord
from discord.ext import commands
import random
import requests
import json
intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True)
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
async def hello(ctx,arg1,arg2):
  await ctx.send('raaaa!!!!!!!!!!!')

@clientXD.command()
async def helloxd(ctx,*args):
  for arg in args:
    await ctx.send("arg"+str(args.index(arg)+1)+": "+str(arg))

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
    await ctx.send(f"pong {round(clientXD.latency*1000)} ms")

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

clientXD.run("ODY4ODgzNzc4NjQ1NDE4MDM2.YP2JEw.Fxly1qTJg08l1NLU8a6swMhIbTQ")

