import sys
sys.path.append('..')
from main import *
class ReactionRoles(commands.Cog):
        @commands.group(name='rr',aliases=['reactionroles'],invoke_without_command=True) 
        @commands.has_permissions(manage_roles=True)
        @commands.before_invoke(usou)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def rr(self,ctx,channelA: discord.TextChannel=None,message_id=None,emoji=None,cargo: discord.Role=None):
            if await bl(ctx.author.id) == True:
                return
            if channelA == None:
                await padrao(ctx,'Moderação','ReactionRoles','ReactionRoles (RR) É um sistema de reação por cargos, você reagir em um emoji e ganha um cargo que a staff decidir','`rr <id da mensagem> <emoji> <cargo>`','```rr | reactionroles```','Staff')         
            else:
                channel = await bot.fetch_channel(channelA.id)
                msg = await channel.fetch_message(int(message_id))
                dados = await Dados(ctx.guild.id)
                dados['config']['rrcont'] += 1
                cont = dados['config']['rrcont']
                try:
                    emoji = await bot.get_emoji(int(emoji))    
                    dados['config']['rr'][str(cont)] = {
                    'emoji':str(emoji.id),
                    'role':str(cargo.id),
                    'msg':str(message_id)
                }
                except ValueError:
                    dados['config']['rr'][str(cont)] = {
                    'emoji':str(emoji),
                    'role':str(cargo.id),
                    'msg':str(message_id)
                    }
                await salvarS(dados,ctx.guild.id)
                await msg.add_reaction(emoji)
                await ctx.send(":question: | **ReactionRole Setado com sucesso**")
        @commands.Cog.listener()
        async def on_raw_reaction_add(self, payload):
            channel = await bot.fetch_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            user = await message.guild.fetch_member(payload.user_id)
            emojiA = payload.emoji
            dados = await Dados(message.guild.id)
            if user.bot == True: return
            for i in dados['config']['rr']:
                if str(message.id) in dados['config']['rr'][i]['msg']:
                    try:
                        emoji = await user.guild.fetch_emoji(int(dados['config']['rr'][i]['emoji']))
                    except ValueError:
                        emoji = dados['config']['rr'][i]['emoji']
                    if str(emojiA) == str(emoji):
                        role = user.guild.get_role(int(dados['config']['rr'][i]['role']))
                        await user.add_roles(role)
        @commands.Cog.listener()
        async def on_raw_reaction_remove(self, payload):
            channel = await bot.fetch_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            user = await message.guild.fetch_member(payload.user_id)
            emojiA = payload.emoji
            dados = await Dados(message.guild.id)
            if user.bot == True: return
            for i in dados['config']['rr']:
                if str(message.id) in dados['config']['rr'][i]['msg']:
                    try:
                        emoji = await user.guild.fetch_emoji(int(dados['config']['rr'][i]['emoji']))
                    except ValueError:
                        emoji = dados['config']['rr'][i]['emoji']
                    if str(emojiA) == str(emoji):
                        role = user.guild.get_role(int(dados['config']['rr'][i]['role']))
                        await user.remove_roles(role)
def setup(self):
    bot.add_cog(ReactionRoles(bot))