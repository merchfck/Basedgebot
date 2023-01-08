from settings import bot_name, token, initial_channels, secondary_prefix, prefix
from bot import chat_output, debug, insert, update
from twitchio.ext import commands
from twitchio import Channel
import re

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            token=token,
            prefix=prefix,
            initial_channels=initial_channels,
            case_insensitive=True)

    async def event_channel_joined(self, channel: Channel):
        print(f"{bot_name} launched on https://www.twitch.tv/{channel.name} channel")

    async def event_message(self, message):
        if message.echo:
            return

        print(chat_output(message))

        if not(debug("exist", message.author.name)):
            insert("reg", [message.author.name, message.author.display_name, message.channel.name])

        if message.content[0] != prefix:
            message.content = prefix + message.content

        await self.handle_commands(message) #

    @commands.command(name=f"{secondary_prefix}remove")
    async def remove_emotes(self, ctx: commands.Context):
        content = ctx.message.content.split()
        if len(content) > 1:
            emote = content[1]
            update("remove_emote", [ctx.channel.name, emote])
            await ctx.reply(f"⚙️ Emote {emote.capitalize()} successfully removed")
        else:
            await ctx.reply(f"⚙️ {secondary_prefix}remove <emote>")

    @commands.command(name="профиль")
    async def profile(self, ctx: commands.Context):
        content = ctx.message.content.split()
        if len(content) > 1:
            username = content[1].lower()[0:50]

            try:
                await ctx.reply(f"{debug('emote', username)} {debug('display_name', username)}: ID: {debug('id', username)}")
            except:
                await ctx.reply(f"⚙️ Игрока {username.capitalize()} не существует")
        else:
            await ctx.reply(f"{debug('emote', ctx.message.author.name)} {ctx.message.author.display_name}: ID: {debug('id', ctx.message.author.name)}")

if __name__ == "__main__":
    bot = Bot()
    bot.run()