import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import openai

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_TOKEN = os.getenv("OPENAI_TOKEN")
openai.api_key = OPENAI_TOKEN

"""
Converts natural language to an SQLite query via the OpenAI API

:param query : The natural language query to convert.
:return : SQLite SELECT query representing the natural language query provided.
"""
def convert(query:str) -> str:
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

"""
NLQ Discord bot command
"""
@bot.command(name="nlq")
async def nlq(ctx, *args : list[str]) -> None:
    query = " ".join(args)
    await ctx.send(convert(query))


bot.run(DISCORD_TOKEN)
