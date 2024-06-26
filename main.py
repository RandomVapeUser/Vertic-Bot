import discord
import random
from discord import app_commands
from discord.ext import commands
import logging
from config import data
from datetime import datetime
import asyncio
import json
import os

bot = commands.Bot(command_prefix = "?", intents = discord.Intents.all())

logging.basicConfig(level=logging.INFO)

log_channel = bot.get_channel(1242721581042765927)
datetime_now = datetime.now()
file_path = 'hwids.json'

if not os.path.exists(file_path):
    with open(file_path, 'w') as file:
        json.dump({}, file)

def load_hwids_info():
    with open(file_path, 'r') as file:
        return json.load(file)

def save_hwids_info(hwids_info):
    with open(file_path, 'w') as file:
        json.dump(hwids_info, file, indent=4)

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
    global datetime_now
    global log_channel
    role = discord.utils.get(ctx.guild.roles, name="Owner")
    if role not in ctx.author.roles:
        await ctx.send("You cannot generate keys!")
        return
    
    client_prefix = "vertic-"
    random_suffix = ''.join(random.choices('abcdefghiojshyen0123456789', k=20))
    custom_key = client_prefix + random_suffix
    with open("keys.txt", "a+") as f:
        f.write(custom_key + "\n")
    
    key_embed = discord.Embed()
    key_embed.add_field(name="Key Generated!", value=f"```{custom_key}```")

    log_embed = discord.Embed(title="Key logged!")
    log_embed.add_field(name="",value=f"{ctx.author.name} has generated a key!")
    log_embed.set_footer(text=f"Time: {datetime_now}")

    await ctx.send(f"Check your dms!")
    await ctx.author.send(embed=key_embed)
    await log_channel.send(embed=log_embed)

@bot.hybrid_command(description="Delete a number of messages in a channel!")
async def purge(ctx: commands.Context, number: int):
    global datetime_now
    if ctx.author.guild_permissions.manage_messages != True:
        await ctx.send("You cannot purge messages!")
        return
    
    await ctx.reply(f"Purging {number} messages.")
    await asyncio.sleep(2)
    await ctx.channel.purge(limit=number+1)

@bot.hybrid_command(description="Log a users hwid into the database!")
async def loghwid(ctx: commands.Context,user: discord.Member, hwid: str):
    role = discord.utils.get(ctx.guild.roles, name="Owner")
    vertic_role = discord.utils.get(ctx.guild.roles, name="vertic")
    if role is None or role not in ctx.author.roles:
        await ctx.send("This command is only availabe for owners!")
        return
    
    if vertic_role not in user.roles:
        await ctx.send("That user does not own Vertic!")
        return
    hwids_info = load_hwids_info()
    
    hwids_info[user.name] = {
        "user_id": user.id,
        "user_hwid": hwid
    }

    save_hwids_info(hwids_info)
    await ctx.send(f"{user.name}'s HWID has been updated!")

@bot.hybrid_command(description="Request a change for your HWID!")
async def hwidrequest(ctx: commands.Context, hwid: str, reason: str):
    global datetime_now
    global log_channel
    role = discord.utils.get(ctx.guild.roles, name="vertic")
    if role is None or role not in ctx.author.roles:
        await ctx.send("You do not own Vertic Client!")
        return

    request_channel = bot.get_channel(1240965482115498005)

    hwid_embed = discord.Embed(title="Hwid Request 📩")
    hwid_embed.add_field(name="Made by:", value=f"`{ctx.author.name} ({ctx.author.id})`",inline=False)
    hwid_embed.add_field(name="HWID: ", value=f"`{hwid}`",inline=False)
    hwid_embed.add_field(name="Reason:",value=f"`{reason}`",inline=False)
    hwid_embed.set_footer(text="Coded by Sal")

    user_embed = discord.Embed(title="Hwid Request Sent!")
    user_embed.add_field(name="",value="Your Hwid request has been sent, please wait until our staff reviews it!")
    user_embed.set_footer(text="⚠️ Spamming or messing with this command can result in a mute")

    log_embed = discord.Embed(title="Hwid Request Logged!")
    log_embed.add_field(name=f"Request made by {ctx.author.name}",value="")
    log_embed.set_author(name=f"{ctx.author.name}", icon_url=ctx.author.avatar)
    log_embed.set_footer(text=f"Time: {datetime_now}")
    
    await ctx.send("Check your dms!")
    await ctx.author.send(embed=user_embed)
    await request_channel.send(embed=hwid_embed)
    await log_channel.send(embed=log_embed)
        
