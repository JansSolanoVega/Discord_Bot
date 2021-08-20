import discord
from discord.ext import commands
from discord.ext.commands.core import check
import youtube_dl
from urllib import parse,request
import re

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
YDL_OPTIONS = {'format': 'bestaudio/best', 'noplaylist':'True'}


class musica(commands.Cog):#inherit class commands.Cog para la carga
    #constructor to run in the setup
    def __init__(self,clientXD):
        self.clientXD=clientXD
        self.queue=[]

    def check_queue(self,ctx):
        if len(self.queue)!=0:
            voiceBOT=ctx.voice_client
            source=self.queue.pop(0)
            voiceBOT.play(source)

    #REGEX-SEARCH TEXT, CONVERT TO URL
    def convert_to_url(self,url):
        if not url.startswith("https:"):
            busqueda_link=parse.urlencode({"search_query":url})
            htmlContent=request.urlopen("https://www.youtube.com/results?"+busqueda_link)
            search_results=re.findall('\"/watch\\?v=(.{11})',str(htmlContent.read().decode()))#regex \\?: search a ?---(.{11})obtener como resultado esos 11 caracteres
            #\": search for a "
            url="https://www.youtube.com/watch?v="+search_results[0]
        return url
    #events
    @commands.command()
    async def join(self,ctx):
        print(ctx.message.guild.id)
        if ctx.author.voice is None:
            await ctx.send("You are not in a voice channel")
            return
        channel=ctx.author.voice.channel
        if ctx.voice_client is None:#el bot no esta conectado a ningun canal
            await channel.connect()
        else:
            await ctx.voice_client.move_to(channel) 
    
    @commands.command()
    async def leave(self,ctx):
        voice_client = ctx.voice_client

        if voice_client is not None:
            await voice_client.disconnect()
        else:
            await ctx.send("The bot is not connected to a voice channel.")

    @commands.command(aliases=["q"])
    async def queue(self,ctx,*,song,aliases=["q"]):
        await ctx.send("🔎 **Searching** :clock:")
        url=self.convert_to_url(song)
        voiceBOT=ctx.voice_client
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url,download=False)
            url2=info['formats'][0]['url']
            nameSong=info['title']
            source=await discord.FFmpegOpusAudio.from_probe(url2,**FFMPEG_OPTIONS)#** is to show that is a dictionaro
            self.queue.append(source)
            await ctx.send(f"**Añadido a la cola**: {nameSong}")
            print(self.queue)
        

    @commands.command(aliases=["p"])
    async def play(self,ctx,*,url:str):
        
        await ctx.send("🔎 **Searching** :clock:")
        url=self.convert_to_url(url)
        
        voiceBOT=ctx.voice_client
        voiceBOT.stop()#stop the bot voice
        
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
            voiceBOT.play(source,after=lambda x: self.check_queue(ctx))
            
            await ctx.send("**Now playing: **"+str(nameSong))
        
        guild_id=ctx.guild.id
        print(guild_id)

    @commands.command(aliases=["s"])
    async def pause(self,ctx):
        voiceBOT=ctx.voice_client
        if voiceBOT.is_playing():
            voiceBOT.pause()
            await ctx.send("**Paused** ⏸️")
        else:
            await ctx.send("Voice is not playing anything")

    @commands.command(aliases=["r"])
    async def resume(self,ctx):
        voiceBOT=ctx.voice_client
        if voiceBOT.is_paused():
            voiceBOT.resume()
            await ctx.send("**Playing** ▶️")
        else:
            await ctx.send("Voice is not paused")
    
def setup(clientXD):
    clientXD.add_cog(musica(clientXD))#añadir un objeto(cog) que tiene como cliente a client

