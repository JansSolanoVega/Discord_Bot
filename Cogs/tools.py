from asyncio import events
import discord
from discord.ext import commands
import requests
import json
import random 

sadWords=["sad","depressed","unhappy","suffering"]
MotivationalMessages=["everything will be ok","thats fine","you're a great bot"]

def getQuote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data=json.loads(response.text)
  cita=json_data[0]["q"]+" -Author: "+json_data[0]["a"]
  return cita

class herramientas(commands.Cog):
    def __init__(self,clientXD):
        self.clientXD=clientXD
    '''
    @commands.Cog.listener()
    async def on_message(self,message):
        if message.author==self.clientXD.user:
            return
        mensaje=message.content

        if mensaje.startswith("ga"):
            await message.channel.send("u're a fucking idiot")
        if "quote" in mensaje:
            await message.channel.send(getQuote())
        if any(i in mensaje for i in sadWords):
            await message.channel.send(random.choice(MotivationalMessages))
        await self.clientXD.process_commands(message)
    '''
    @commands.command()
    async def clear(cx,amount=2):
        await cx.channel.purge(limit=amount)

    @commands.command(aliases=["8ball","test"])
    async def _8ball(self,ctx,*,question):
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
    
    @commands.command()
    async def ping(self,ctx):
        await ctx.send(f"pong {round(self.clientXD.latency*1000)} ms")



def setup(clientXD):
    clientXD.add_cog(herramientas(clientXD))