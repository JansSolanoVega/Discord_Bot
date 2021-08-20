import discord
from discord.ext import commands
import random
WINNING_STRATEGY=[
  [0,1,2],
  [3,4,5],
  [6,7,8],
  [0,3,6],
  [1,4,7],
  [2,5,8],
  [0,4,8],
  [2,4,6],
]
class juegos(commands.Cog):
    def __init__(self,clientXD):
        self.clientXD=clientXD
        self.gameIsRunning=False
        self.finish=False

    async def printBoard(self,ctx):
        line=""
        for i in range(len(self.board)):
            if(i==2 or i==5 or i==8):
                line+=self.board[i]+" "
                await ctx.send(line)
                line=""
            else:
                line+=self.board[i]+" "

    @commands.command()
    async def tictactoe(self,ctx, player1XD : discord.Member, player2XD : discord.Member):
        if not self.gameIsRunning:
            self.finish=0
            self.player1=player1XD
            self.player2=player2XD
            self.gameIsRunning=True
            
            self.board=[
            ":white_large_square:",":white_large_square:",":white_large_square:",
            ":white_large_square:",":white_large_square:",":white_large_square:",
            ":white_large_square:",":white_large_square:",":white_large_square:",
            ]
            
            #Printing the board
            await self.printBoard(ctx)#esperar hasta que imprima
            

            #who starts?
            personWhoStarts=random.randint(0,1)
            
            if personWhoStarts==1:
                await ctx.send("<@"+str(self.player1.id)+"> is gonna start")#<@member.id>=@member
                self.playerNow=self.player1
            else:
                await ctx.send("<@"+str(self.player2.id)+"> is gonna start")#<@member.id>=@member
                self.playerNow=self.player2

        else:
            await ctx.send("There is a game in play :video_game:")

    @commands.command()
    async def place(self,ctx, number:int):
        global WINNING_STRATEGY
        if self.gameIsRunning==False:
            await ctx.send("The game has finished, please start a new one :video_game:")
            return
        if self.playerNow==ctx.author:#si es el turno de quien envio
            #placing the mark
            if self.board[number-1]==":white_large_square:":
                if(self.playerNow==self.player1):      
                    self.board[number-1]=":regional_indicator_o:"
                else:
                    self.board[number-1]=":regional_indicator_x:"
            else:
                await ctx.send("That is not an available place, please choose a new one!!!!!!")
                return

            #printing the board
            await self.printBoard(ctx)

            #Check if is the winner
            ga=list(a if i==self.board[number-1] else None for a,i in enumerate(self.board))
            ra=list()
            for a in ga:
                if a is not None:
                    ra.append(a)
            print(ra)
            for element in WINNING_STRATEGY:
                if(all(a in ra for a in element)):
                    await ctx.send("<@"+str(self.playerNow.id)+"> has won "+":trophy:"+" "+":trophy:"+" "+":trophy:"+" ")
                    self.gameIsRunning=False
                    return 

            #Next turn
            if self.playerNow==self.player1:
                await ctx.send("Now it's turn of <@"+str(self.player2.id)+">")
                self.playerNow=self.player2
            else:
                await ctx.send("Now it's turn of <@"+str(self.player1.id)+">")
                self.playerNow=self.player1

        elif ctx.author!=self.player1 and ctx.author!=self.player2:
            await ctx.send("You are not playing, fucking idiot")
        else:
            await ctx.send("Is not your turn yet")


def setup(clientXD):
    clientXD.add_cog(juegos(clientXD))