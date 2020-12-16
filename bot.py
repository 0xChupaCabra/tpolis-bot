import urllib3
import discord
from discord.ext import commands
import asyncio
import json
import mysql.connector
import requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

mydb = mysql.connector.connect(
    host="localhost",
    user="stepollo",
    passwd="root",
    database="tpolis",
    autocommit=True
)

mycursor = mydb.cursor()
bot = commands.Bot(command_prefix='!')

amount2= "500"

@bot.command()
async def tpolis(ctx, arg1):
    
    discord_id = ctx.message.author.id
    mycursor.execute("SELECT * FROM tpolis WHERE discord_id = '%s'"%(discord_id))
    spam = mycursor.fetchall()

    if not spam:
        try:
            data = '{"name":"stepollo","password":"stepollo"}'

            response = requests.post('https://localhost:8081/wallet/open', data=data, verify=False)
            r = response.json()
            print(r)
        #print(r.keys())

            account = str(arg1)
            data_2 = '{"account":"'+account+'","amount":"'+amount2+'"}'
            send_tpolis = requests.post('https://localhost:8081/wallet/sendtransaction', data=data_2, verify=False)
            r2 = send_tpolis.json()

            embed = discord.Embed(title="Testnet Faucet", description=f'{ctx.message.author.mention} 500 tPOLIS have been sent to your wallet', color=0xf54242)
            embed.add_field(name="TXID", value=r2['hash'])
            await ctx.send(embed=embed)
            sql_balance_update2 = "INSERT INTO tpolis (discord_id, time) VALUES ('%s', CURRENT_TIMESTAMP())"%(str(discord_id))
            mycursor.execute(sql_balance_update2)
        except:
            embed = discord.Embed(title="Testnet Faucet", description=f'{ctx.message.author.mention}, error. Please check your address', color=0xf54242)
            embed.add_field(name="TXID", value='null')
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Testnet Faucet", description=f'{ctx.message.author.mention}, you can claim tPOLIS once per day', color=0xf54242)
        embed.add_field(name="TXID", value='null')
        await ctx.send(embed=embed)
bot.run('token') 
