import discord
from discord.ext import commands
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive


client = commands.Bot(command_prefix = '!')

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing", "help"]

starter_encouragements = [
  "If you're feeling down, try to go outside and get some fresh air. Take a stroll through your neighborhood!", 
  "Take a break if you're feeling overwhelmed. Try taking deep breaths for 30 seconds.",
  "You are not alone in your sadness and there are people who care about you.",
  "Take some time to yourself. Make sure to drink lots of water and stay hydrated!",
  "Pause and take a breather. Meditation is known for alleviating some anxiety symptoms."
]

if "responding" not in db.keys() or db["responding"] == False:
  db["responding"] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragement(index):
  encouragements = list(db["encouragements"])
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements

def update_vents(vent_message):
  if "vents" in db.keys():
    vents = db["vents"]
    vents.append(vent_message)
    db["vents"] = vents
  else:
    db["vents"] = [vent_message]

def delete_vent(index):
  vents = list(db["vents"])
  if len(vents) > index:
    del vents[index]
    db["vents"] = vents

@client.event
async def on_ready():
  print("We have logged in as {0.user}"
.format(client))

@client.command()
async def quote(ctx):
  quote = get_quote()
  await ctx.send(quote)

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  if db["responding"]:
    options = starter_encouragements
    if "encouragements" in db.keys():
      options = options + list(db["encouragements"])

    if any(word in message.content.lower() for word in sad_words):
      await message.channel.send(random.choice(options))

  await client.process_commands(message)

@client.command()
async def addVent(ctx, *, arg):
  update_vents(arg)
  await ctx.send("New vent message added.")

@client.command()
async def deleteVent(ctx, arg):
  vents = []
  if "vents" in db.keys():
    if not arg.isdigit() or int(arg) + 1 > len(list(db["vents"])) or int(arg) < 0:
      await ctx.send("Please enter a valid index between 0 and " + str(len(list(db["vents"]))-1) + ".")
      return
    index = int(arg)
    delete_vent(index)
    vents = list(db["vents"])
  await ctx.send(vents)

@client.command()
async def viewVent(ctx):
  vents = []
  if "vents" in db.keys():
    vents = list(db["vents"])
  await ctx.send(vents)

@client.command()
async def addEncouragement(ctx, *, arg):
  update_encouragements(arg)
  await ctx.send("New encouraging message added.")

@client.command()
async def deleteEncouragement(ctx, arg):
  encouragements = []
  if "encouragements" in db.keys():
    if not arg.isdigit() or int(arg) + 1 > len(list(db["encouragements"])) or int(arg) < 0:
      await ctx.send("Please enter a valid index between 0 and " + str(len(list(db["encouragements"]))-1) + ".")
      return
    index = int(arg)
    delete_encouragement(index)
    encouragements = list(db["encouragements"])
  await ctx.send(encouragements)

@client.command()
async def viewEncouragement(ctx):
  encouragements = []
  if "encouragements" in db.keys():
    encouragements = list(db["encouragements"])
  await ctx.send(encouragements)

@client.command()
async def responding(ctx, arg):
  if arg.lower() == "on":
    db["responding"] = True
    await ctx.send("Responding is on.")
  elif arg.lower() == "off":
    db["responding"] = False
    await ctx.send("Responding is off.")
  else:
    await ctx.send('Not a valid input. Please enter \"on\" or \"off\".')

@client.command()
async def hotlines(ctx):
  embed = discord.Embed(
    title = 'Hotlines',
    description = 'Here is a list of free mental health hotlines and their respective countries.',
    colour = discord.Colour.blue()
  )

  embed.set_footer(text='You are not alone.')
  embed.set_image(url='https://cdn.discordapp.com/attachments/881182437382684702/881394376138448896/unknown.png')
  embed.set_thumbnail(url='https://media.discordapp.net/attachments/881044747643392021/881392437468209152/Untitled_design_2-removebg-preview.png')
  embed.add_field(name='Canada', value = '1-800-668-6868', inline=True)
  embed.add_field(name='USA', value = '1-800-273-8255 ', inline=True)
  embed.add_field(name='UK', value = '116-123', inline=True)
  embed.add_field(name='Australia', value = '13-11-14', inline=True)
  embed.add_field(name='New Zealand', value = '09 5222 999', inline=True)
  embed.add_field(name='South Africa', value = '0514445691', inline=True)

  await ctx.send(embed=embed)

r = requests.head(url="https://discord.com/api/v1")
try:
    print(f"Rate limit {int(r.headers['Retry-After']) / 60} minutes left")
except:
    print("No rate limit")


keep_alive()
client.run(os.environ['TOKEN'])







