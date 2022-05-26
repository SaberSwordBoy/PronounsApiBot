import json
import discord
import requests
from discord.ext import commands

config = json.load(open("config/config.json"))["bot"]

bot = commands.Bot(command_prefix=config["prefix"])

@bot.event
async def on_ready():
    print("Ready!")
    print(f"Logged in as {bot.user.name} - {bot.user.id}")


@bot.event
async def on_connect():
    print("Connected!")


@bot.command()
async def pronoun(ctx, pronoun):
    try:
        request = requests.get(f"https://en.pronouns.page/api/pronouns/{pronoun}")
        data = request.json()
        embed = discord.Embed(title=data.get("description"), color=discord.Color.magenta())

        morphs = data.get("morphemes")
        asd = ""
        for k, v in morphs.items():
            asd += f"{k} - {v}\n"

        embed.add_field(name="Morphemes", value=asd)
        embed.add_field(name="Plural", value=data.get("plural")[0])
        embed.add_field(name="Aliases", value=data.get("aliases"))

        embed.set_image(url=f"https://en.pronouns.page/api/banner/{data.get('canonicalName')}.png")

        await ctx.send(embed=embed)

    except Exception as Error:
        await ctx.send(f"Sorry, there was an error processsing your command.\n{Error}")


@bot.command(aliases=["try"])
async def tryout(ctx, pronoun):
    try:
        request = requests.get(f"https://en.pronouns.page/api/pronouns/{pronoun}")
        data = request.json()
        embed = discord.Embed(title=data.get("description"), color=discord.Color.magenta())

        examples = ""

        ex = data.get("examples")
        for e in ex:
            examples += f"{e}\n"
        embed.description = examples

        await ctx.send(embed=embed)


    except Exception as Error:
        await ctx.send(f"Sorry, there was an error processsing your command.\n{Error}")

@bot.command()
async def profile(ctx, username):
    try:
        request = requests.get(f"https://en.pronouns.page/api/profile/get/{username}")
        data = request.json()

        embed = discord.Embed(
            title=data.get("username"), 
            color=discord.Color.blurple())

        embed.description = data.get("profiles")["en"]["description"]

        embed.add_field(name="Pronouns", value=data.get("profiles")["en"]["pronouns"])

        embed.add_field(name="Names", value=data.get("profiles")["en"]["names"])

        embed.set_thumbnail(url=data.get("avatar"))
        embed.set_author(
            name=data.get("username").title(),
            url=f"https://en.pronouns.page/@{data.get('username')}",
            icon_url=data.get('avatar'))
        await ctx.send(embed=embed)


    except Exception as Error:
        await ctx.send(f"Sorry, there was an error processsing your command.\n{Error}")


bot.run(config["token"])