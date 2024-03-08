import discord
import random
from discord.ext import commands, tasks
import sqlite3
from config import TOKEN, SERVER_ID



intents = discord.Intents.default()
intents.members = True  # Nécessaire pour accéder aux membres du serveur
bot = commands.Bot(command_prefix='!', intents=intents)

# Dictionnaire pour stocker les pseudonymes originaux






    



@bot.event
async def on_ready():
    print("Bot logged in as {0.user}".format(bot))
    try:
        synced = await bot.tree.sync()
        print("synced")
    except:
        print("not synced")


@bot.tree.command(name="rando", description= "randomise tous les pseudos")
@commands.has_permissions(administrator=True)
async def randomize_nicknames(ctx):
    def populate_db(bot: discord.Client, SERVER_ID: int):
        conn = sqlite3.connect('discord_nicknames.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM nicknames')
        rows = cursor.fetchall()
        if len(rows) == 0:
            server = bot.get_guild(SERVER_ID)
            owner = server.owner
            try:
                for member in server.members:
                    if member == owner:
                        continue
                    cursor.execute("INSERT INTO nicknames VALUES (?, ?)", (member.id, member.display_name))
                conn.commit()
                conn.close()
                return 1
            except:
                conn.close()
                return -1
        else:
            conn.close()
            return 0

    status = populate_db(bot, SERVER_ID)
    if status == 1:
        print("La base de données a été remplie avec succès.")
    elif status == 0:
        print("La base de données est déjà remplie, les pseudos déjà randomisé")
        await ctx.response.send_message("La base de données est déjà remplie, les pseudos déjà randomisé")
    else:
        print("Une erreur s'est produite lors du remplissage de la base de données.")
        return

    original_nicknames = {}
    conn = sqlite3.connect('discord_nicknames.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM nicknames')
    rows = cursor.fetchall()
    original_nicknames = {row[0]: row[1] for row in rows}
    conn.close()

    li_errors=[]
    server = bot.get_guild(SERVER_ID)
    for member in server.members:
        if member == server.owner:
            continue
        else:
            try:
                new_nickname = ''.join(random.sample(member.display_name, len(member.display_name)))
                await member.edit(nick=new_nickname)
            except:
                li_errors.append(member.display_name)
                continue
    if len(li_errors) > 0:
        await ctx.response.send_message(f"Les pseudos ont été randomisés, mais une erreur s'est produite pour les pseudos suivants: {li_errors}")
    else:
        await ctx.response.send_message("Les pseudos ont été randomisés avec succès.")

        
            
            

@commands.has_permissions(administrator=True)
@bot.tree.command(name="restore", description= "restore tous les pseudos")
async def restore_nicknames(ctx):
    original_nicknames = {}
    conn = sqlite3.connect('discord_nicknames.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM nicknames')
    rows = cursor.fetchall()
    original_nicknames = {row[0]: row[1] for row in rows}
    conn.close()

    li_errors=[]
    server = bot.get_guild(SERVER_ID)
    for member in server.members:
        if member == server.owner:
            continue
        else:
            try:
                await member.edit(nick=original_nicknames[member.id])
            except:
                li_errors.append(member.display_name)
                continue
    if len(li_errors) > 0:
        try:
            await ctx.response.send_message(f"Les pseudos ont été restaurés, mais une erreur s'est produite pour les pseudos suivants: {li_errors}")
        except:
            await ctx.followup.send(f"Les pseudos ont été restaurés, mais une erreur s'est produite pour les pseudos suivants: {li_errors}")
    else:
        try:
            await ctx.response.send_message("Les pseudos ont été restaurés avec succès.")
        except:
            await ctx.followup.send("Les pseudos ont été restaurés avec succès.")

bot.run(TOKEN)