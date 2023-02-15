import SniperPackage.Sniper
import discord
from discord import app_commands
import time

watchdog = SniperPackage.Sniper.watchdog()
auth = SniperPackage.Sniper.credentials()

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

guild_object = discord.Object(id=1067257535549157427)
token = open('dog_bot_token.txt', 'r').read()

@tree.command(name = "ping", description = "Poke the Shiba", guild=guild_object)
async def ping_command(interaction):
    message = f"\U0001f415 Sat in {int((time.time() - interaction.created_at.timestamp()) * 1000)} ms"
    await interaction.response.send_message(message, ephemeral=True)

@tree.command(name = "add", description = "Add username to droptime watchdog", guild=guild_object)
async def add_command(interaction, username: str):
    if watchdog.Watch(username):
        message = f'``{username}`` is already being watched'
    else: 
        message = f'Added ``{username}`` to ``WatchDog``'

    await interaction.response.send_message(message, ephemeral=True)

@tree.command(name = "remove", description = "Remove username from watchdog", guild=guild_object)
async def remove_command(interaction, username: str):
    if watchdog.Ignore(username):
        message = f'``{username}`` is not watched``'
    else: 
        message = f'Removed ``{username}`` from ``WatchDog``'

    await interaction.response.send_message(message, ephemeral=True)

@client.event
async def on_ready():
    await tree.sync(guild=guild_object)
    await client.change_presence(status=discord.Status.online, activity=discord.Streaming(name='API requests.', platform='Twitch', url='https://www.twitch.tv/directory'))
    print("Ready!")

client.run(token)