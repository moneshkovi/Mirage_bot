from __future__ import annotations
from asyncio import sleep as asyncsleep
from base.utilities import utilities
from discord.ext import commands
from random import randint 
from io import BytesIO
from discord import File as dFile
from discord import Member as dMember
import aiohttp
import discord
import re
class Leveling(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.db = utilities.database(self.bot.loop, self.bot.cfg.postgresql_user, self.bot.cfg.postgresql_password)
        self.brake = []
    @commands.Cog.listener()
    async def on_message(self, message) -> None:
        if message.author == self.bot:
            return
        if message.author.id == 758292526486126632:
            return
        result = await self.db.fetch(f'SELECT rank, xp FROM users WHERE id=\'{message.author.id}\'')
        Enthusiast = discord.utils.get(message.guild.roles, name = "Enthusiast")
        Rookie = discord.utils.get(message.guild.roles, name = "Rookie")
        Veterain = discord.utils.get(message.guild.roles, name = "Veterain")
        Elite = discord.utils.get(message.guild.roles, name = "Elite")
        Pro = discord.utils.get(message.guild.roles, name = "Pro")
        Master = discord.utils.get(message.guild.roles, name = "Master")
        Legendary = discord.utils.get(message.guild.roles, name = "Legendary")
        Mythical = discord.utils.get(message.guild.roles, name="Mythical")
        if result[0][0] >= 5 and Enthusiast not in message.author.roles:
            await message.author.add_roles(Enthusiast)    
            await message.channel.send(f"{message.author.mention} has been promoted to Enthusiast")
        elif result[0][0] >=15 and Rookie not in message.author.roles:
            await message.author.add_roles(Rookie)
            await message.channel.send(f"{message.author.mention} has been promoted to Rookie")
        elif result[0][0] >=25 and Veterain not in message.author.roles:
            await message.author.add_roles(Veterain)
            await message.channel.send(f"{message.author.mention} has been promoted to Veterain")
        elif result[0][0] >=35 and Elite not in message.author.roles:
            await message.author.add_roles(Elite)
            await message.channel.send(f"{message.author.mention} has been promoted to Elite")
        elif result[0][0] >=50 and Pro not in message.author.roles:
            await message.author.add_roles(Pro)
            await message.channel.send(f"{message.author.mention} has been promoted to Pro")
        elif result[0][0] >=65 and Master not in message.author.roles:
            await message.author.add_roles(Master)
            await message.channel.send(f"{message.author.mention} has been promoted to Master")
        elif result[0][0] >=75 and Legendary not in message.author.roles:
            await message.author.add_roles(Legendary)
            await message.channel.send(f"{message.author.mention} has been promoted to Legendary")
        elif result[0][0] >=85 and Mythical not in message.author.roles:
            await message.author.add_roles(Mythical)
            await message.channel.send(f"{message.author.mention} has been promoted to Mythical")

        if message.author.id not in self.brake:
            if not await self.db.fetch(f'SELECT * FROM users WHERE id=\'{message.author.id}\''):
                await self.db.fetch(f'INSERT INTO users (id, rank, xp) VALUES (\'{message.author.id}\', \'0\', \'0\')')
                current_xp = 0

            else:
                result = await self.db.fetch(f'SELECT rank, xp FROM users WHERE id=\'{message.author.id}\'')
                current_xp = result[0][1] + randint(self.bot.cfg.min_message_xp, self.bot.cfg.max_message_xp)

                if current_xp >= utilities.rankcard.neededxp(result[0][0]):
                    await self.db.fetch(f'UPDATE users SET rank=\'{result[0][0]+1}\', xp=\'0\' WHERE id=\'{message.author.id}\'')
                else:
                    await self.db.fetch(f'UPDATE users SET xp=\'{current_xp}\' WHERE id=\'{message.author.id}\'')
                self.brake.append(message.author.id)
                await asyncsleep(randint(15, 25))
                self.brake.remove(message.author.id)
    @commands.Cog.listener()
    async def on_member_join(self, member):
        embed=discord.Embed(title=f"Hey {member.name}, Welcome to Call of Duty: Mobile!", description="""Make sure you go through #🎄-information-desk and have a read through all the rules and follow them to avoid any infractions.\n
Call of Duty: Mobile is a free-to-play first-person shooter game developed by TiMi Studios and published by Activision. Being developed for mobile platform, this game brings together the maps, weapons and characters from across the Call of Duty series in the definitive first-person action experience on mobile.\n
As of right now, we are gathering information regarding the overall player experience to help make changes and improvements for the same. Please do fill up this survey form to help make the game better for our audience.\n
This server is a community-run server, owned by TiMi Studios and supported by Activision, so feel free to address and express your concerns for the game to help improve it or just to have a wonderful time!\n
So, what are you waiting for? See ya in the Battlefield!\n """, color=0x00ff00)
        file = discord.File("c.jpg", filename="image.jpg")
        embed.set_image(url="attachment://image.jpg")
        await member.send(file=file, embed=embed)

    @commands.command()
    async def help(self, ctx) -> None:
        embed=discord.Embed(title=f"Hey {ctx.author.name}, Here are the commands", description="""Leveling Commands
**\n.rank**
Displays your current level with an intuitive layout.
Aliases: **.rank** \n\n**.leaderboard**
Displays the top 10 most active users in the server!
Aliases: **.lb**\n \n**.color**
Set a color of your own to be displayed with your rank card.
Aliases: **.color**\n """, color=0x00ff00)
        await ctx.send(embed=embed)

    @commands.command()
    async def lb(self, ctx) -> None:
        result = await self.db.fetch(f'SELECT id, rank, xp FROM users ORDER BY rank desc LIMIT 10 ')
        for i in result:
            if i[0] == 741306813965795430:
                result.remove(i)

        embed=discord.Embed(title=f"leaderboard",  color=0x00ff00)
        counter = 1
        for i in result:
            try:
                user = await ctx.guild.fetch_member(i[0])
                if user != None:
                    embed.add_field(name=str(counter)+"-"+user.name, value="🌟 Level : "+str(i[1])+"\n"+"EXP: "+str(i[2])+"/"+str(i[2]*80+100), inline=False)
                    counter += 1
            except:
                continue
        await ctx.send(embed=embed)
    @commands.command()
    async def rank(self, ctx, member: dMember=None) -> None:
        if member:
            uMember = member
        else:
            uMember = ctx.author
        result = await self.db.fetch(f'SELECT rank, xp FROM users WHERE id=\'{uMember.id}\'')
        if result:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'{uMember.avatar_url}?size=128') as resp:
                    profile_bytes = await resp.read()

            buffer = utilities.rankcard.draw(str(uMember), result[0][0], result[0][1], BytesIO(profile_bytes))

            await ctx.send(file=dFile(fp=buffer, filename='rank_card.png'))
        else:
            await ctx.send(f'{uMember.mention}, you don\'t received xp yet.')


def setup(bot) -> None:
    bot.add_cog(Leveling(bot))
"""**.background**\n
Choose a custom background from the gallery of images available for your rank card!
Aliases: **.bg, .setbg**"""
