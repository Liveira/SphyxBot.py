import sys
sys.path.append('..')
from main import *
class EventLog(commands.Cog):
    @commands.group(name='eventlog', aliases=['event','el'],invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    @commands.before_invoke(usou)
    @commands.cooldown(1,5,commands.BucketType.member)
    @blacklists()
    async def eventlog(self,ctx,channel: discord.TextChannel=None):
        if await bl(ctx.author.id) == True:
                return
        if channel == None:
            await ctx.send(":x: | **Você esqueceu de inserir o canal de texto**") 
        else:
            await ctx.send("**Pronto...**, o event log foi ativado, porém ele está com a configuração ZERADA, para configurar use o comando `.eventlog config` que lá mostrara todas as configurações do event log!")
            dados = await Dados(ctx.guild.id)
            dados['config']['eventlog'] = {
                "chid":channel.id,
                "msgdel":False,
                "editmsgs":False,
                "leftmemb":False,
                "newmemb":False,
            }
            await salvarS(dados,ctx.guild.id)
    @eventlog.command(name='config')
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1,5,commands.BucketType.member)
    @blacklists()
    async def Econfig(self,ctx,coisa=None):
        if coisa == None:
            await ctx.send(":question: | **Aqui está um mini guia!, para ativar uma opção use o comando `.eventlog config <nome da config>` e para desativar use o comando novamente!**\n`newmemb` -> Avisa quando um membro entrar e quando um membro for desbanido\n`leftmemb` -> Avisa quando um membro saiu ou foi banido\n`msgdel` -> Avisa quando uma mensagem for apagada\n`editmsgs` -> Avisa quando uma mensagem for editada\n\nUm exemplo de como ativar uma opção: `.eventlog config leftmemb` e para desativar um comando é só usar o comando novamente")
            return
        d = await Dados(ctx.guild.id)
        try:
            if coisa not in d['config']['eventlog']:
                await ctx.send(":x: | **Tipo inválido, use o comando sem argumentos para ver a ajuda**")
            else:
                if d['config']['eventlog'][coisa] == False:
                    d['config']['eventlog'][coisa] = True
                    await ctx.send(":question: | **Opção ativada**")
                else:
                    d['config']['eventlog'][coisa] = False
                    await ctx.send(":question: | **Opção desativada**")
                await salvarS(d,ctx.guild.id)
        except Exception as ex:await ctx.send(ex.args)
    @eventlog.command(name='painel')
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1,5,commands.BucketType.member)
    @blacklists()
    async def painel(self,ctx):
        d = await Dados(ctx.guild.id)
        try:await ctx.send(f"Painel do eventlog\n\n**Entrada de membro**: {d['config']['eventlog']['newmemb']}\n**Saida de membro**: {d['config']['eventlog']['leftmemb']}\n**Mensagem editadas**: {d['config']['eventlog']['editmsgs']}\n**Mensagens apagadas**: {d['config']['eventlog']['msgdel']}")
        except: await ctx.send(":x: | **Você não ativou o event log, para ativar use `.eventlog`**")
    @commands.has_permissions(administrator=True)
    @eventlog.command(name='desativar')
    @commands.cooldown(1,5,commands.BucketType.member)
    @blacklists()
    async def desativ(self,ctx):
        d = await Dados(ctx.guild.id)
        try:
            d['config']['eventlog']['chid'] = 0
            await salvarS(ctx.guild.id)
            await ctx.send(":question: | **Event log desativado com sucesso**")
        except:
            await ctx.send(":x: | **Você não ativou o event log, para ativar use `.eventlog`**")
def setup(self):
    bot.add_cog(EventLog(bot))