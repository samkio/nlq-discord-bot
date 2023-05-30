import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import openai

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_TOKEN = os.getenv("OPENAI_TOKEN")
openai.api_key = OPENAI_TOKEN


def convert(query):
    # TODO input validation, sanitization
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"### SQLite tables, with their properties:\n#\n#\n#\n### A query to {query}\nSELECT",
        temperature=0,
        max_tokens=150,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["#", ";"],
    )
    # TODO error handling
    # TODO output validation, sanitization
    return f"```sql\nSELECT{response.choices[0].text};```"


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="?", intents=intents)


@bot.command(name="nlq")
async def nlq(ctx, *args):
    query = " ".join(args)
    await ctx.send(convert(query))


bot.run(DISCORD_TOKEN)
