import asyncio
from random import randrange
import time
import discord,json,datetime,random,os
from discord.ext import commands
from discord.ext.commands.errors import RoleNotFound
from discord.flags import Intents
intents = intents = discord.Intents.all()
log = ""
def prefix(bot,message):
    with open("dados.json","r") as f:
	    prefixo = json.load(f)
    return prefixo["Servers"][str(message.guild.id)]['config']['prefix']
bot = commands.Bot(command_prefix=prefix,case_insensitive=True,intents=intents)
bot.remove_command("help")
#Variaveis
class token():
    def token():
        bottoken='Seu prefixo!'
        return bottoken
epoch = datetime.datetime.utcfromtimestamp(0)
#Funções
@bot.event
async def on_ready():
    await outroloop()
async def padrao(ctx: object,nomeEmbed: str,name: str,desc: str,como: str,aliases: str,perm: str) -> None:
    if perm == "Staff":
        embed = discord.Embed(title=f'Ajuda de {nomeEmbed}',description=f'Esse painel mostrara como usar o {name}, somente a Staff podem usar esse comando\n\n :question:  **Para que serve?**\n\n {desc}\n\n\n :question: **Quais são os comandos?**\n\n {como} \n\n** :globe_with_meridians: Outros nomes**\n {aliases}')
    else:
        embed = discord.Embed(title=f'Ajuda de {nomeEmbed}',description=f'Esse painel mostrara como usar o {name}, todos podem usar esse comando\n\n :question:  **Para que serve?**\n\n {desc}\n\n\n :question: **Quais são os comandos?**\n\n {como} \n\n** :globe_with_meridians: Outros nomes**\n {aliases}')
    await ctx.send(embed=embed)
async def Dados() -> json:
    with open('dados.json','r')as f:
        return json.load(f)
async def UDados() -> json:
    with open('users.json','r')as f:
        return json.load(f)
async def CConta(user: discord.Member):
    dados = await UDados()
    if str(user.id) in dados['Users']:
        return
    else:
        dados['Users'][str(user.id)] = {'nome':user.name,'desc':'Usuario','rep':0,"xp_time":0}
        with open('users.json','w') as f:
            json.dump(dados,f,indent=4)
async def GCConta(guild: discord.Guild):
    dados = await Dados()
    if str(guild.id) in dados["Servers"]:
        return
    else:
        dados['Servers'][str(guild.id)] = {'users':{},'config':{'time_xp':30,'role_mute':0,'welcome_channel':0,'mediaxp':10,'WelcomeMsg':' Bem vindo! ','LeaveMsg':'Saiu do servidor!','dmpu':0,'prefix':'#','autorole':{},'controle':0},'reg':{},'contIDreg':0}
    with open('dados.json','w') as f:
        json.dump(dados,f,indent=4)
async def loop():
    while True:
        await asyncio.sleep(15)
        dados = await Dados()
        udados = await UDados()
        cont=0
        contU=0
        contD=0
        async for guild in bot.fetch_guilds(limit=None):
            cont+=1
            if str(guild.id) not in dados['Servers']:
                await GCConta(guild)
            async for member in guild.fetch_members(limit=None):
                if str(member.id) in dados['Servers'][str(guild.id)]['users']:
                    pass
                else:
                    contD+=1
                    dados['Servers'][str(guild.id)]['users'][str(member.id)] = {'warns':0,'ficha':{},'fichamute':{},'contmute':0,'xp':0,'msg':0} 
                if str(member.id) in udados['Users']:
                    pass
                else:
                    contU += 1      
                    await CConta(member)
            with open('dados.json','w') as f:
                json.dump(dados,f,indent=4)
        global log
        log = log + "\n" + '------------------'
        log = log + "\n" + f"[{str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))}]\n"
        log = log + "\n" + f"Foi registrado: {contU} contas"
        log = log + "\n" + f"Foi registrado: {contD} contas de {cont} Servidores"
        log = log + "\n" + '------------------\n\n'
async def outroloop():
    while True:
        await asyncio.sleep(20000)
        f = open(f"logs/{str(time.strftime('%Y-%m-%d %H-%M-%S', time.localtime()))}.txt","x")
        with open(f.name,"w") as f:
            f.write(log)
        file = discord.File(open(f.name,'rb'))
        channel = bot.get_channel(785611411043647578)
        await channel.send(file=file)
        log = ""
