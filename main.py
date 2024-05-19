import discord
import random
from discord import app_commands
from discord.ext import commands
from git import Repo
from config import data

bot = commands.Bot(command_prefix = "?", intents = discord.Intents.all())

async def sender(ctx, member: discord.Member):
    server_name = member.guild.name
    avatar = member.avatar.url
    description = "Welcome to Vertic's Client discord! Check out #rules and dont be a retard."
    embed = discord.Embed(color=0x00ffe0)
    embed.set_author(name=f"Welcome to {server_name}, {member.name}!", icon_url=avatar)
    embed.add_field(name="", value=description, inline=False)
    embed.set_image(url="https://media.giphy.com/media/OYwYE7UtTTqLBfpBS8/giphy.gif")
    channel2 = ctx.guild.get_channel(1241375154559389788)
    await channel2.send(embed=embed)

@bot.event
async def on_member_join(member: discord.Member):
    await sender(member,member)

@bot.hybrid_command(description="Generate Client key")
async def gen(ctx: commands.Context):
    role = discord.utils.get(ctx.guild.roles, name="Owner")
    if role not in ctx.author.roles:
        await ctx.send("You cannot generate keys!")
        return
    
    client_prefix = "vertic-"
    random_suffix = ''.join(random.choices('abcdefghiojshyen0123456789', k=20))
    custom_key = client_prefix + random_suffix
    with open("keys.txt", "a+") as f:
        f.write(custom_key + "\n")
    await ctx.send(f"Check your dms!")
    await ctx.author.send(f"Successfully generated a client key! : {custom_key}")



@bot.hybrid_command(description="Request a change for your HWID!")
async def hwidrequest(ctx: commands.Context, hwid: str, reason: str):
    role = discord.utils.get(ctx.guild.roles, name="vertic")
    channel = bot.get_channel(1240965482115498005)
    embed = discord.Embed()
    if role is None or role not in ctx.author.roles:
        await ctx.send("You do not own Vertic Client!")
        return
    
    await ctx.send("Check your dms!")
    await ctx.author.send("Your HWID request has been made!")
    embed.add_field(name="HWID Request", value=f"{ctx.author.id} has requested to change their HWID to {hwid}",inline=False)
    embed.add_field(name="Reason:",value=f"{reason}",inline=False)
    await channel.send(embed=embed)

import discord
from discord.ext import commands
from git import Repo

import discord
from discord.ext import commands
from git import Repo

local_repo_path = "https://github.com/RandomVapeUser/Vector-Client-HWIDS"
hwid_file_path = f"{local_repo_path}/HWIDS.txt"
repo_url = "https://github.com/RandomVapeUser/Vector-Client-HWIDS.git"
commit_message = "HWID's updated nigga"

@bot.hybrid_command(description="Set a user's HWID")
async def sethwid(ctx: commands.Context, user: discord.Member, hwid: str):
    channel = bot.get_channel(1240965482115498005)
    hwid_found = False
    role = discord.utils.get(ctx.guild.roles, name="vertic")
    if role not in user.roles:
        await ctx.send("That user does not own Vertic!")
        return
    
    with open(hwid_file_path, "a+") as f:
        lines = f.readlines()
        f.seek(0)
        for line in lines:
            user_id, stored_hwid = line.strip().split(" ")
            if str(user.id) == user_id:
                f.write(f"{user_id} {hwid}\n")
                hwid_found = True
            else:
                f.write(line)
        if not hwid_found:
            f.write(f"{user.id} {hwid}\n")
        f.truncate()
    
    try:
        repo = Repo(local_repo_path)
    except Exception as e:
        repo = Repo.clone_from(repo_url, local_repo_path)

    repo.index.add([hwid_file_path])
    repo.index.commit(commit_message)
    origin = repo.remote(name='origin')
    origin.push()

    await ctx.send("Updated HWID in github LES GO!")

@bot.hybrid_command(description="Nuke a channel")
async def nuke(ctx: commands.Context, channel: discord.TextChannel):
    role = discord.utils.get(ctx.guild.roles, name="Owner")
    if role not in ctx.author.roles:
        await ctx.send("You cannot nuke channels!")
        return

    nuke_channel = discord.utils.get(ctx.guild.channels, name=channel.name)

    if nuke_channel is not None:
        new_channel = await nuke_channel.clone()
        await nuke_channel.delete()
        await new_channel.send(f"`Nuked by {ctx.author.mention}`")

    else:
        await ctx.send(f"No channel named {channel.name} was found!")
            
@bot.hybrid_command(description="Redeem a client key!")
async def redeem(ctx: commands.Context, key: str):
    vertic_role = discord.utils.get(ctx.guild.roles, name="vertic")
    if vertic_role in ctx.author.roles:
        await ctx.send("You already own vertic!")
        return
    
    with open("keys.txt", "r+") as f:
        channel = bot.get_channel(1240965482115498005)
        lines = f.readlines()
        f.seek(0) 
        for line in lines:
            if line.strip() == key: 
                await ctx.send(f"Redeemed key successfully!")
                await ctx.author.add_roles(vertic_role)
                await channel.send(f"{ctx.author.id} has redeemed key `{key}`")
                f.truncate()
                return
            else:
                f.write(line)
        f.truncate()  
    await ctx.send("Key not found.")

@bot.hybrid_command(description="Sync Commands")
async def sync(ctx: commands.Context):
    await bot.tree.sync(guild=ctx.guild)
    await ctx.send("Synced!")

@bot.event
async def on_ready():
    await bot.tree.sync()
    print("Synced!")

bot.run(data["token"])