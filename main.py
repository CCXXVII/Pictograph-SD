import interactions
from interactions import Client, Intents, listen, slash_command, SlashContext, slash_option, OptionType, SlashCommandChoice
import os
import dotenv
import requests
import io
import asyncio
import base64

bot = Client(intents=Intents.DEFAULT)
url = "http://127.0.0.1:7860"

@listen()
async def on_ready():
    print("Ready")
    print(f"This bot is owned by {bot.owner}")
@listen()
async def on_message_create(event):
    print(f"message received: {event.message.content}")


#* COMMANDS
#* FIRST COMMAND
@slash_command(name="image", description="Creates images with Stability Diffusion")


#! FIRST OPTION OF IMAGE COMMAND
@slash_option(
    name="prompt",
    description="Enter a text prompt to generate an image. Describe the scene or concept you have in mind.",
    required=True,
    opt_type=OptionType.STRING
)

#! SECOND OPTION OF IMAGE COMMAND
@slash_option(
    name="style",
    description="Choose a style for the image.",
    required=False,
    opt_type=OptionType.STRING,
    choices=[
        SlashCommandChoice(name="digital art", value="digital art"),
        SlashCommandChoice(name="anime", value="anime"),
        SlashCommandChoice(name="cinematic", value="cinematic"),
        SlashCommandChoice(name="analog film", value="analog film"),
        SlashCommandChoice(name="digital painting", value="digital painting"),
        SlashCommandChoice(name="black and white", value="black and white"),
        SlashCommandChoice(name="fantasy art", value="fantasy art"),
        SlashCommandChoice(name="cyber punk", value="cyber punk"),
        SlashCommandChoice(name="vector illustrations", value="vector illustration"),
        SlashCommandChoice(name="realistic photo portraits", value="realistic photo portraits"),
    ]
)

#! THIRD OPTION OF IMAGE COMMAND
@slash_option(
    name="negative_prompt",
    description="An optional text that provides a contrasting or opposing idea to the main prompt.",
    required=False,
    opt_type=OptionType.STRING
)

#! FOURTH OPTION OF IMAGE COMMAND
@slash_option(
    name="steps",
    description="desc step",
    required=False,
    opt_type=OptionType.INTEGER,
    max_value=51
)
#! FIFTH OPTION OF IMAGE COMMAND
@slash_option(
    name="width",
    description="desc width",
    required=False,
    opt_type=OptionType.INTEGER,
    min_value=312,
    max_value=1024
)

#! SIXTH OPTION OF IMAGE COMMAND
@slash_option(
    name="height",
    description="desc height",
    required=False,
    opt_type=OptionType.INTEGER,
    min_value=312,
    max_value=1024
)

#* RUNNING FUNCTION
async def image_function(ctx: SlashContext, 
                         prompt: str, 
                         style: str = "Digital Art", 
                         negative_prompt: str="text", 
                         width: int = 512, 
                         height: int = 512,
                         steps: int = 10
                         ):
    await ctx.defer()
    
    payload = {
        "prompt": prompt,
        "styles": [style],
        "negative_prompt" : negative_prompt,
        "width" : width,
        "height" : height,
        "steps": steps
    }
    
    response = requests.post(url=f"{url}/sdapi/v1/txt2img", json=payload)
    r = response.json()
    image_bytes = base64.b64decode(r['images'][0])
    image = io.BytesIO(image_bytes)
    
    await asyncio.sleep(12)

    # A display method to to see the image in jupyter > 
    # >>>>>  display(Image(data=img.getvalue(), format='png'))

    mention = f"<@{ctx.author.id}>"
    file_name = f"{prompt}.png"
    await ctx.send(f"**Prompt: {prompt}** by {mention}  ", 
                   file=interactions.File(image, file_name=file_name))
    
























#* GET TOKEN
dotenv.load_dotenv(".env")
token = os.getenv("TOKEN")
bot.start(token)