# Eventos...
class events(commands.Cog):
    @commands.Cog.listener()
    async def on_ready(self):
        print('.................')
        print('Sphyx está ligado!')
        print('.................')
        print('       LOG       ')
        print('                 ')
        await loop()  
    @commands.Cog.listener()
    async def on_message(self,message):
        
        
        if message.author.bot != True:
            dados = await Dados()
            config = dados['Servers'][str(message.guild.id)]['config']
            if bot.user.mentioned_in(message):
                await message.channel.send(f":question: | `{config['prefix']}help` **<- Comando de ajuda**")
            xp = dados['Servers'][str(message.guild.id)]['users'][str(message.author.id)]['xp']
            dados['Servers'][str(message.guild.id)]['users'][str(message.author.id)]['msg'] += 1
            user = message.author
            if user.id in dados:
                pass
            else:
                await CConta(user)
            time_diff = (datetime.datetime.utcnow() - epoch).total_seconds() - dados['Servers'][str(message.guild.id)]['users'][str(message.author.id)]['xp_time']
            if time_diff >= dados['Servers'][str(message.author.guild.id)]['config']['time_xp']:
                   dados['Servers'][str(message.guild.id)]['users'][str(message.author.id)]['xp'] += int(randrange(int(int(config['mediaxp']) /2),int(int(config['mediaxp']))))
                   dados['Servers'][str(message.guild.id)]['users'][str(message.author.id)]['xp_time'] = (datetime.datetime.utcnow() - epoch).total_seconds()
            with open('dados.json','w')as f:
                json.dump(dados,f,indent=4)
    @commands.Cog.listener()
    async def on_guild_join(self,guild):
        print('SphyX Entrou em ' + guild.name)
        dados = await Dados()
        cont=0
        user={}
        if str(guild.id) in dados['Servers']:
            return
        dados['Servers'][str(guild.id)] = {'users':{},'config':{'time_xp':30,'role_mute':0,'welcome_channel':0,'mediaxp':10,'WelcomeMsg':' Bem vindo! ','LeaveMsg':'Saiu do servidor!','dmpu':0,'prefix':'.','autorole':0},'reg':{},'contIDreg':0}
        async for i in guild.fetch_members(limit=None):
            if i.bot != True:
                dados['Servers'][str(guild.id)]['users'][str(i.id)] = {'warns':0,'ficha':{},'fichamute':{},'contmute':0,'xp':0,'msg':0}
                print(dados['Servers'][str(guild.id)]['users'][str(i.id)])
                await CConta(i)
        with open('dados.json','w') as f:
            json.dump(dados,f,indent=4)
    @commands.Cog.listener()
    async def on_member_join(self,member):
        dados = await Dados()
        print(member.name)
        for i in dados['Servers'][str(member.guild.id)]['config']['autorole']:
            role = member.guild.get_role(dados['Servers'][str(member.guild.id)]['config']['autorole'][i]['roleid'])
            await member.add_roles(role)
        mensagem = dados['Servers'][str(member.guild.id)]['config']['WelcomeMsg']
        mensagem = mensagem.replace('[mention]',member.mention)
        mensagem = mensagem.replace('[user]',member.name)
        mensagem = mensagem.replace('[usertag]',member.name + '#' + member.discriminator)
        mensagem = mensagem.replace('[guildname]',member.guild.name)
        channel = bot.get_channel(int(dados['Servers'][str(member.guild.id)]['config']['welcome_channel']))        
        await channel.send(mensagem)
        await CConta(member)
        dados['Users'][str(member.id)] = {'nome':member.name,'warns':{},'desc':'Usuario','rep':0,"xp_time":0}
        with open('users.json','w') as f:
            json.dump(dados,f,indent=4)

    @commands.Cog.listener()
    async def on_member_remove(self,member):
        dados = await Dados()
        print(member.name)
        mensagem = dados['Servers'][str(member.guild.id)]['config']['LeaveMsg']
        mensagem = mensagem.replace('[mention]',member.mention)
        mensagem = mensagem.replace('[user]',member.name)
        mensagem = mensagem.replace('[usertag]',member.name + '#' + member.discriminator)
        mensagem = mensagem.replace('[guildname]',member.guild.name)
        channel = bot.get_channel(int(dados['Servers'][str(member.guild.id)]['config']['welcome_channel']))        
        await channel.send(mensagem)

bot.add_cog(events(bot))

# Comandos...

