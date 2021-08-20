import discord
from discord.ext import commands
import os
import music #importar el otro archivo music.py

intents = discord.Intents().all()                                
clientXD = commands.Bot(command_prefix = '*', intents = intents)

@clientXD.command()
async def load(ctx,extension):
    clientXD.load_extension(f"Cogs.{extension}")#carga archivos como comandos cogs o listeners
    #una extension es un archivo de python que contiene comandso o eventos
    #toda extension tiene una funcion setup que tiene como parametro el cliente, y cada que se carga entra allí
@clientXD.command()
async def unload(ctx,extension):
    clientXD.unload_extension(f"Cogs.{extension}")

Cogs=[music]

for i in range(len(Cogs)):
    Cogs[i].setup(clientXD)#llamar a la funcion del archivo
music.ga()
clientXD.run("ODY4ODgzNzc4NjQ1NDE4MDM2.YP2JEw.Fxly1qTJg08l1NLU8a6swMhIbTQ")
