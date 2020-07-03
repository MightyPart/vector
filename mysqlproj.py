import mysql.connector

import discord
from discord.utils import get
from discord.ext import commands

bottomtext = "website coming soon"

mydb = mysql.connector.connect(
  host="192.168.241.1",
  port="3306",
  user="Cameron",
  password="322005bday",
  database="mydatabase"
)

mycursor = mydb.cursor()

TOKEN = ('NzI4MjI5OTEwMzEyNjQ4NzY0.Xv8sLA.n8Vfefvx0Xo4MyoHVoceySv570s')

client = commands.Bot(command_prefix='.')

@client.event
async def on_member_join(member):
    sql = "INSERT INTO cointable (UserID, VectorCoins) VALUES (%s, %s)"
    val = (str(member.id), "0")
    mycursor.execute(sql, val)

    mydb.commit()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Many Servers!"))



@client.command()
async def vectorcoins(ctx):
    sql = "SELECT * FROM cointable WHERE UserID ="+str(ctx.author.id)

    mycursor.execute(sql)

    myresult = mycursor.fetchall()

    for row in myresult:
        embed = discord.Embed(title=(str(ctx.author)+"'s Vector Coins"),color=11259375)
        embed.add_field(name=row[1]+" 💰", value=bottomtext)
        await ctx.channel.send(f"{ctx.author.mention}", embed=embed)
        break

@client.command()
async def setup(ctx):
    for member in ctx.author.guild.members:
        if str(member.id) != "728229910312648764": 
            mycursor.execute("SELECT UserID FROM cointable")

            myresult = mycursor.fetchall()
    
            for x in myresult:
                y = str(x)
                y = y.replace('(', '')
                y = y.replace(')', '')
                y = y.replace(',', '')
                y = y.replace("'", '')
                if str(member.id) == str(y):
                    action = True
                    break
                else:
                    action = False

            if action == True:
                print(str(member)+" is in table")
            else:
                print(str(member)+" is not in table")
                
                sql = "INSERT INTO cointable (UserID, VectorCoins) VALUES (%s, %s)"
                val = (str(member.id), "0")
                mycursor.execute(sql, val)

                mydb.commit()
                
                    

@client.command()
async def addme(ctx):
    sql = "INSERT INTO cointable (UserID, VectorCoins) VALUES (%s, %s)"
    val = (str(ctx.author.id), "0")
    mycursor.execute(sql, val)

    mydb.commit()


@client.command()
async def addcoins(ctx,*,args):
    sql = "SELECT VectorCoins FROM cointable WHERE UserId ="+str(ctx.author.id)

    mycursor.execute(sql)

    myresult = mycursor.fetchall()

    for x in myresult:
        y = str(x)
        y = y.replace('(', '')
        y = y.replace(')', '')
        y = y.replace(',', '')
        y = y.replace("'", '')

    newcoins = int(y)+int(args)
    sql = "UPDATE cointable SET VectorCoins = "+str(newcoins)+" WHERE UserId ="+str(ctx.author.id)

    mycursor.execute(sql)

    mydb.commit()

client.run(TOKEN)