@bot.hybrid_command(description="Nuke a channel")
async def nuke(ctx: commands.Context, channel: discord.TextChannel):
    global datetime_now
    global log_channel
    role = discord.utils.get(ctx.guild.roles, name="Owner")
    if role not in ctx.author.roles:
        await ctx.send("You cannot nuke channels!")
        return

    nuke_channel = discord.utils.get(ctx.guild.channels, name=channel.name)

    log_embed = discord.Embed(title="Channel nuke logged!")
    log_embed.add_field(name="",value=f"{channel.name} has been nuked by {ctx.author.name}")
    log_embed.set_footer(text=f"Time: {datetime_now}")

    new_channel = await nuke_channel.clone()
    await nuke_channel.delete()
    await new_channel.send(f"`Nuked by {ctx.author.name}`")
    await log_channel.send(embed=log_embed)

@bot.hybrid_command(description="Redeem a client key!")
async def redeem(ctx: commands.Context, key: str):
    global datetime_now
    global log_channel
    vertic_role = discord.utils.get(ctx.guild.roles, name="vertic")
    if vertic_role in ctx.author.roles:
        await ctx.send("You already own vertic!")
        return
    
    log_embed = discord.Embed(title="Key redeemed!")
    log_embed.add_field(name="",value=f"{ctx.author.name} has reedemed vertic client!")
    log_embed.add_field(name="Key: ",value=f"`{key}`",inline=False)
    log_embed.set_footer(text=f"Time: {datetime_now}")

    with open("keys.txt", "r+") as f:
        channel = bot.get_channel(1240965482115498005)
        lines = f.readlines()
        f.seek(0) 
        for line in lines:
            if line.strip() == key: 
                await ctx.send(f"Redeemed key successfully!")
                await ctx.author.add_roles(vertic_role)
                await channel.send(f"{ctx.author.id} has redeemed key `{key}`")
                await log_channel.send(embed=log_embed)
                f.truncate()
                return
            else:
                f.write(line)
        f.truncate()

    await ctx.send("Key not found.")

@bot.hybrid_command(description="Dev information about users!")
async def userinfo(ctx : commands.Context, user: discord.Member):
    if ctx.author.id not in data["devs"]:
        await ctx.send("This command is only available for devs!")
        return
    
    vertic_role = discord.utils.get(ctx.guild.roles, name="vertic")
    hwids_info = load_hwids_info()


    if user.name in hwids_info:
        user_data = hwids_info[user.name]
        hwid = user_data["user_hwid"]
        user_id = user_data["user_id"]

        has_client = discord.Embed(title=f"Client Info for {user.name}",description="Overall description about user stats!")
        has_client.add_field(name=f"\{user.name}'s ID:", value=f"`{user.id}`")
        has_client.add_field(name="\Client Ownership: ", value="This user owns Vertic!")
        has_client.add_field(name="\Hwid: ", value=f"{hwid}")
        await ctx.author.send(embed=has_client)

    else:
        if vertic_role in user.roles:
            client = discord.Embed(title=f"Client Info for {user.name}",description="Overall description about user stats!")
            client.add_field(name=f"\{user.name}'s ID:", value=f"`{user.id}`")
            client.add_field(name="\Client Ownership: ", value="This user owns Vertic!")
            client.add_field(name="\Hwid: ", value="This users hwid has not been logged yet ⚠️")
            await ctx.author.send(embed=client)
        else:
            no_client = discord.Embed(title=f"Client Info for {user.name}",description="Overall description about user stats")
            no_client.add_field(name=f"\{user.name}'s ID:", value=f"`{user.id}`")
            no_client.add_field(name="\Client Ownership: ", value="The user does not own Vertic.")
            no_client.add_field(name="\Hwid: ", value="None")
            await ctx.author.send(embed=no_client)

@bot.hybrid_command(description="Sync Commands")
async def sync(ctx: commands.Context):
    await bot.tree.sync(guild=ctx.guild)
    await ctx.send("Synced!")

@bot.event
async def on_ready():
    await bot.tree.sync()
    print("Synced!")

bot.run(data["token"])