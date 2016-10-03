import discord
from discord.ext import commands
from isAllowed import *
import requests
import os


class OwnerCommands():

	def __init__(self, bot):
		self.bot = bot


	## Change the icon of the bot
	@commands.command(pass_context=True)
	async def av(self, ctx):
	    if allowUse(ctx, ['is_caleb']):
	        try:
	        	## Get the url of the image
	            a = requests.get(ctx.message.content.split(' ', 1)[1]).content

	            ## Change the avatar
	            await self.bot.edit_profile(avatar=a)
	            await self.bot.say("Changed profile image.")
	        except Exception as e:

	        	## Work out what went wrong
	            exc = '{}: {}'.format(type(e).__name__, e)
	            await self.bot.say("Something went wrong :: {}".format(exc))
	    else:
	    	## Tell people when they aren't allowed
	        await self.bot.say(notallowed)


	## Restart any running instance of the bot
	@commands.command(pass_context=True, aliases=['rs'])
	async def restart(self, ctx):
	    if allowUse(ctx, ['is_caleb']):
	    	## Write to file the channel that needs to be pinged when online again
	        with open(workingDirectory + 'restartFile.txt', 'w') as a:
	            a.write(str(ctx.message.channel.id))
	        await self.bot.say("Restarting...")

	        ## os restart
	        os.execl(sys.executable, *([sys.executable] + sys.argv))
	    else:
	        await self.bot.say(notallowed)
	    return


	## Kill all running instances of the bot
	@commands.command(pass_context=True, aliases=['k'])
	async def kill(self, ctx):
	    if allowUse(ctx, ['is_caleb']):
	    	## Exit using sys
	        await self.bot.say("Killing.")
	        sys.exit()
	    else:
	        await self.bot.say(notallowed)


	## Run any given line of code
	@commands.command(pass_context=True, hidden=True)
	async def ex(self, ctx):
	    if allowUse(ctx, ['is_caleb']):
	        exec(ctx.message.content.split(' ',1)[1])
	    else:
	        await self.bot.say(notallowed)


	## Reload an extention without restarting bot
	@commands.command(aliases=["rldext"],pass_context=True)
	async def reloadextension(self, ctx, *, ext: str=None):
	    """Reload bot extension"""
	    if allowUse(ctx, ['is_caleb']):
	    	## Check there's an extention being asked about
	        if ext == None:
	            await self.bot.say("Please choose an extension, currently available to be reloaded are:\n```" + "\n".join(bot.cogs) + "```")
	            return

	        await self.bot.say("Reloading extension...")
	        try: 
	        	## Unload it
	        	self.bot.unload_extension(ext)
	        except: 
	        	pass

	        try: 
	        	## Load it
	        	self.bot.load_extension(ext)
	        except:
	            await bot.say("That extention does not exist.")
	            return

	        await self.bot.say("Done!")
	    else:
	        await self.bot.say(notallowed)


def setup(bot):
    bot.add_cog(OwnerCommands(bot))
