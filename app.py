import discord
import dotenv
import os
from dotenv import load_dotenv
from discord.ext import commands

# Load environment variables
load_dotenv()
token = os.getenv('TOKEN')

# Ensure the bot has the correct intents (enable message content intent)
intents = discord.Intents.default()
intents.message_content = True

# Create the bot instance
client = commands.Bot(command_prefix='$', intents=intents)

# Check if the token is found
if token is None:
    print('Token is missing')  # Check if token is missing
else:
    print('Token is found')  # Check if token is found

# Event when the bot has logged in and is ready
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

# Event to handle messages
@client.event
async def on_message(message):
    # Don't let the bot reply to its own messages
    if message.author == client.user:
        return

    # If the message is '$Ping', respond with 'Pong!'
    if message.content.startswith('$Ping'):
        await message.channel.send('Pong!')

    # Ensure other commands are processed properly
    await client.process_commands(message)

# Example command to say hello
@client.command()
async def hello(ctx):
    await ctx.send('Hello!')

# Ban command
@client.command()
@commands.has_permissions(ban_members=True)  # Ensure the user has the proper permissions
async def ban(ctx, member: discord.Member, *, reason=None):
    """Ban a member from the server."""
    if reason is None:
        reason = "No reason provided."
    
    try:
        await member.ban(reason=reason)
        await ctx.send(f"{member} has been banned for: {reason}")
    except discord.Forbidden:
        await ctx.send("I don't have permission to ban that user.")
    except discord.HTTPException as e:
        await ctx.send(f"An error occurred while trying to ban: {e}")
    except Exception as e:
        await ctx.send(f"An unexpected error occurred: {e}")
@client.command()
@commands.has_permissions(kick_members=True)  # Ensure the user has the proper permissions
async def kick(ctx, member: discord.Member, *, reason=None):
    """Kick a member from the server."""
    if reason is None:
        reason = "No reason provided."
    
    try:
        await member.kick(reason=reason)
        await ctx.send(f"{member} has been kicked for: {reason}")
    except discord.Forbidden:
        await ctx.send("I don't have permission to kick that user.")
    except discord.HTTPException as e:
        await ctx.send(f"An error occurred while trying to kick: {e}")
    except Exception as e:
        await ctx.send(f"An unexpected error occurred: {e}")
@client.command()
@commands.has_permissions(ban_members=True)  # Ensure the user has the proper permissions
async def unban(ctx, user: discord.User, *, reason=None):
    """Unban a user from the server."""
    if reason is None:
        reason = "No reason provided."
    
    try:
        await ctx.guild.unban(user, reason=reason)
        await ctx.send(f"{user} has been unbanned for: {reason}")
    except discord.Forbidden:
        await ctx.send("I don't have permission to unban that user.")
    except discord.HTTPException as e:
        await ctx.send(f"An error occurred while trying to unban: {e}")
    except Exception as e:
        await ctx.send(f"An unexpected error occurred: {e}")
@client.command()
@commands.has_permissions(manage_messages=True)  # Ensure the user has the proper permissions
async def clear(ctx, amount=5):
    """Clear a specified amount of messages."""
    try:
        await ctx.channel.purge(limit=amount)
    except discord.Forbidden:
        await ctx.send("I don't have permission to clear messages.")
    except discord.HTTPException as e:
        await ctx.send(f"An error occurred while trying to clear messages: {e}")
    except Exception as e:
        await ctx.send(f"An unexpected error occurred: {e}")
@client.command(pass_context=True)
@commands.has_role("Admin")
async def mute(ctx, member: discord.Member, time: int, *, reason=None):
    """Mute a member in the server for a specified time (in seconds)."""
    if reason is None:
        reason = "No reason provided."
    # Ensure the time is valid (greater than 0)
    if time <= 0:
        await ctx.send("Please specify a valid time greater than 0 seconds.")
        return
    try:
        # Timeout the user for the specified time
        await member.timeout(duration=discord.Duration(seconds=time), reason=reason)
        await ctx.send(f"{member} has been timed out for {time} seconds for: {reason}")
    except discord.Forbidden:
        await ctx.send("I don't have permission to timeout that user.")
    except discord.HTTPException as e:
        await ctx.send(f"An error occurred while trying to timeout: {e}")
    except Exception as e:
        await ctx.send(f"An unexpected error occurred: {e}")
@client.command()
@commands.has_permissions(administrator=True)  # Ensure the user invoking the command has administrator permissions
async def give_admin(ctx, member: discord.Member):
    """Give the Admin role to a specified member."""
    try:
        # Get the "Admin" role
        admin_role = discord.utils.get(ctx.guild.roles, name="Admin")
        
        if admin_role is None:
            await ctx.send("The 'Admin' role does not exist in this server.")
            return
        
        # Add the "Admin" role to the member
        await member.add_roles(admin_role)
        await ctx.send(f"{member} has been given the Admin role.")
    
    except discord.Forbidden:
        await ctx.send("I don't have permission to assign the Admin role.")
    except discord.HTTPException as e:
        await ctx.send(f"An error occurred while trying to give the Admin role: {e}")
    except Exception as e:
        await ctx.send(f"An unexpected error occurred: {e}")


# Run the bot with the token
client.run(token)