# Moderação
class Moderacao():
    class warn(commands.Cog):
        @commands.group(name='warn', invoke_without_command=True)
        @commands.has_permissions(kick_members=True)
        async def cmdwarn(self, ctx, user: discord.Member=None, *, Motivo='Não especificado'):
            if user == None:
                await padrao(ctx,'Moderação','warn','Serve para avisar membros, quando se usa em uma pessoa, é registrado +1 warn nos registro do usuario','`warn <user>* <motivo>` -> Serve para avisar o usuario\n`list <user>*` -> Serve para ver o registro de warns, motivo, e quem deu warn\n`edit <user> <motivo>` -> Serve para alterar o motivo do warn','```warn | avisar```','Staff')
            elif user.id == ctx.author.id:
                await ctx.send(":x: | **Você não pode se \"Auto avisar\"**")
                return
            elif user.top_role >= ctx.author.top_role:
                await ctx.send(":x: | **Seu cargo está abaixo do usuario**")
                return
            else:
                
                dados = await Dados()
                guild = user.guild.id
                userID = user.id
                dados['Servers'][str(guild)]['users'][str(userID)]['warns'] += 1
                cont = dados['Servers'][str(guild)]['users'][str(userID)]['warns']
                dados['Servers'][str(guild)]['users'][str(userID)]['ficha'][str(cont)] = {
                    "Motivo":Motivo,
                    "ID":cont,
                    "Staff":ctx.author.name
                }
                with open('dados.json','w') as f:
                    json.dump(dados,f,indent=4)
                await ctx.send(f'{user.name} Levou warn, motivo: {Motivo}, Já é o {cont}° Warn que ele já tem')
                if dados['Servers'][str(guild)]['config']['dmpu'] == 0:
                    pass
                else:
                    await user.send(f"Você tomou warn, motivo: {Motivo}, evite o maximo levar warn.")
                global log
                log = log + '\n' + f'{user.name} levou warn no servidor {ctx.guild.name}, motivo {Motivo}'
        @cmdwarn.command(name='check',aliases=['list'])
        @commands.has_permissions(kick_members=True)
        async def check(self,ctx,user: discord.Member=None):
            if user == None:
                await padrao(ctx,'Moderação','list','Serve para listar todos os warns de um determinado membro, alem de listar, ele mostra todas as informações que podem ser úteis!','```warn list <user>*```','```Listar | Check```','Staff')
            else:
                msg=''
                dados = await Dados()
                for i in dados['Servers'][str(user.guild.id)]['users'][str(user.id)]['ficha']:
                    msg = msg + '\n' + str(dados['Servers'][str(user.guild.id)]['users'][str(user.id)]['ficha'][i]['ID']) + ' - ' + dados['Servers'][str(user.guild.id)]['users'][str(user.id)]['ficha'][i]['Motivo'] + ' - ' + dados['Servers'][str(user.guild.id)]['users'][str(user.id)]['ficha'][i]['Staff']
                embed = discord.Embed(title=f'Ficha de {user.name}',description='```INDEX|MOTIVO|STAFF\n'+msg+'\n```')
                await ctx.send(embed=embed)              
        @cmdwarn.command(name='edit',aliases=['editar'])
        @commands.has_permissions(kick_members=True)
        async def edit(self,ctx,user: discord.Member=None,index=None,novomotivo='Não especificado'):
            if user == None:
                await padrao(ctx,'Moderação','edit','Serve para editar um determinado warn','```warn edit <user>* <index>* <novo_motivo>*```','```edit | editar```','Staff')
            else:
                dados = await Dados()
                if index == None or index not in dados['Servers'][str(ctx.guild.id)]['users'][str(user.id)]['fichamute']:
                    await ctx.send(":x: | **Index inválida, para saber as index válidas use o `warn list <member>`**")
                else:
                    dados['Servers'][str(ctx.guild.id)]['users'][str(user.id)]['fichae'][index]['Motivo'] = novomotivo
                    with open('dados.json','w') as f:
                        json.dump(dados,f,indent=4)
                    await ctx.send(":question: | **Warn editado com sucesso**")
    class unwarn(commands.Cog):
        @commands.command(name='unwarn',aliases=['desavisar'])
        @commands.has_permissions(kick_members=True)
        async def unwarn(self,ctx,user:discord.Member=None,index: int=None,*,motivo='Não especificado'):
            if user == None:
                await padrao(ctx,'Moderação','unwarn','Serve para remover o warn de um membro','`unwarn <user> <index> <motivo>','```unwarn | desavisar ```','Staff')
            elif user.id == ctx.author.id:
                    await ctx.send(":x: | **Você não pode tirar o seu próprio aviso**")
                    return
            elif user.top_role >= ctx.author.top_role:
                await ctx.send(":x: | **Seu cargo está abaixo do usuario**")
                return
            else:
                dados = await Dados()
                if dados['Servers'][str(ctx.guild.id)]['users'][str(user.id)]['warns'] == 0:
                    await ctx.send(":x: | **O Usuario não tem avisos**")
                    return
                else:
                    dados['Servers'][str(ctx.guild.id)]['users'][str(user.id)]['warns'] -= 1
                    if index == None:
                        index = dados['Servers'][str(ctx.guild.id)]['users'][str(user.id)]['warns']
                    del dados['Servers'][str(ctx.guild.id)]['users'][str(user.id)]['ficha'][str(index)]
                    with open('dados.json','w') as f:
                        json.dump(dados,f,indent=4)
                    await ctx.send(f":question: | **O Aviso do usuario {user.name} foi removido!**")
                    if dados['Servers'][str(ctx.guild.id)]['users'][str(user.id)]['config']['dmpu'] == 1:
                        await user.send(":warning: | **Seu aviso foi removido**")  
                    global log
                    log = log + '\n' + f'{user.name} warn retirado no servidor {ctx.guild.name}'             
    class mute(commands.Cog):
        @commands.group(name='mute',invoke_without_command=True)
        @commands.has_permissions(kick_members=True)
        async def mute(self,ctx,user: discord.Member=None,tempoMute=None,motivo='Não especificado'):
            if user == None:
                await padrao(ctx,'Moderação','mute','Serve para mutar um usuario por um determinado tempo, caso não coloque nenhum tempo o tempo vai ser automaticamente inderteminado ou permanente','`mute <user>* <tempo> <motivo>','```mute | silenciar | mutar```','Staff')
                return
            dados = await Dados()
            time=0
            try:
                role = ctx.guild.get_roles(dados['Servers'][str(ctx.guild.id)]['config']['role_mute'])
            except RoleNotFound:
                await ctx.send(":x: | **Você não configurou o cargo de mute! Configure usando o comando** `config role-mute <cargo>`")
                return

            try:       
                if tempoMute[1] == 'm' or tempoMute[2] == 'm':
                    tempoMute = tempoMute.replace('m','')
                    time=int(tempoMute)
                    time = time * 60
            except IndexError:
                pass
            try:
                if tempoMute[1] == 'h' or tempoMute[2] == 'h':
                    tempoMute = tempoMute.replace('h','')
                    time=int(tempoMute)
                    time = time * 60 * 60
            except IndexError:
                pass
            try:
                if tempoMute[1] == 'd' or tempoMute[2] == 'd':
                    tempoMute = tempoMute.replace('d','')
                    time=int(tempoMute)
                    time = time * 60 * 60 * 60
            except IndexError:
                pass
            if tempoMute == None:
                await user.add_roles(role)
                await ctx.send(f":question: | **O Usuario: {user.name} foi mutado por um tempo inderterminado, motivo: {motivo}**")
                if dados['Servers'][str(ctx.guild.id)]['config']['dmpu'] == 1:
                    await user.send(f"Você está **Mutado** por tempo inderteminado, motivo: {motivo}")
                return
            user.add_roles(role)
            cont=0
            await ctx.send(f":question: | **O Usuario: {user.name} foi mutado por {tempoMute}, motivo: {motivo}")
            if dados['Servers'][str(ctx.guild.id)]['config']['dmpu'] == 1:
                    await user.send(f"Você está **Mutado** por {tempoMute}, motivo: {motivo}")
            dados['Servers'][str(ctx.guild.id)]['users'][str(ctx.author.id)]['warns'] += 1
            cont = dados['Servers'][str(ctx.guild.id)]['users'][str(ctx.author.id)]['warns']
            dados['Servers'][str(ctx.guild.id)]['users'][str(ctx.author.id)]['ficha'][str(cont)] = {
                    "Motivo":motivo,
                    "tempo":tempoMute,
                    "ID":cont,
                    "Staff":ctx.author.name
                }
            global log
            log = log + '\n' + f'{user.name} levou mute no servidor {ctx.guild.name} por o tempo {tempoMute}, motivo: {motivo}'
            with open('dados.json','w') as f:
                json.dump(dados,f,indent=4)
            await asyncio.sleep(time)        
            user.remove_roles(role)
        @mute.command(name='check',alises=['list'])
        @commands.has_permissions(kick_members=True)
        async def check(self,ctx,user: discord.Member=None):
            if user == None:
                await padrao(ctx,'Moderação','mute check','Serve para listar todos os mutes do membro mostrando o motivo, o tempo do mute, e quem mutou!','`mute check <user>*` -> lista todos os mutes do membro','```check | list```','Staff')
            else:
                msg=''
                dados = await Dados()
                for i in dados['Servers'][str(user.guild.id)]['users'][str(user.id)]['fichamute']:
                    msg = msg + '\n' + str(dados['Servers'][str(user.guild.id)]['users'][str(user.id)]['fichamute'][i]['ID']) + ' - ' + dados['Servers'][str(user.guild.id)]['users'][str(user.id)]['fichamute'][i]['Motivo'] + ' - ' +dados['Servers'][str(user.guild.id)]['users'][str(user.id)]['fichamute'][i]['tempo']+ dados['Servers'][str(user.guild.id)]['users'][str(user.id)]['fichamute'][i]['Staff']
                embed = discord.Embed(title=f'Ficha de {user.name}',description='```INDEX|MOTIVO|TEMPO|STAFF\n'+msg+'\n```')
                await ctx.send(embed=embed)           
        @mute.command(name='edit',aliases=['editar'])
        @commands.has_permissions(kick_members=True)
        async def edit(self,ctx,user: discord.Member=None,index=None,novomotivo='Não especificado'):
            if user == None:
                await padrao(ctx,'Moderação','edit','Serve para editar um determinado mute','```mute edit <user>* <index>* <novo_motivo>*```','```edit | editar```','Staff')
            else:
                dados = await Dados()
                if index == None or index not in dados['Servers'][str(ctx.guild.id)]['users'][str(user.id)]['fichamute']:
                    await ctx.send(":x: | **Index inválida, para saber as index válidas use o `mute list <member>`**")
                else:
                    dados['Servers'][str(ctx.guild.id)]['users'][str(user.id)]['fichamute'][index]['Motivo'] = novomotivo
                    with open('dados.json','w') as f:
                        json.dump(dados,f,indent=4)
                    await ctx.send(":question: | **Mute editado com sucesso**")
    
    bot.add_cog(warn(bot))
    bot.add_cog(unwarn(bot))
