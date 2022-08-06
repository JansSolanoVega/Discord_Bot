import discord
from discord.ext import commands
import os

intents = discord.Intents().all()                                
clientXD = commands.Bot(command_prefix = '*', intents = intents)

@clientXD.event
async def on_ready():
    print("Bot Messirve esta ready")

@clientXD.event
async def on_member_join(member):
    print(type(member))
    print(f"{member} ha ingresado al servidor")

@clientXD.event
async def on_member_remove(member):
    print(f"{member} ha salido del servidor")


@clientXD.command()
async def load(ctx,extension):
    clientXD.load_extension(f"Cogs.{extension}")#carga archivos como comandos cogs o listeners
    #una extension es un archivo de python que contiene comandso o eventos
    #toda extension tiene una funcion setup que tiene como parametro el cliente, y cada que se carga entra allí

@clientXD.command()
async def unload(ctx,extension):
    clientXD.unload_extension(f"Cogs.{extension}")

for filename in os.listdir(".\Cogs"):
    if filename.endswith(".py") and filename!="main2.py":
        clientXD.load_extension(f"Cogs.{filename[:-3]}")

clientXD.run("TOKEN")
