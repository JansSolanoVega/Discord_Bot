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
        await ctx.send(f"ping {round(self.clientXD.latency*1000)} ms")

    @commands.command()
    async def predict(self,ctx):
        from SearchingFeatures import ConstruccionFeatures
        construyendo=ConstruccionFeatures("spam OR inbox",200)
        construyendo.construir()

        #Algoritmo entrenado:
        from sklearn.metrics import accuracy_score, balanced_accuracy_score
        from sklearn.metrics import classification_report
        from sklearn.metrics import confusion_matrix
        from sklearn.preprocessing import StandardScaler
        from sklearn.pipeline import make_pipeline
        from sklearn.feature_selection import SelectKBest
        from sklearn.feature_selection import chi2,f_classif
        from sklearn.svm import SVC

        import pandas as pd
        df=pd.read_csv("finalData.csv",encoding="latin-1",sep=",")
        df["target"].replace("spam",1,inplace=True)
        df["target"].replace("inbox",0,inplace=True)
        x=df.iloc[:,0:-1]
        y=df.iloc[:,-1]

        from sklearn.model_selection import train_test_split
        valid_fraction=0.2
        seed=20
        X_train, X_valid, y_train, y_valid = train_test_split(x, y, test_size=valid_fraction, random_state=seed)  

        model = make_pipeline(SelectKBest(score_func=chi2,k=20),StandardScaler(), SVC()) 
        model.fit(X_train, y_train)

        construyendo.df.drop(columns=["target"],inplace=True)

        y_predicted = model.predict(construyendo.df)
        print(y_predicted[0])
        texto="SPAM" if y_predicted==1 else "NO SPAM" 
        await ctx.send(f"El último correo recibido, que fue enviado por: **{construyendo.sender}** y con título: **{construyendo.subject}** creo que es __**{texto}**__")

      
def setup(clientXD):
    clientXD.add_cog(herramientas(clientXD))