class Config(): 
    class config(commands.Cog):
        @commands.group(name='config',aliases=['cfg','configurar','cf'],invoke_without_command=True)
        async def cmdconfig(self,ctx):
            embed = discord.Embed(title='Ajuda de configuração',description="""Esse painel mostrara como usar o config, somente pessoas com a permissão "Administrador" pode usar esse comando\n \n:question: **Para que serve?**\nServe para mudar, intervalo de XP, Media de XP, Configurações de canais de MUTE, Canal de bem vindo e etc...\n\n:question: **Quais são os comandos?**\n`xp-time` -> Muda o tempo de CoolDown de XP\n`mute-role` -> Mudar o cargo de mute\n`welcome-channel` -> Muda o chat para mandar as mensagem de bem vindo\n`welcome-msg` -> Muda a mensagem de bem vindo\n`leave-msg` -> Muda a mensagem de saida do membro\n`media-xp` -> Muda a media de xp que o usuario ganha no servidor\n`autorole` -> Quando um membro entra no servidor ele dá esse cargo automaticamente\n`slowmode` -> Muda o CoolDown de mensagems do chat\n`prefix` -> Muda o prefixo do bot\n`dmpu` -> Manda a mensagem na DM do usuario que foi punido\n\n:grey_question: **Perguntas Frequentes**\n**Como eu tiro o sistema de "Bem Vindo/ AutoRole" ?** : Use o comando **del**, por exemplo "`del config welcome-channel`"\n\n**__Comandos que já tem essa função__**: \n`media-xp` <Desativa o XP por completo>\n`welcome-channel` <Desativa a mensagem de Boas Vindas por completo>\n\n**Ainda ficou com dúvida?** Entre no servidor de suporte do SphyX 'https://discord.gg/hReae7c67G'\n\n:globe_with_meridians: **Outros nomes**\n```cfg | config | configurar | cf```""")
            await ctx.send(embed=embed)            
        @cmdconfig.command(name='xp-time')
        @commands.has_permissions(kick_members=True)
        async def xp_time(self,ctx,novo_valor: int=None):
            if novo_valor == None:
                await padrao(ctx,'configuração','xp-time','Serve para mudar o tempo de cooldown para ganhar o XP','`xp-time <Novo Valor: SEGUNDOS>*` -> Muda o CoolDown de XP','```xp-time```','Staff')
                #ctx: object,nomeEmbed: str,name: str,desc: str,como: str,aliases: str,perm: str)
            else:
                dados = await Dados()
                ant = dados['Servers'][str(ctx.guild.id)]['config']['time_xp']
                dados['Servers'][str(ctx.guild.id)]['config']['time_xp'] = int(novo_valor)
                await ctx.send(f":question:  | **Tempo de CoolDown alterado para {novo_valor}!**")
                dados['Servers'][str(ctx.guild.id)]['contIDreg'] += 1
                cont = dados['Servers'][str(ctx.guild.id)]['contIDreg']
                dados['Servers'][str(ctx.guild.id)]['reg'][cont] = {
                            'tipo':'XP_TIME',
                            'anVal':ant,
                            'dpVal':int(novo_valor),
                            'QmMd':ctx.author.name 
                }
                with open('dados.json','w') as f:
                    json.dump(dados,f,indent=4)
                    global log
                    log = log + "\n" + f"XP_TIME alterado para {novo_valor} no servidor {ctx.guild.name}"
        @cmdconfig.command(name='mute-role')
        @commands.has_permissions(kick_members=True)
        async def mute_role(self,ctx,novo_cargo: discord.Role=None):
            if novo_cargo == None:
                await padrao(ctx,'configuração','mute-role','Serve para mudar o cargo de mute do servidor','`mute-role <Novo Valor: CARGO>*` -> Muda o cargo de mute','```mute-role```','Staff')
                #ctx: object,nomeEmbed: str,name: str,desc: str,como: str,aliases: str,perm: str)
            else:
                dados = await Dados()
                ant = dados['Servers'][str(ctx.guild.id)]['config']['role_mute']
                dados['Servers'][str(ctx.guild.id)]['config']['role_mute'] = int(novo_cargo.id)
                await ctx.send(f":question:  | **Cargo de mute foi mudado para: {novo_cargo}!**")
                dados['Servers'][str(ctx.guild.id)]['contIDreg'] += 1
                cont = dados['Servers'][str(ctx.guild.id)]['contIDreg']
                dados['Servers'][str(ctx.guild.id)]['reg'][cont] = {
                            'tipo':'MUTE_ROLE',
                            'anVal':ant,
                            'dpVal':int(novo_cargo.id),
                            'QmMd':ctx.author.name 
                }
                with open('dados.json','w') as f:
                    json.dump(dados,f,indent=4)
                    global log
                    log = log + "\n" + f"MUTE_ROLE Alterado para {novo_cargo.name} no servidor {ctx.guild.name}"
        @cmdconfig.command(name='welcome-msg')
        @commands.has_permissions(kick_members=True)
        async def welcome_msg(self,ctx,*,novo_valor: str=None):
            if novo_valor == None:
                #ctx: object,nomeEmbed: str,name: str,desc: str,como: str,aliases: str,perm: str) 
                embed = discord.Embed(title='Ajuda de configuração',description='Esse painel mostrara como usar o welcome-msg, somente pessoas com a permissão "Administrador" pode usar esse comando\n\n :question:  **Para que serve?**\n\nServe para mudar a mensagem de boas vindas!\n\n\n :question: **Quais são os comandos?**\n\n`welcome-msg <nova mensagem>`\n\n:newspaper: **Guia**\n[mention] -> Menciona o usuario na mensagem\n[user] -> Coloca o nome do usuario (sem marcar)\n[usertag] -> Coloca o nome do usuario junto com a tag EX: NightterX#0311\n[guildname] -> Coloca o nome do servidor\n\n :globe_with_meridians: **Outros nomes**\n\n ```welcome-msg```')
                await ctx.send(embed=embed)
            else:
                dados = await Dados()
                member = ctx.author
                ant = dados['Servers'][str(ctx.guild.id)]['config']['WelcomeMsg']
                dados['Servers'][str(ctx.guild.id)]['config']['WelcomeMsg'] = novo_valor
                dados['Servers'][str(ctx.guild.id)]['contIDreg'] += 1
                cont = dados['Servers'][str(ctx.guild.id)]['contIDreg']
                dados['Servers'][str(ctx.guild.id)]['reg'][cont] = {
                            'tipo':'WELCOME_MESSAGE',
                            'anVal':ant,
                            'dpVal':novo_valor,
                            'QmMd':ctx.author.name 
                }
                with open('dados.json','w') as f:
                    json.dump(dados,f,indent=4)
                    global log
                    log = log + "\n" + f"WELCOME_MESSAGE Alterado para {novo_valor} no servidor {ctx.guild.name}"
                mensagem = dados['Servers'][str(member.guild.id)]['config']['WelcomeMsg']
                mensagem = mensagem.replace('[mention]',member.mention)
                mensagem = mensagem.replace('[user]',member.name)
                mensagem = mensagem.replace('[usertag]',member.name + '#' + member.discriminator)
                mensagem = mensagem.replace('[guildname]',member.guild.name)
                await ctx.send(f":question:  | **A mensagem de boas vindas foi mudado para: {novo_valor}!\nSua mensagem ficou assim: {mensagem}**")
        @cmdconfig.command(name='leave-msg')
        @commands.has_permissions(kick_members=True)
        async def leave_msg(self,ctx,*,novo_valor: str=None):
            if novo_valor == None:
                #ctx: object,nomeEmbed: str,name: str,desc: str,como: str,aliases: str,perm: str) 
                embed = discord.Embed(title='Ajuda de configuração',description='Esse painel mostrara como usar o leave-msg, somente pessoas com a permissão "Administrador" pode usar esse comando\n\n :question:  **Para que serve?**\n\nServe para mudar a mensagem de boas vindas!\n\n\n :question: **Quais são os comandos?**\n\n`leave-msg <nova mensagem>`\n\n:newspaper: **Guia**\n[mention] -> Menciona o usuario na mensagem\n[user] -> Coloca o nome do usuario (sem marcar)\n[usertag] -> Coloca o nome do usuario junto com a tag EX: NightterX#0311\n[guildname] -> Coloca o nome do servidor\n\n :globe_with_meridians: **Outros nomes**\n\n ```leave-msg```')
                await ctx.send(embed=embed)
            else:
                dados = await Dados()
                member = ctx.author
                ant = dados['Servers'][str(ctx.guild.id)]['config']['LeaveMsg']
                dados['Servers'][str(ctx.guild.id)]['config']['LeaveMsg'] = novo_valor
                dados['Servers'][str(ctx.guild.id)]['contIDreg'] += 1
                cont = dados['Servers'][str(ctx.guild.id)]['contIDreg']
                dados['Servers'][str(ctx.guild.id)]['reg'][cont] = {
                            'tipo':'LEAVE_MESSAGE',
                            'anVal':ant,
                            'dpVal':novo_valor,
                            'QmMd':ctx.author.name 
                }
                with open('dados.json','w') as f:
                    json.dump(dados,f,indent=4)
                    global log
                    log = log + "\n" + f"LEAVE_MESSAGE Alterado para {novo_valor} no servidor {ctx.guild.name}"
                mensagem = dados['Servers'][str(member.guild.id)]['config']['LeaveMsg']
                mensagem = mensagem.replace('[mention]',member.mention)
                mensagem = mensagem.replace('[user]',member.name)
                mensagem = mensagem.replace('[usertag]',member.name + '#' + member.discriminator)
                mensagem = mensagem.replace('[guildname]',member.guild.name)
                await ctx.send(f":question:  | **A mensagem de saida foi mudado para: {novo_valor}!\nSua mensagem ficou assim: {mensagem}**")
        @cmdconfig.command(name='welcome-channel')
        @commands.has_permissions(kick_members=True)
        async def welcome_channel(self,ctx,novo_canal: discord.TextChannel=None):
            if novo_canal == None:
                await padrao(ctx,'Moderação','welcome-channel','Muda o canal que o bot manda a mensagem de boas vindas! Caso não queira mais mensagems de boas vindas, só não faça nada','`welcome-channel <canal de texto>*` -> Muda o canal de boas vindas','welcome-channel','Staff')       
            else:
                dados = await Dados()
                ant = dados['Servers'][str(ctx.guild.id)]['config']['welcome_channel']
                dados['Servers'][str(ctx.guild.id)]['config']['welcome_channel'] = int(novo_canal.id)
                dados['Servers'][str(ctx.guild.id)]['contIDreg'] += 1
                cont = dados['Servers'][str(ctx.guild.id)]['contIDreg']
                dados['Servers'][str(ctx.guild.id)]['reg'][cont] = {
                            'tipo':'WELCOME_CHANNEL',
                            'anVal':ant,
                            'dpVal':novo_canal.id,
                            'QmMd':ctx.author.name 
                }
                with open('dados.json','w') as f:
                    json.dump(dados,f,indent=4)
                    global log
                    log = log + "\n" + f"WELCOME_CHANNEL Alterado para {novo_canal.name} no servidor {ctx.guild.name}"
                await ctx.send(f":question:  | **Canal alterado para {novo_canal}**")
        @cmdconfig.command(name='media-xp')
        @commands.has_permissions(kick_members=True)
        async def media_xp(self,ctx,novo_valor=None):
            if novo_valor == None:
                await padrao(ctx,'Moderação','media-xp','Muda a media de Xp que o usuario ganha no servidor','`media-xp <xp>*` -> Muda a media de xp','media-xp','Staff')       
            else:
                dados = await Dados()
                ant = dados['Servers'][str(ctx.guild.id)]['config']['mediaxp']
                dados['Servers'][str(ctx.guild.id)]['config']['mediaxp'] = int(novo_valor)
                dados['Servers'][str(ctx.guild.id)]['contIDreg'] += 1
                cont = dados['Servers'][str(ctx.guild.id)]['contIDreg']
                dados['Servers'][str(ctx.guild.id)]['reg'][cont] = {
                            'tipo':'AVERAGE_XP',
                            'anVal':ant,
                            'dpVal':novo_valor,
                            'QmMd':ctx.author.name 
                }
                with open('dados.json','w') as f:
                    json.dump(dados,f,indent=4)
                    global log
                    log = log + "\n" + f"AVERAGE_XP Alterado para {novo_valor} no servidor {ctx.guild.name}"
                await ctx.send(f":question:  | **A Media de XP foi alterada para {novo_valor}**")
        @cmdconfig.command(name='slowmode',aliases=['slow','cd','cooldown'])
        @commands.has_permissions(kick_members=True)
        async def slowmode(self,ctx,chat: discord.TextChannel=None,tempo=0):
            if chat == None:
                await padrao(ctx,'Moderação','slowmode','Muda o tempo de cooldown de um chat em especifico sem limites','`slowmode <chat>* tempo*` -> Muda o tempo de CoolDown de um chat','``` slowmode | slow | cd | cooldown```','Staff')
                #ctx: object,nomeEmbed: str,name: str,desc: str,como: str,aliases: str,perm: str)
    
            else:
                await chat.edit(slowmode_delay = int(tempo))
                dados = await Dados()
                cont = dados['Servers'][str(ctx.guild.id)]['contIDreg']
                dados['Servers'][str(ctx.guild.id)]['reg'][cont] = {
                            'tipo':'SLOWMODE_CHANGE',
                            'dpVal':int(tempo),
                            'QmMd':ctx.author.name 
                }
                with open("dados.json",'w') as f:
                    json.dump(dados,f,indent=4)
                await ctx.send(f":question:  | **O CoolDown do chat {chat} foi alterado para {tempo}**")
                global log
                log = log + "\n" + f"SLOWMODE Alterado para {tempo} no servidor {ctx.guild.name}"
        @cmdconfig.command(name='prefix',aliases=['prefixo'])
        @commands.has_permissions(kick_members=True)
        async def prefix(self,ctx,prefix=None):
            if prefix != None:
                dados = await Dados()
                
                if prefix == dados['Servers'][str(ctx.guild.id)]['config']['prefix']:
                    await ctx.send(":warning: | **Já tem esse prefixo**")
                else:
                    dados['Servers'][str(ctx.guild.id)]['config']['prefix'] = prefix
                    cont = dados['Servers'][str(ctx.guild.id)]['contIDreg']
                    dados['Servers'][str(ctx.guild.id)]['reg'][cont] = {
                            'tipo':'PREFIX_CHANGE',
                            'dpVal':prefix,
                            'QmMd':ctx.author.name 
                }
                    with open("dados.json",'w')as f:
                        json.dump(dados,f,indent=4)
                        global log
                        log = log + "\n" + f"AVERAGE_XP Alterado para {prefix} no servidor {ctx.guild.name}"
                    await ctx.send(f":question: | **Prefixo alterado para \"{prefix}\" **")
            else:
                await padrao(ctx,"Moderação",'prefix','Muda o prefixo do bot do servidor! Mude para oque quiser letras e etc...','`prefix <novo prefixo>*`  ','```prefix | prefixo```','Staff')
        @cmdconfig.group(name='autorole',invoke_without_command=True)
        @commands.has_permissions(kick_members=True)
        async def cmdautorole(self,ctx,role: discord.Role=None):
                await padrao(ctx,'Moderação','autorole','Da um cargo automatico quando a pessoa entra no servidor','`add <cargo>*` -> Muda o cargo de Autorole\n`edit <index> <cargo>* <novo index>` -> Edita a posição do cargo\n`list` -> lista todos as autoroles','```autorole```','Staff')
        @cmdautorole.command(name='add',aliases=['adicionar'])
        @commands.has_permissions(kick_members=True)
        async def add(self,ctx,role: discord.Role=None):
            if role == None:
                await padrao(ctx,'Moderação','add autorole','Serve para adicionar um cargo automatico!','`add <cargo>*` -> Adiciona um cargo no autorolelist','```add```',"Staff")
            else:
                dados = await Dados()
                dados["Servers"][str(ctx.guild.id)]['config']['controle'] += 1
                cont = dados["Servers"][str(ctx.guild.id)]['config']['controle']
                dados["Servers"][str(ctx.guild.id)]['config']['autorole'][str(cont)] = {
                    'roleid':role.id
                }
                cont = dados['Servers'][str(ctx.guild.id)]['contIDreg']
                dados['Servers'][str(ctx.guild.id)]['reg'][cont] = {
                            'tipo':'AUTOROLE_CHANGE',
                            'dpVal':role.id,
                            'QmMd':ctx.author.name 
                }
                with open("dados.json",'w') as f:
                    json.dump(dados,f,indent=4)
                await ctx.send(":question: | **Um cargo de autorole foi adicionado**")
        @cmdautorole.command(name='edit',aliases=['editar'])
        @commands.has_permissions(kick_members=True)
        async def edit(self,ctx,index=None,novo_index=None):
            if index == None:
                await padrao(ctx,'Moderação','edit autorole','Edita uma posição de um autorole','`edit <index>* <novo index>*` -> Edita a posição de um autorole',"```edit | editar```",'staff')
            else:
                dados = await Dados()
                try:
                    ant = dados['Servers'][str(ctx.guild.id)]['config']['autorole'][index]
                    val = dados['Servers'][str(ctx.guild.id)]['config']['autorole'][novo_index]
                    dados['Servers'][str(ctx.guild.id)]['config']['autorole'][novo_index] = dados['Servers'][str(ctx.guild.id)]['config']['autorole'][index].pop(index)
                    dados['Servers'][str(ctx.guild.id)]['config']['autorole'][novo_index] = ant
                    dados['Servers'][str(ctx.guild.id)]['config']['autorole'][index] = val
                except IndexError:
                    await ctx.send(":x: | **Index inválida**")
        @cmdautorole.command(name='list',aliases=['listar'])
        @commands.has_permissions(kick_members=True)
        async def list(self,ctx):
            dados = await Dados()
            msg=""
            for i in dados["Servers"][str(ctx.guild.id)]["config"]['autorole']:
                role = ctx.guild.get_role(dados["Servers"][str(ctx.guild.id)]["config"]['autorole'][str(i)]['roleid'])
                msg = msg + "\n" + str(i) +"  -  "+  role.name
            embed=discord.Embed(title='Lista do AutoRole',description='Aqui vai mostrar todos os cargos em ordem que estão no seu autorole')
            embed.add_field(name='INDEX    |     CARGO  ',value=f'```\n{msg}```')
            embed.set_footer(text='Quer algo mais detalhado? Tente usar o "config autorole preview',icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        @cmdautorole.command(name='remove',aliases=['remover'])
        @commands.has_permissions(kick_members=True)
        async def remover(self,ctx,index=None):
            if index == None:
                await padrao(ctx,'Moderação','autorole remove','Serve para tirar um cargo de um autorole, coloque o index do cargo que você quer remover e pronto!','`autorole remove <index autorole>`','```remove | remover```','Staff')
            else:
                dados = await Dados()
                try:
                    ant = dados['Servers'][str(ctx.guild.id)]['config']['autorole'][index]['roleid']
                    del dados['Servers'][str(ctx.guild.id)]['config']['autorole'][index]
                except KeyError:
                    await ctx.send(":x: | **Você colocou um Index inválido, para saber os index de cada cargo use o \"config autorole list\"**")    
                    return
                with open('dados.json','w') as f:
                    json.dump(dados,f,indent=4)
                role = ctx.guild.get_role(ant)
                await ctx.send(f":question: | **Pronto! O Cargo {role.name}**")
        @cmdconfig.command(name='des',aliases=['desativar','del'])
        @commands.has_permissions(kick_members=True)
        async def des(self,ctx,tipo=None):
            if tipo == None:
                await padrao(ctx,'Moderação','des','Desativa uma função do bot, seja ele autorole, mensagems de boas vindas e entre outros...','`des <tipo>*` -> Desativa a função de acordo com o tipo que você digitou!\n**Tipos existentes**\nwelcome-channel -> Desativa as mensagems de boas vindas\nautorole -> Desativa o autorole\nmedia-xp -> Desativa o xp','```des | desativiar | del```','Staff')
            else:
                tipo = tipo.replace("-","_")
                dados = await Dados()
                if not tipo in dados['Servers'][str(ctx.guild.id)]['config']:
                    await ctx.send(":x: | **Tipo invalido!**")
                else:
                    dados['Servers'][str(ctx.guild.id)]['config'][tipo] = 0
                    await ctx.send(f":question:  | **A função {tipo} foi desativado(a)**")
                with open('dados.json','w') as f:
                    json.dump(dados,f,indent=4)
        @cmdconfig.command(name='dmpu')
        @commands.has_permissions(kick_members=True)
        async def dmpu(self,ctx,tipo=None):
            if tipo == None:
                await padrao(ctx,'Moderação','dmpu','Quando ativado o usuario que levou algum tipo de punição por exemplo Warn, o bot vai diretamente no DM dele avisar','`dmpu ativar ou desativar` -> Desativa ou Ativa a mensagem de punição na DM','```dmpu```','Staff')
            else: 
                tipo = tipo.lower()
                dados = await Dados()
                if tipo == 'Ativar':
                    dados['Servers'][str(ctx.guild.id)]['config']['dmpu'] = 1
                    await ctx.send(":question: | **Mensagems de punição na DM foram ativados**")
                elif tipo == 'Desativar':
                    dados['Servers'][str(ctx.guild.id)]['config']['dmpu'] = 0
                    await ctx.send(":question: | **Mensagems de punição na DM foram desativados**")
                else:
                    await ctx.send(":x: | **Use `ativar` ou `desativar`**")
                with open('dados.json','w') as f:
                    json.dump(dados,f,indent=4)
    bot.add_cog(config(bot))
            
    

bot.run(token.token())