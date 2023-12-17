import interactions
from interactions import Client, Intents, listen, slash_command, SlashContext, slash_option, OptionType
import os
import dotenv
import requests
import io
import base64
from interactions import SlashCommandChoice

bot = Client(intents=Intents.DEFAULT)

@listen()
async def on_ready():
    print("Ready")
    print(f"This bot is owned by {bot.owner}")
@listen()
async def on_message_create(event):
    print(f"message received: {event.message.content}")


#* COMMANDS
#* FIRST COMMAND
url = "http://127.0.0.1:7860"
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
    name="negativeprompt",
    description="An optional text that provides a contrasting or opposing idea to the main prompt.",
    required=False,
    opt_type=OptionType.STRING
)

#! FOURTH OPTION OF IMAGE COMMAND
@slash_option(
    name="steps",
    description="",
    required=False,
    opt_type=OptionType.INTEGER,
    min_value=10,
    max_value=50
)
#! FIFTH OPTION OF IMAGE COMMAND
@slash_option(
    name="width",
    description="",
    required=False,
    opt_type=OptionType.INTEGER,
    min_value=312,
    max_value=1024
)

#! SIXTH OPTION OF IMAGE COMMAND
@slash_option(
    name="height",
    description="",
    required=False,
    opt_type=OptionType.INTEGER,
    min_value=312,
    max_value=1024
)


#* RUNNING FUNCTION
async def image_function(ctx: SlashContext, 
                         prompt: str, 
                         style: str = "Digital Art", 
                         negative_prompt: str="", 
                         width: int = 512, 
                         height: int = 512,
                         steps: int = 20
                         
                         ):
    
    

    payload = {
        "prompt": prompt,
        "negative_prompt" : negative_prompt,
        "styles": [style],
        "steps": steps,
        "width" : width,
        "height" : height
    }

    response = requests.post(url=f"{url}/sdapi/v1/txt2img", json=payload)
    r = response.json()
    image_bytes = base64.b64decode(r['images'][0])
    

    # A display method to to see the image in jupyter > 
    # >>>>>  display(Image(data=img.getvalue(), format='png'))
    mention = f"<@{ctx.author.id}>"
    await ctx.send(f"**Prompt: {prompt}** by {mention}  ", file=interactions.File(io.BytesIO(image_bytes), file_name="image.png"))
























#* GET TOKEN
dotenv.load_dotenv(".env")
token = os.getenv("TOKEN")
bot.start(token)

