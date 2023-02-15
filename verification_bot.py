import discord
from discord import app_commands
from captcha.image import ImageCaptcha
import random
import string

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
captchaImage = ImageCaptcha(fonts=['/home/ec2-user/fonts/Raleway.ttf', '/home/ec2-user/fonts/OpenSans.ttf'])
token = open('verification_bot_token.txt', 'r').read()

captchaList = {}

def __generate_captcha(user_id):
    captchaKey = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
    captchaData = captchaImage.generate(captchaKey)
    captchaImage.write(captchaKey, '/home/ec2-user/captcha.png')
    captchaList[user_id] = captchaKey

    return captchaData

@tree.command(name="verify", description="Human verification", guild=discord.Object(id=1067257535549157427))
async def verify_command(interaction):
    captchaData = __generate_captcha(interaction.user.id)

    captchaFile = discord.File(filename='/home/ec2-user/captcha.png', fp=captchaData, spoiler=False, description='Captcha Image')
    await interaction.response.send_message('Do ``/solve <captcha>`` when you\'re done.', file=captchaFile, ephemeral=True, delete_after=600)


@tree.command(name="solve", description="Submit a CAPTCHA answer", guild=discord.Object(id=1067257535549157427))
async def solve_command(interaction, captcha_answer: str):
    generatedAnswer = str(captchaList[interaction.user.id]).lower()
    if generatedAnswer == captcha_answer.lower():
        verified_role_id = 1069575551867682896
        verified = discord.Object(verified_role_id)

        velma = '<:velma:1071083663619535038>'

        await interaction.user.add_roles(verified)
        await interaction.response.send_message(f'You\'re Successfully Verified! {velma}', ephemeral=True, delete_after=600)
    else:
        await interaction.response.send_message('The CAPTCHA is wrong. Try again.', ephemeral=True, delete_after=600)

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=1067257535549157427))
    await client.change_presence(status= discord.Status.online, activity= discord.Streaming(name='account verification.', platform='Twitch', url='https://www.twitch.tv/directory'))
    print("Ready!")

client.run(token)