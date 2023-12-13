import interactions
from interactions import Client, Intents, listen, slash_command, SlashContext, slash_option, OptionType
import os
import dotenv
import json
import requests
import io
import base64

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
@slash_option(
    name="prompt",
    description="The prompt ",
    required=True,
    opt_type=OptionType.STRING
)
async def image_function(ctx: SlashContext, prompt : str):
    payload = {
        "prompt": prompt,
        "steps": 5
    }

    response = requests.post(url=f"{url}/sdapi/v1/txt2img", json=payload)
    r = response.json()

    image_bytes = base64.b64decode(r['images'][0])
    #await ctx.send(file=interactions.File(io.BytesIO(image_bytes), file_name="image.png"), content={prompt})
    mention = f"<@{ctx.author.id}>"
    await ctx.send(f"**Prompt: {prompt}** by {mention}  ", file=interactions.File(io.BytesIO(image_bytes), file_name="image.png"))
    




















#* GET TOKEN
dotenv.load_dotenv(".env")
token = os.getenv("TOKEN")
bot.start(token)

