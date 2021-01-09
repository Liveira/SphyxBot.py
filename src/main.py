import asyncio
from io import BytesIO
from json import decoder
from operator import iand
from random import randrange
import time
from discord.errors import HTTPException
from discord.ext.commands.cooldowns import BucketType
from mal import *
import requests
import subprocess
from osuapi import OsuApi, ReqConnector
import discord,json,datetime,random,os,textwrap
from PIL import Image as img, ImageDraw
from PIL import ImageFont as imgfont
from PIL import ImageDraw as imgdraw
from PIL import ImageOps
from discord.ext import commands
from discord.ext.commands.errors import CommandInvokeError, MemberNotFound, RoleNotFound
from discord.flags import Intents
from dpymenus import Page, PaginatedMenu
from requests.api import request
import base64
import dbl
import pyshorteners
import qrcode,pymongo
intents = intents = discord.Intents.all()
log = ""
ultimafoto={}
vargv={}
dtemp={}
cl = pymongo.MongoClient('##')
db = cl['Usuarios']
users = db['Users']
servers = db['Servers']
devs=[437679061251391488,236248595051839488,563448056125587457,471698795189764096,638020094076649493,685635634316312597]
def check(author,messagecheck):
    def inner_check(message):
        if message.author == author:
            if message.content.lower() == messagecheck or message.content.lower() in messagecheck: return True
            else: return False
    return inner_check
verif={
    "none":"Fraco",
    "medium":"Medio",
    "high":"Alto",
    "table_flip":"Alto (╯°□°）╯︵ ┻━┻ ",
    "extreme" : "ExTrEmO",
    "double_table_flip":"EXTREMO",
    "very_high":"Extremo"
}
osu = OsuApi("##", connector=ReqConnector())
def prefix(bot,message):
    ca = ''
    with open('dados.json','r') as f:
        ca = json.load(f)
    return ca[str(message.guild.id)]
bot = commands.Bot(command_prefix='.',case_insensitive=True,intents=intents)
bot.remove_command('help')
epoch = datetime.datetime.utcfromtimestamp(0)
class token():
    def token():
        bottoken='##'
        return bottoken
@bot.event
async def on_ready():
    await outroloop()
async def padrao(ctx: object,nomeEmbed: str,name: str,desc: str,como: str,aliases: str,perm: str) -> None:
    if perm == "Staff":
        embed = discord.Embed(title=f'Ajuda de {nomeEmbed}',description=f'Esse painel mostrara como usar o {name}, somente a Staff podem usar esse comando\n\n :question:  **Para que serve?**\n\n {desc}\n\n\n :question: **Quais são os comandos?**\n\n {como} \n\n** :globe_with_meridians: Outros nomes**\n {aliases}')
    else:
        embed = discord.Embed(title=f'Ajuda de {nomeEmbed}',description=f'Esse painel mostrara como usar o {name}, todos podem usar esse comando\n\n :question:  **Para que serve?**\n\n {desc}\n\n\n :question: **Quais são os comandos?**\n\n {como} \n\n** :globe_with_meridians: Outros nomes**\n {aliases}')
    await ctx.send(embed=embed)
async def salvar(dados):
    sets = {"$set":dados}
    users.update_one(users.find_one(),sets)
async def salvarS(dados):
    sets = {"$set":dados}
    servers.update_one(servers.find_one(),sets)
async def Dados() -> json:
    return servers.find_one()
async def UDados() -> json:
    return users.find_one()
async def CConta(user: discord.Member):
    dados = await UDados()
    if str(user.id) in dados['Users']:
        return
    else:
        if user.bot == True:
            return
        dados['Users'][str(user.id)] = {'nome':user.name,'desc':'Eu sou uma pessoa misteriosa, mas eu posso mudar minha descrição usando .desc','rep':0,"xp_time":0,'money':0,'gold':0,'inventory':{"Padrão": {"name": "Padrão","desc": "Background padrão","tip": "BackGround Profile","use": True,"cont": 0,"onetime": True,"preview": "https://media.discordapp.net/attachments/776197504378732555/795800876383338496/default.png?width=642&height=459","tipte": "back-pf","author": "SphyX Team"}},'profile':{'back-pf':{'url':'https://media.discordapp.net/attachments/776197504378732555/795800876383338496/default.png?width=642&height=459','name':"Padrão"}}}
    await salvar(dados)
async def GCConta(guild: discord.Guild):
    dados = await Dados()
    if str(guild.id) in dados["Servers"]:
        return
    else:
        a = ''
        with open('dados.json') as f:
            a = json.load(f)
        dados['Servers'][str(guild.id)] = {'users':{},'config':{'time_xp':30,'role_mute':0,'welcome_channel':0,'mediaxp':10,'WelcomeMsg':' Bem vindo! ','LeaveMsg':'Saiu do servidor!','dmpu':0,'autorole':{},'controle':0,'rr':{},'rrcont':0},'reg':{},'contIDreg':0,'automessage':0,'tick':{}}
        a[str(guild.id)] = "."
        with open('dados.json','w') as f:
            json.dump(a,f)
    await salvarS(dados)
async def loop():
    while True:
        await asyncio.sleep(60)
        dados = await Dados()
        udados = await UDados()
        cont=0
        contU=0
        contD=0
        async for guild in bot.fetch_guilds(limit=None):
            cont+=1
            if str(guild.id) not in dados['Servers']:
                await GCConta(guild)
                dados = await Dados()
            async for member in guild.fetch_members(limit=None): 
                if str(member.id) not in dados['Servers'][str(guild.id)]['users']:
                    contD+=1
                    dados['Servers'][str(guild.id)]['users'][str(member.id)] = {'warns':0,'ficha':{},'fichamute':{},'contmute':0,'xp':0,'msg':0,'xp_time':0} 
                if str(member.id) not in udados['Users']:
                    contU += 1      
                    if member.bot == True:
                        pass
                    else:
                        await CConta(member)
            await salvarS(dados)
        global log
        log = log + "\n" + '------------------'
        log = log + "\n" + f"[{str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))}]\n"
        log = log + "\n" + f"Foi registrado: {contU} contas"
        log = log + "\n" + f"Foi registrado: {contD} contas de {cont} Servidores"
        log = log + "\n" + '------------------\n\n'
async def outroloop():

    while True:
        global log
        await asyncio.sleep(20000)
        f = open(f"logs/{str(time.strftime('%Y-%m-%d %H-%M-%S', time.localtime()))}.txt","x")
        with open(f.name,"w") as f:
            f.write(log)
        file = discord.File(open(f.name,'rb'))
        channel = bot.get_channel(785611411043647578)
        await channel.send(file=file)
        log = ""
class events(commands.Cog):
    @commands.Cog.listener()
    async def on_ready(self):
        print('.................')
        print('Sphyx está ligado!')
        print('.................')
        print('       LOG       ')
        print('                 ')
        await bot.change_presence(activity=discord.Game(name=f".help | Eu estou em {len(bot.guilds)} servidores e {len(bot.users)} Usuários!", type=1))
        await loop()  
    @commands.Cog.listener()
    async def on_message(self,message):
        try:
            global ultimafoto
            yeah = message.attachments
            try:
                if yeah[0].size > 0:
                    ultimafoto[message.guild.id]= yeah
            except IndexError:
                pass
        except TypeError as error:
            print(error)
        if message.author.bot != True:
            dados = await Dados()
            dadosU = await UDados()
            var = None
            with open('dados.json','r') as f:
                var = json.load(f)
            config = dados['Servers'][str(message.guild.id)]['config']
            if  message.content == f"<@!{bot.user.id}>":
                await message.channel.send(f":question: | `{var[str(message.guild.id)]}help` **<- Comando de ajuda**")
            xp = dados['Servers'][str(message.guild.id)]['users'][str(message.author.id)]['xp']
            dados['Servers'][str(message.guild.id)]['users'][str(message.author.id)]['msg'] += 1
            user = message.author
            if user.id in dadosU:
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
        lo = await guild.audit_logs(action=discord.AuditLogAction.bot_add).flatten()
        use = lo[0].user
        print(use)
        await use.send("Obrigado por me adicionar!\n\nEu tenho algumas informações que podem ser úteis para você, caso queira configurar o seu servidor você usa o comando `.config` que ele vai listar todos os comandos e como usar cada um, enfim muito obrigado por me adicionar!\n\nVocê pode tentar ir no meu discord oficial! -> https://discord.gg/CG7spnTsKa \nOu ver os meus comandos -> https://tinyurl.com/y99phkrp")
        print('SphyX Entrou em ' + guild.name)
        owner = bot.fetch_user(guild.owner_id)
        dados = await Dados()
        userdata = await UDados()
        cont=0
        user={}
        if str(guild.id) in dados['Servers']:
            return
        await GCConta(guild)
        async for i in guild.fetch_members(limit=None):
            if i.bot != True:
                dados['Servers'][str(guild.id)]['users'][str(i.id)] = {'warns':0,'ficha':{},'fichamute':{},'contmute':0,'xp':0,'msg':0,'xp_time':0}
                print(dados['Servers'][str(guild.id)]['users'][str(i.id)])
                if str(user.id) in userdata['Users']:
                    return
                else:
                    if user.bot == True:
                        pass
                    else:
                        userdata['Users'][str(user.id)] = {'nome':user.name,'desc':'Eu sou uma pessoa misteriosa, mas eu posso mudar minha descrição usando .desc','rep':0,"xp_time":0,'money':0,'gold':0,'inventory':{"Padrão": {"name": "Padrão","desc": "Background padrão","tip": "BackGround Profile","use": True,"cont": 0,"onetime": True,"preview": "https://media.discordapp.net/attachments/776197504378732555/795800876383338496/default.png?width=642&height=459","tipte": "back-pf","author": "SphyX Team"}},'profile':{'back-pf':{'url':'https://media.discordapp.net/attachments/776197504378732555/795800876383338496/default.png?width=642&height=459','name':"Padrão"}}}
        with open('dados.json','w') as f:
            json.dump(dados,f,indent=4)
        with open('users.json','w') as f:
            json.dump(userdata,f,indent=4)
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
        dados['Servers'][str(member.guild.id)]['users'][str(member.id)] = {'warns':0,'ficha':{},'fichamute':{},'contmute':0,'xp':0,'msg':0,'xp_time':0} 
        if dados['Servers'][str(member.guild.id)]['config']['automessage'] != 0:
            mensagem = dados['Servers'][str(member.guild.id)]['config']['automessage']
            mensagem = mensagem.replace('[mention]',member.mention)
            mensagem = mensagem.replace('[user]',member.name)
            mensagem = mensagem.replace('[usertag]',member.name + '#' + member.discriminator)
            mensagem = mensagem.replace('[guildname]',member.guild.name)
            await member.send(f'Mensagem enviada do servidor {member.guild.name};\n'+mensagem)
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
class Moderacao():
    class warn(commands.Cog):
        @commands.group(name='warn' ,aliases=['avisar'] , invoke_without_command=True)
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
                await salvarS(dados)
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
                if index == None or index not in dados['Servers'][str(ctx.guild.id)]['users'][str(user.id)]['ficha']:
                    await ctx.send(":x: | **Index inválida, para saber as index válidas use o `warn list <member>`**")
                else:
                    dados['Servers'][str(ctx.guild.id)]['users'][str(user.id)]['ficha'][index]['Motivo'] = novomotivo
                    await salvarS(dados)

                    await ctx.send(":question: | **Warn editado com sucesso**")
        @cmdwarn.command(name='all')
        @commands.has_permissions(kick_members=True)
        async def all(self,ctx):
            dados = await Dados()
            us = dados['Servers'][str(ctx.guild.id)]['users']
            lista=[]
            do={}
            embed=None
            msg=''
            for x in us:
                if us[x]['warns'] == 0:
                    pass
                else:
                    user = bot.get_user(int(x))
                    do[us[x]['warns']] = user.name
                    lista.append(us[x]['warns'])
            lista = sorted(lista,reverse=True)
            for i in lista:
                msg = msg + '\n' + do[i] + ' - ' + str(i)      
            await ctx.send(embed=discord.Embed(title='Lista de avisos',description=f'```{msg if msg != "" else "A Lista de avisos está vazia..."}```'))
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
                    await salvarS(dados)
                    await ctx.send(f":question: | **O Aviso do usuario {user.name} foi removido!**")
                    if dados['Servers'][str(ctx.guild.id)]['users'][str(user.id)]['config']['dmpu'] == 1:
                        await user.send(":warning: | **Seu aviso foi removido**")  
                    global log
                    log = log + '\n' + f'{user.name} warn retirado no servidor {ctx.guild.name}'             
    class kick(commands.Cog):
        @commands.command(name='kick',aliases=['expulsar'])
        @commands.has_permissions(kick_members=True)
        async def kick(self,ctx,member : discord.Member=None,motivo = "Não especificado"):
            if member == None:
                await padrao(ctx,'Moderação','kick','Expulsa um membro','`.kick <user>* motivo`','```kick | expulsar```','Staff')
            else:
                await member.kick()
                dados = await Dados()
                if dados['Servers'][str(ctx.guild.id)]['config']['dmpu'] != 0:
                    await member.send(f":x: | **Você foi expulso do servidor {ctx.guild.name}, motivo: {motivo}**")                
                await ctx.guild.ban(member,reason=motivo)      
                await ctx.send(f":question: | **O Usuario {member.name} foi expulso do servidor**")
    class mute(commands.Cog):
        @commands.group(name='mute',aliases=['mutar','silenciar','tempmute'], invoke_without_command=True)
        @commands.has_permissions(kick_members=True)
        async def cmdmute(self,ctx,user: discord.Member=None,tempoMute=None,motivo='Não especificado'):
            if user == None:
                await padrao(ctx,'Moderação','mute','Serve para mutar um usuario por um determinado tempo, caso não coloque nenhum tempo o tempo vai ser automaticamente inderteminado ou permanente','`mute <user>* <tempo> <motivo>` -> Silencia um membro\n`list <user>*`','```mute | silenciar | mutar```','Staff')
                return
            elif user.top_role >= ctx.author.top_role:
                await ctx.send(":x: | **Seu cargo está abaixo do usuario**")
                return
            dados = await Dados()
            time=0
            role=None
            ant = tempoMute
            if dados['Servers'][str(ctx.guild.id)]['config']['role_mute'] == 0:
                await ctx.send(":x: | **Você não configurou o cargo de mute! Configure usando o comando** `config mute-role <cargo>`")
            else:
                role = ctx.guild.get_role(dados['Servers'][str(ctx.guild.id)]['config']['role_mute'])
            if tempoMute == None:
                pass
            else:
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
            await user.add_roles(role)
            cont=0
            await ctx.send(f":question: | **O Usuario: {user.name} foi mutado por {ant}, motivo: {motivo}**")
            if dados['Servers'][str(ctx.guild.id)]['config']['dmpu'] == 1:
                    await user.send(f"Você está **Mutado** por {ant}, motivo: {motivo}")
            dados['Servers'][str(ctx.guild.id)]['users'][str(ctx.author.id)]['warns'] += 1
            cont = dados['Servers'][str(ctx.guild.id)]['users'][str(ctx.author.id)]['warns']
            dados['Servers'][str(ctx.guild.id)]['users'][str(ctx.author.id)]['fichamute'][str(cont)] = {
                    "Motivo":motivo,
                    "tempo":ant,
                    "ID":cont,
                    "Staff":ctx.author.name
                }
            global log
            log = log + '\n' + f'{user.name} levou mute no servidor {ctx.guild.name} por o tempo {ant}, motivo: {motivo}'
            await salvarS(dados)
            await asyncio.sleep(time)        
            await user.remove_roles(role)
        @cmdmute.command(name='check',aliases=['list'])
        @commands.has_permissions(kick_members=True)
        async def check(self,ctx,user: discord.Member=None):
            if user == None:
                await padrao(ctx,'Moderação','mute check','Serve para listar todos os mutes do membro mostrando o motivo, o tempo do mute, e quem mutou!','`mute check <user>*` -> lista todos os mutes do membro','```check | list```','Staff')
            else:
                msg=''
                dados = await Dados()
                for i in dados['Servers'][str(user.guild.id)]['users'][str(user.id)]['fichamute']:
                    msg = msg + '\n' + str(dados['Servers'][str(user.guild.id)]['users'][str(user.id)]['fichamute'][i]['ID']) + ' - ' + dados['Servers'][str(user.guild.id)]['users'][str(user.id)]['fichamute'][i]['Motivo'] + ' - ' +dados['Servers'][str(user.guild.id)]['users'][str(user.id)]['fichamute'][i]['tempo']+'  -  '+ dados['Servers'][str(user.guild.id)]['users'][str(user.id)]['fichamute'][i]['Staff']
                embed = discord.Embed(title=f'Ficha de {user.name}',description='```INDEX|MOTIVO|TEMPO|STAFF\n'+msg+'\n```')
                await ctx.send(embed=embed)           
        @cmdmute.command(name='edit',aliases=['editar'])
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
                    await salvarS(dados)
                    await ctx.send(":question: | **Mute editado com sucesso**")
    class unmute(commands.Cog):
        @commands.command(name='unmute',aliases=['desmutar'])
        async def unmute(self,ctx,user: discord.Member=None):
            if user == None:
                await padrao(ctx,'Moderação','unmute','Serve para desmutar membros que já estão mutados','`unmute <user>*` -> desmuta o usuario`','```unmute | desmute```','Staff')
            else:
                dados = await Dados()
                role = ctx.guild.get_role(dados['Servers'][str(ctx.guild.id)]['config']['role_mute'])
                if role not in user.roles:
                    await ctx.send(f":x: | **{user.name} não está mutado**")
                    return
                else:
                    await user.remove_roles(role)
                    await ctx.send(f":question: | **{user.name} foi desmutado")
    class ban(commands.Cog):
        @commands.command(name='ban',aliases=['banir'])
        @commands.has_permissions(ban_members=True)
        async def ban(self,ctx,user:discord.User=None,*,motivo='Não especificado'):
            if user == None:
                await padrao(ctx,'Moderação','ban','Serve para banir membros','`ban <user>* <motivo>` -> bani um usuario do servidor','```ban | banir```','Staff')
                return
            try:
                memb = ctx.guild.get_member(user.id)
                if memb.top_role >= ctx.author.top_role:
                    await ctx.send(":x: | **Seu cargo está abaixo do usuario**")
                return
            except MemberNotFound:
                pass   
            dados = await Dados()
            try:
                del dados['Servers'][str(ctx.guild.id)]['users'][str(user.id)]
            except KeyError:
                pass
            if dados['Servers'][str(ctx.guild.id)]['config']['dmpu'] != 0:
                await user.send(f":x: | **Você foi banido do servidor {ctx.guild.name}, motivo: {motivo}**")                
            await ctx.guild.ban(user,reason=motivo) 
            await salvarS(dados)
            await ctx.send(f":question: | **O Usuario {user.name} foi banido do servidor**")
    class unban(commands.Cog):
        @commands.command(name='unban',aliases=['desbanir'])
        @commands.has_permissions(ban_members=True)
        async def unban(self,ctx,user: discord.User=None):
            if user == None:
                await padrao(ctx,'Moderação','unban','Serve para desbanir um usuario!','`unban <user>*` -> Desban em um usuario','```unban | desbanir```','Staff')
            else:
                dados = await Dados()
                await ctx.guild.unban(user)
                await ctx.send(f":question: | **O Usuario {user.name} foi desbanido**")
    class serverinfo(commands.Cog):
        @commands.command(name='serverinfo',aliases=['guildinfo'])
        async def serverinfo(self,ctx, guild: int=None):
            rol=[]
            fi=""
            if guild != None:
                guild = bot.get_guild(guild)
                if guild == None:
                    await ctx.send(":x: | **Servidor não encontrado... Talvez eu não esteja dentro do servidor :thinking: **")
                    return
                rol = guild.roles
                for i in rol:
                    fi = fi + " @" + i.name
            else:
                guild = ctx.guild
                rol = guild.roles
                for i in rol:
                    fi = fi + " " + i.mention
            bots=0
            users=0
            while True:
                async for i in guild.fetch_members(limit=None):
                    if i.bot == True:
                        bots += 1
                    else:
                        users += 1
                embed = discord.Embed(title=f'Informações do servidor {guild.name} | Pagina 1',description=f'Dono do servidor: **{guild.owner.name}**\nQuantidade total de membros: **{guild.member_count}** | Bots: **{bots}** | Humanos: **{users}**\nNivel de seguração de moderação: **{"Fraca" if guild.mfa_level == 0 else "Forte"}** | Nivel de verificação : **{verif[str(guild.verification_level)]}**\nNivel do servidor: **{guild.premium_tier}** | Quantidade de "Boosters": **{guild.premium_subscription_count}**\nCriado em **{guild.created_at.date()}**\nQuantidade de canais: **{len(guild.channels)}** | Quantidade de canais de texto: **{len(guild.text_channels)}** | Quantidade de canais de voz: **{len(guild.voice_channels)}** | Quantidade de categorias: **{len(guild.categories)}**\nQuantidade de cargos: **{len(guild.roles)}**\nRegião do servidor: {guild.region}\n')
                embed.set_thumbnail(url = guild.icon_url if guild.icon_url != "0" or 0 else None)
                embed.set_image(url=guild.banner_url if guild.banner_url != "0" or 0 else None)
                embed.set_footer(text='Digite "1" para ver mais detalhes')
                msgA = await ctx.send(embed=embed)
                try:
                    msg = await bot.wait_for('message', check=check(ctx.author,"1"), timeout=10)   
                except asyncio.TimeoutError:

                    m = await ctx.send(':x: | **Tempo Excedido**')
                    await asyncio.sleep(5)
                    await m.delete()
                    await msgA.delete()    
                    return
                if msg.content.lower() == "1":
                    await msgA.delete()
                    await msg.delete()
                    msg=""
                    for d in guild.premium_subscribers: msg = msg +"\n **"+ str(d) + '**'
                    embed = discord.Embed(title=f'Informações do servidor {guild.name} | Pagina 2',description=f'Boosters:\n{msg}')
                    embed.set_footer(text='Digite "voltar" para voltar ou "2" para avançar')
                    ma = await ctx.send(embed=embed)
                    try:
                        msg = await bot.wait_for('message', check=check(ctx.author,["voltar","2"]), timeout=10)
                        if msg.content.lower() == 'voltar':
                            pass
                        elif msg.content.lower() == '2':
                            await ma.delete()
                            await msg.delete()
                            em = ''
                            for i in guild.emojis: em = em + ' ' + str(i)
                            embed = discord.Embed(title=f'Informações do servidor {guild.name} | Pagina 3',description=f'Emojis: \n{em}')
                            embed.set_footer(text='Digite "voltar" para voltar ou digite "3" para avançar')
                            mi = await ctx.send(embed=embed)
                            try:
                                msg = await bot.wait_for('message', check=check(ctx.author,["voltar","3"]), timeout=10)
                                if msg.content.lower() == 'voltar':
                                    await msg.delete()
                                    await mi.delete()
                                    pass
                                elif msg.content.lower() == '3':
                                    await msg.delete()
                                    await mi.delete()
                                    embed = discord.Embed(title=f'Informações do servidor {guild.name} | Pagina 4',description=f'Cargos: \n{fi}')
                                    embed.set_footer(text='Digite "voltar" para voltar')
                                    mo = await ctx.send(embed=embed)
                                    try:
                                        msg = await bot.wait_for('message', check=check(ctx.author,["voltar"]), timeout=10)
                                        if msg.content.lower() == 'voltar':
                                            await msg.delete()
                                            await mo.delete()
                                            pass
                                    except asyncio.TimeoutError:
                                        m = await ctx.send(':x: | **Tempo Excedido**')
                                        await asyncio.sleep(5)
                                        await m.delete()
                                        return            

                            except asyncio.TimeoutError:
                                m = await ctx.send(':x: | **Tempo Excedido**')
                                await asyncio.sleep(5)
                                await m.delete()
                                return    
                    except asyncio.TimeoutError:
                        m = await ctx.send(':x: | **Tempo Excedido**')
                        await asyncio.sleep(5)
                        await m.delete()
                        return
    class userinfo(commands.Cog):
        @commands.command(name='userinfo',aliases=['memberinfo'])
        async def userinfo(self,ctx,user: discord.User=None):
            user = user or ctx.author
            try:
                member = ctx.guild.get_member(user.id)
                embed = discord.Embed(title=f'Informações do usuario **{str(user)}**', description=f'\nConta criada em: **{user.created_at.date()}** | Entrou no servidor em: **{member.joined_at.date()}** | Booster desde: **{"Nunca" if member.premium_since == None else member.premium_since.date()}**\nID Do usuario `{user.id}` | Tag: **{user.discriminator}** | Apelido: **{member.display_name}**\n')  
            except MemberNotFound:                
                embed = discord.Embed(title=f'Informações do usuario {str(user)}', description=f'\nConta criada em: {user.created_at.date()}\n ID: `{user.id}`\n')  
            embed.set_thumbnail(url=user.avatar_url)  
            await ctx.send(embed=embed)
        @userinfo.error
        async def userinfo_error(self ,ctx , error):
            if isinstance(error, MemberNotFound):
                await ctx.send(":x: | **Membro não encontrado**")   
    class ticket(commands.Cog):
        @commands.command(name='ticket',aliases=['tick'])
        @commands.has_permissions(kick_members=True)
        async def ticket(self,ctx,canal: discord.TextChannel=None,idmensagem: int=None):
            print(canal)
            print(idmensagem)

            if canal == None or idmensagem == None:
                await ctx.send(":x: | **Para criar um sistema de tickets informe o canal de texto onde tem a mensagem e o id da mensagem para eu reagir e assim ativando o sistema de tickets**")
            else:
                msg = await canal.fetch_message(idmensagem)
                await msg.add_reaction('📤')
                dados = await Dados()
                dados['Servers'][str(ctx.guild.id)]["tick"][idmensagem] = True
                await salvarS(dados)
        @commands.Cog.listener()
        async def on_raw_reaction_add(self, payload):
            channel = await bot.fetch_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            user = await message.guild.fetch_member(payload.user_id)
            if user.bot == True:return
            emojiA = payload.emoji
            dados = await Dados()
            if str(message.id) in dados['Servers'][str(message.guild.id)]['tick']:
                if dados['Servers'][str(message.guild.id)]['tick'][str(message.id)]:
                    overwrites = {
                        message.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                        user: discord.PermissionOverwrite(read_messages=True)
                    }
                    ch = await message.guild.create_text_channel("tick-"+str(user),overwrites=overwrites)
                    await ch.send(f":white_check_mark: | **{user.mention}, você abriu um ticket espere uma pessoa responder ao seu pedido!**")
        @commands.command(name='close',aliases=['fechar','close_request'])
        @commands.has_permissions(kick_members=True)
        async def close_request(self,ctx,user: discord.Member=None):
            if user == None:
                await ctx.send(":x: | **Informe o membro do ticket para fechar**")
            else:
                dados = await Dados()
                print(f'tick-{str(user).replace("#","").lower()}')
                ch = discord.utils.get(ctx.guild.channels, name='tick-'+str(user).replace('#','').lower())
                if ch == None:
                    await ctx.send(":x: | **Algo deu errado... Verifique se você usou o comando corretamente**")
                await ch.delete()
                await ctx.send(':white_check_mark: | **Pronto!**')
    class botinfo(commands.Cog):
        pass
    class nuke(commands.Cog):
        @commands.command(name='nuke')
        async def nuke(self,ctx,ch: discord.TextChannel=None):
            if ch == None:
                await ctx.send(":x: | **Você esqueceu de informar o canal de texto**")
                return
            embed = discord.Embed(title='Verificação',description=f'**Você tem certeza disso?** Se sim reaja :white_check_mark: caso o contrario reaja ❎\n\nPense bem, caso de o nuke **TODAS** as mensagens serão apagadas junto com os {len(await ch.pins())} Pins...')
            msg = await ctx.send(embed=embed)
            await msg.add_reaction("✅")
            await msg.add_reaction("❎")
            def checkr(reaction,user):
                    return user == ctx.message.author and reaction.emoji in ['✅','❎']
            try:
                reac,user = await bot.wait_for('reaction_add',check=checkr,timeout=60)
                if reac.emoji == '❎':
                    await ctx.send("Nuke cancelado...")
                    return
                else:
                    await ctx.send("5 SEGUNDOS")
                    await asyncio.sleep(1)
                    await ctx.send("4 SEGUNDOS")
                    await asyncio.sleep(1)
                    await ctx.send("3 SEGUNDOS")
                    await asyncio.sleep(1)
                    await ctx.send("2 SEGUNDOS")
                    await asyncio.sleep(1)
                    await ctx.send("1 SEGUNDO")
                    a = await ch.clone()
                    await a.edit(position=ch.position)
                    await ch.delete()
                    await a.send('First!')
            except asyncio.TimeoutError:
                await ctx.send(':x: | **Tempo esgotado**')
    bot.add_cog(warn(bot))
    bot.add_cog(nuke(bot))
    bot.add_cog(ticket(bot))
    bot.add_cog(unwarn(bot))
    bot.add_cog(mute(bot))
    bot.add_cog(unmute(bot))    
    bot.add_cog(ban(bot))
    bot.add_cog(userinfo(bot))
    bot.add_cog(serverinfo(bot))
    bot.add_cog(unban(bot))
class Config(): 
    class config(commands.Cog):
        @commands.group(name='config',aliases=['cfg','configurar','cf'],invoke_without_command=True)
        async def cmdconfig(self,ctx):
            embed = discord.Embed(title='Ajuda de configuração',description="""Esse painel mostrara como usar o config, somente pessoas com a permissão "Administrador" pode usar esse comando\n \n:question: **Para que serve?**\nServe para mudar, intervalo de XP, Media de XP, Configurações de canais de MUTE, Canal de bem vindo e etc...\n\n:question: **Quais são os comandos?**\n`xp-time` -> Muda o tempo de CoolDown de XP\n`mute-role` -> Mudar o cargo de mute\n`welcome-channel` -> Muda o chat para mandar as mensagem de bem vindo\n`welcome-msg` -> Muda a mensagem de bem vindo\n`leave-msg` -> Muda a mensagem de saida do membro\n`media-xp` -> Muda a media de xp que o usuario ganha no servidor\n`autorole` -> Quando um membro entra no servidor ele dá esse cargo automaticamente\n`slowmode` -> Muda o CoolDown de mensagems do chat\n`prefix` -> Muda o prefixo do bot\n`dmpu` -> Manda a mensagem na DM do usuario que foi punido\n`automessage` -> quando um usuario entra no servidor essa mensagem vai ser enviada no DM automaticamente do membro\n\n:grey_question: **Perguntas Frequentes**\n**Como eu tiro o sistema de "Bem Vindo/ AutoRole" ?** : Use o comando **del**, por exemplo "`del config welcome-channel`"\n\n**__Comandos que já tem essa função__**: \n`media-xp` <Desativa o XP por completo>\n`welcome-channel` <Desativa a mensagem de Boas Vindas por completo>\n\n**Ainda ficou com dúvida?** Entre no servidor de suporte do SphyX 'https://discord.gg/hReae7c67G'\n\n:globe_with_meridians: **Outros nomes**\n```cfg | config | configurar | cf```""")
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
                dados['Servers'][str(ctx.guild.id)]['reg'][str(cont)] = {
                            'tipo':'XP_TIME',
                            'anVal':ant,
                            'dpVal':int(novo_valor),
                            'QmMd':ctx.author.name 
                }
                await salvarS(dados)
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
                dados['Servers'][str(ctx.guild.id)]['reg'][str(cont)] = {
                            'tipo':'MUTE_ROLE',
                            'anVal':ant,
                            'dpVal':int(novo_cargo.id),
                            'QmMd':ctx.author.name 
                }
                await salvarS(dados)
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
                dados['Servers'][str(ctx.guild.id)]['reg'][str(cont)] = {
                            'tipo':'WELCOME_MESSAGE',
                            'anVal':ant,
                            'dpVal':novo_valor,
                            'QmMd':ctx.author.name 
                }
                await salvarS(dados)
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
                dados['Servers'][str(ctx.guild.id)]['reg'][str(cont)] = {
                            'tipo':'LEAVE_MESSAGE',
                            'anVal':ant,
                            'dpVal':novo_valor,
                            'QmMd':ctx.author.name 
                }
                await salvarS(dados)
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
                dados['Servers'][str(ctx.guild.id)]['reg'][str(cont)] = {
                            'tipo':'WELCOME_CHANNEL',
                            'anVal':ant,
                            'dpVal':novo_canal.id,
                            'QmMd':ctx.author.name 
                }
                await salvarS(dados)
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
                dados['Servers'][str(ctx.guild.id)]['reg'][str(cont)] = {
                            'tipo':'AVERAGE_XP',
                            'anVal':ant,
                            'dpVal':novo_valor,
                            'QmMd':ctx.author.name 
                }
                await salvarS(dados)
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
                dados['Servers'][str(ctx.guild.id)]['reg'][str(cont)] = {
                            'tipo':'SLOWMODE_CHANGE',
                            'dpVal':int(tempo),
                            'QmMd':ctx.author.name 
                }
                await salvarS(dados)
                await ctx.send(f":question:  | **O CoolDown do chat {chat} foi alterado para {tempo}**")
                global log
                log = log + "\n" + f"SLOWMODE Alterado para {tempo} no servidor {ctx.guild.name}"
        @cmdconfig.command(name='prefix',aliases=['prefixo'])
        @commands.has_permissions(kick_members=True)
        async def prefix(self,ctx,prefix=None):
            if prefix != None:
                dados = await Dados()
                
                if prefix in dados['Servers'][str(ctx.guild.id)]['config']['prefix']:
                    await ctx.send(":warning: | **Já tem esse prefixo**")
                else:
                    dados['Servers'][str(ctx.guild.id)]['config']['prefix'][1] = prefix
                    cont = dados['Servers'][str(ctx.guild.id)]['contIDreg']
                    dados['Servers'][str(ctx.guild.id)]['reg'][str(cont)] = {
                            'tipo':'PREFIX_CHANGE',
                            'dpVal':prefix,
                            'QmMd':ctx.author.name 
                }
                    await salvarS(dados)
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
                dados['Servers'][str(ctx.guild.id)]['reg'][str(cont)] = {
                            'tipo':'AUTOROLE_CHANGE',
                            'dpVal':role.id,
                            'QmMd':ctx.author.name 
                }
                await salvarS(dados)
                await ctx.send(":question: | **Um cargo de autorole foi adicionado**")
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
            embed.set_footer(text='Está gostando do SphyX? Doe! .donate ',icon_url=ctx.author.avatar_url)
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
                await salvarS(dados)
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
                await salvarS(dados)
        @cmdconfig.command(name='dmpu')
        @commands.has_permissions(kick_members=True)
        async def dmpu(self,ctx,tipo=None):
            if tipo == None:
                await padrao(ctx,'Moderação','dmpu','Quando ativado o usuario que levou algum tipo de punição por exemplo Warn, o bot vai diretamente no DM dele avisar','`dmpu ativar ou desativar` -> Desativa ou Ativa a mensagem de punição na DM','```dmpu```','Staff')
            else: 
                tipo = tipo.lower()
                dados = await Dados()
                if tipo == 'ativar':
                    dados['Servers'][str(ctx.guild.id)]['config']['dmpu'] = 1
                    await ctx.send(":question: | **Mensagems de punição na DM foram ativados**")
                elif tipo == 'desativar':
                    dados['Servers'][str(ctx.guild.id)]['config']['dmpu'] = 0
                    await ctx.send(":question: | **Mensagems de punição na DM foram desativados**")
                else:
                    await ctx.send(":x: | **Use `ativar` ou `desativar`**")
                await salvarS(dados)
        @cmdconfig.command(name='automessage')
        @commands.has_permissions(kick_members=True)
        async def atmessage(self,ctx,*,nova_mensagem=None):
            if nova_mensagem == None:
                await padrao(ctx,'Moderação','automessage','Quando ativo os proximos membros que entrarem no servidor vão receber uma mensagem de boas vindas escrito por você!','`automessage <nova_mensagem>*`','```automessage```','Staff')
            else:
                dados = await Dados()
                dados['Servers'][str(ctx.guild.id)]['config']['automessage'] = nova_mensagem
                cont = dados['Servers'][str(ctx.guild.id)]['contIDreg']
                dados['Servers'][str(ctx.guild.id)]['reg'][cont] = {
                            'tipo':'AUTO_MESSAGE',
                            'dpVal':nova_mensagem,
                            'QmMd':ctx.author.name 
                }
                await salvarS(dados)
                global log
                log = log + "\n" + f"AVERAGE_XP Alterado para {prefix} no servidor {ctx.guild.name}"
    bot.add_cog(config(bot))
class RR():
    class ReactionRoles(commands.Cog):
        @commands.group(name='rr',aliases=['reactionroles'],invoke_without_command=True) 
        @commands.has_permissions(kick_members=True)
        async def rr(self,ctx,channelA: discord.TextChannel=None,message_id=None,emoji=None,cargo: discord.Role=None):
            if channelA == None:
                await padrao(ctx,'Moderação','ReactionRoles','ReactionRoles (RR) É um sistema de reação por cargos, você reagir em um emoji e ganha um cargo que a staff decidir','`rr <id da mensagem> <emoji> <cargo>`','```rr | reactionroles```','Staff')         
            else:
                channel = await bot.fetch_channel(channelA.id)
                msg = await channel.fetch_message(int(message_id))
                dados = await Dados()
                dados['Servers'][str(ctx.guild.id)]['config']['rrcont'] += 1
                cont = dados['Servers'][str(ctx.guild.id)]['config']['rrcont']
                try:
                    emoji = await bot.get_emoji(int(emoji))    
                    dados['Servers'][str(ctx.guild.id)]['config']['rr'][str(cont)] = {
                    'emoji':str(emoji.id),
                    'role':str(cargo.id),
                    'msg':str(message_id)
                }
                except ValueError:
                    dados['Servers'][str(ctx.guild.id)]['config']['rr'][str(cont)] = {
                    'emoji':str(emoji),
                    'role':str(cargo.id),
                    'msg':str(message_id)
                    }
                await salvarS(dados)
                await msg.add_reaction(emoji)
                await ctx.send(":question: | **ReactionRole Setado com sucesso**")
        @commands.Cog.listener()
        async def on_raw_reaction_add(self, payload):
            channel = await bot.fetch_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            user = await message.guild.fetch_member(payload.user_id)
            emojiA = payload.emoji
            dados = await Dados()
            if user.bot == True: return
            for i in dados['Servers'][str(user.guild.id)]['config']['rr']:
                if str(message.id) in dados['Servers'][str(user.guild.id)]['config']['rr'][i]['msg']:
                    try:
                        emoji = await user.guild.fetch_emoji(int(dados['Servers'][str(user.guild.id)]['config']['rr'][i]['emoji']))
                    except ValueError:
                        emoji = dados['Servers'][str(user.guild.id)]['config']['rr'][i]['emoji']
                    if str(emojiA) == str(emoji):
                        role = user.guild.get_role(int(dados['Servers'][str(user.guild.id)]['config']['rr'][i]['role']))
                        await user.add_roles(role)
        @commands.Cog.listener()
        async def on_raw_reaction_remove(self, payload):
            channel = await bot.fetch_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            user = await message.guild.fetch_member(payload.user_id)
            emojiA = payload.emoji
            dados = await Dados()
            if user.bot == True: return
            for i in dados['Servers'][str(user.guild.id)]['config']['rr']:
                if str(message.id) in dados['Servers'][str(user.guild.id)]['config']['rr'][i]['msg']:
                    try:
                        emoji = await user.guild.fetch_emoji(int(dados['Servers'][str(user.guild.id)]['config']['rr'][i]['emoji']))
                    except ValueError:
                        emoji = dados['Servers'][str(user.guild.id)]['config']['rr'][i]['emoji']
                    if str(emojiA) == str(emoji):
                        role = user.guild.get_role(int(dados['Servers'][str(user.guild.id)]['config']['rr'][i]['role']))
                        await user.remove_roles(role)
    bot.add_cog(ReactionRoles(bot))
class Diversao():
    class Gato(commands.Cog):
        @commands.command(name='gato',aliases=['cat','gatos','gatoaleatorio','randomcat'])
        async def cat(self,ctx):
            url = requests.get(url='https://aws.random.cat/meow')
            js = url.json()
            embed = discord.Embed(title='Gato Aleatorio')
            embed.set_image(url=js['file'])
            await ctx.send(embed=embed)
    class Dog(commands.Cog):
        @commands.command(name='cachorro',aliases=['dog','cachorros','cachorroaleatorio','randomdog'])
        async def dog(self,ctx):
            url = requests.get(url='https://dog.ceo/api/breeds/image/random')
            js = url.json()
            embed = discord.Embed(title='Cachorro Aleatorio')
            embed.set_image(url=js['message'])
            await ctx.send(embed=embed)
    class Ciencia(commands.Cog):
        @commands.command(name='ciencia',aliases=['acienciafoilongedemais','simounao'])
        async def ciencia(self,ctx,user: discord.User=None):
            if user == None:
                file = ctx.message.attachments
                try:
                    foto = file[0].url    
                except IndexError:
                    try:
                        foto = ultimafoto[ctx.guild.id][0].url               
                    except KeyError:
                        foto = ctx.author.avatar_url
            else:
                foto = user.avatar_url
            async with ctx.channel.typing():    
                template = img.open('imgs/ciencia.jpg')
                url = requests.get(url=foto)
                foto = img.open(BytesIO(url.content))
                foto = foto.resize((906,495))
                foto = foto.copy()
                template.paste(foto,(0,122))
                nome_do_arquivo=f"ciencia.png"
                template.save(nome_do_arquivo)
                arq = discord.File(open(nome_do_arquivo,'rb'))
            msg = await ctx.send(file=arq)
            await msg.add_reaction('😮')
            await msg.add_reaction('😠')
    class Art(commands.Cog):
        @commands.command(name='art',aliases=['arte'])
        async def art(self,ctx,user: discord.User=None):
            if user == None:
                file = ctx.message.attachments
                try:
                    foto = file[0].url    
                except IndexError:
                    try:
                        foto = ultimafoto[ctx.guild.id][0].url               
                    except KeyError:
                        foto = ctx.author.avatar_url
            #439 42, 145,170
            #440, 381
            else:
                foto = user.avatar_url
            async with ctx.channel.typing():   
                template = img.open('imgs/bbfoul.png')
                url = requests.get(url=foto)
                foto = img.open(BytesIO(url.content))
                foto = foto.resize((146,171))
                foto = foto.copy()
                template.paste(foto,(439,41))
                foto = foto.copy()
                template.paste(foto,(439,380))
                nome_do_arquivo=f"btfoul.png"
                template.save(nome_do_arquivo)
                arq = discord.File(open(nome_do_arquivo,'rb'))
            msg = await ctx.send(file=arq)
    class Fogo(commands.Cog): 
        @commands.command(name='fogo',aliases=['fire'])
        async def art(self,ctx,user: discord.User=None):
            if user == None:
                file = ctx.message.attachments
                try:
                    foto = file[0].url    
                except IndexError:
                    try:
                        foto = ultimafoto[ctx.guild.id][0].url               
                    except KeyError:
                        foto = ctx.author.avatar_url
            else:
                foto = user.avatar_url
            async with ctx.channel.typing():   
                kak = img.new('RGBA',(720,871))
                template = img.open('imgs/fogo.png')
                url = requests.get(url=foto)
                foto = img.open(BytesIO(url.content))
                foto = foto.resize((219,294))
                foto = foto.copy()
                kak.paste(foto,(59,76))
                template = template.copy()
                kak.paste(template,(0,0),template)
                nome_do_arquivo=f"fire.png"
                kak.save(nome_do_arquivo)
                arq = discord.File(open(nome_do_arquivo,'rb'))#218 294
            msg = await ctx.send(file=arq)
    class Triste(commands.Cog):
        @commands.command(name='triste',aliases=['sad'])
        async def art(self,ctx,user: discord.User=None):
            if user == None:
                file = ctx.message.attachments
                try:
                    foto = file[0].url    
                except IndexError:
                    try:
                        foto = ultimafoto[ctx.guild.id][0].url               
                    except KeyError:
                        foto = ctx.author.avatar_url      
            else:
                foto = user.avatar_url
            async with ctx.channel.typing():   
                kak = img.new('RGBA',(1024,599))
                template = img.open('imgs/tristeza.png')
                url = requests.get(url=foto)
                foto = img.open(BytesIO(url.content))
                foto = foto.resize((770,601))
                foto = foto.copy()
                kak.paste(foto,(344,0))
                template = template.copy()
                kak.paste(template,(0,0),template)
                nome_do_arquivo=f"fire.png"
                kak.save(nome_do_arquivo)
                arq = discord.File(open(nome_do_arquivo,'rb'))#218 294
            msg = await ctx.send(file=arq)
    class News(commands.Cog):
        @commands.command(name='news',aliases=['noticia','noticias'])
        async def news(self,ctx,user: commands.Greedy[discord.Member]=None,*,message=f'Noticias CHOCANTES! O Servidor morreu por falta de membros'):
            if user == None:
                file = ctx.message.attachments
                try:
                    foto = file[0].url    
                except IndexError:
                    try:
                        foto = ultimafoto[ctx.guild.id][0].url               
                    except KeyError:
                        foto = ctx.author.avatar_url
    
            else:
                foto = user[0].avatar_url
            async with ctx.channel.typing():   
                kak = img.new('RGBA',(1024,599))
                template = img.open('imgs/news.png')
                fonte = imgfont.truetype('cambriaz.ttf', 30)
                text = imgdraw.Draw(template)
                message = textwrap.fill(message,50)
                text.text((51,476),message,font=fonte,fill=(255,255,255)) #897 443
                url = requests.get(url=ctx.guild.icon_url if ctx.guild.icon_url != "" else ctx.author.avatar_url)
                imgsv = img.open(BytesIO(url.content))
                url = requests.get(url=foto)
                foto = img.open(BytesIO(url.content))
                foto = foto.resize((990,576))
                foto = foto.copy()
                imgsv = imgsv.resize((86,72))
                imgsv = imgsv.copy()
                template.paste(imgsv,(897,443))
                kak.paste(foto,(0,0))
                template = template.copy()
                kak.paste(template,(0,0),template)
                nome_do_arquivo=f"fire.png"
                kak.save(nome_do_arquivo)
                arq = discord.File(open(nome_do_arquivo,'rb'))#218 294
            msg = await ctx.send(file=arq)
        #51 476
    class Anime(commands.Cog):
        @commands.command(name='anime')
        async def anime(self,ctx,*,nome: str=None):
            if nome == None:
                await ctx.send(":x: | **Você esqueceu de informar o nome do anime**")
            else:
                try:
                    resultado = AnimeSearch(nome)
                except ValueError:
                    await ctx.send(':x: | **Nenhum resultado foi encontrado com esse nome**')
                    return
                anime = resultado.results[0]
                embed = discord.Embed(title=anime.title)
                embed.add_field(name=f'Informações de {anime.title}',value=f'\n\nNumero de episodios: {anime.episodes}\n\nAvaliação: {anime.score}\n\nTipo: {anime.type}\n\nSinopse: {anime.synopsis}\n\nQuer saber mais? [Clique aqui!]({anime.url})')
                embed.set_thumbnail(url=anime.image_url)
                
                embed.set_footer(text=f'ID: {anime.mal_id}')
                await ctx.send(embed=embed)
    class Osu(commands.Cog):
        @commands.command(name='osu',invoke_without_command=True)
        async def osu(self,ctx,*,user: str=None):
            if user == None:
                await ctx.send("Você esqueceu de colocar um valor, você pode tentar ```osu <user>```  ou ```osu_beatmap <beatmap id>```")
            else:
                resulta = osu.get_user(user)
                try:
                    user = resulta[0]
                except IndexError:
                    await ctx.send(":x: | **Você informou um usuario não existente, tente novamente**")
                    return
                embed = discord.Embed(title=f'Perfil de {user.username}')
                embed.add_field(name=f'Informações do membro {user.username}',value=f'\nNivel: {int(user.level)}\n\nData de entrada: [{user.join_date}]\n\nTempo de jogo: {user.total_seconds_played // 60 // 60} Horas de jogo\n\nRANK PP: {user.pp_rank}\n\nPrecisão: {int(user.accuracy)}\n\nQuantidade de partidas jogadas: {user.playcount}\n\nPontuação: {user.total_score}\n\n**Contagem de grade**\nSS+ : {user.count_rank_ssh}\nSS : {user.count_rank_ss}\nS+ : {user.count_rank_sh}\nS : {user.count_rank_s}\nA : {user.count_rank_a}')
                embed.set_thumbnail(url=f'http://s.ppy.sh/a/{user.user_id}')
                await ctx.send(embed=embed)
    class OsuBeatMap(commands.Cog):
        @commands.command(name='osu_beatmap')
        async def beatmap(self,ctx,beatmap=None):
            if beatmap == None:
                await ctx.send("Você esqueceu de colocar o id do beatmap")
            else:
                bp=0
                haha = osu.get_beatmaps(beatmap_id=beatmap)
                try:
                    bp = haha[0]
                except IndexError:
                    await ctx.send(":x: | **Você informou um beatmap inexistente**")
                    return
                embed = discord.Embed(title=f'Beatmap {bp.title}')
                if bp.approved == "1":
                    apro = "Rankeado"
                elif bp.approved == "2":
                    apro = "Aprovado"
                elif bp.approved == "3":
                    apro = "Qualificado"
                elif bp.approved == "4":
                    apro = "Loved"
                else:
                    apro = "Pendente"

                embed.add_field(name=f'Informações do beatmap {bp.title}',value=f'\nStatus do BP: {apro}\n\nCriador: {bp.artist}\n\nBPM: {bp.bpm}\n\nMedia de dificuldade: {int(bp.difficultyrating)}\n\nTags: {bp.tags}\n\nDuração: {bp.total_length // 60} Minutos e {int(bp.total_length % 60)} Segundos')
                embed.set_thumbnail(url=f'https://assets.ppy.sh/beatmaps/{bp.beatmap_id}/covers/cover.jpg')
                await ctx.send(embed=embed)    
    class Run(commands.Cog):
        @commands.command(name='run')
        async def run(self,ctx,*,code=None):
            if code == None:
                try:
                    file = ctx.message.attachments
                    await file[0].save('krek.py')    
                except IndexError:
                    await ctx.send('Insira o código')
                    return
            
            file = ctx.message.attachments
            try:
                await file[0].save('krek.py')    
            except IndexError:
                code = code
                with open("krek.py",'w') as f:
                    f.write(code)
            process = subprocess.Popen(['python.exe','krek.py'], stdout=subprocess.PIPE)
            await ctx.send(f"```\n{process.communicate()[0].decode('cp1250')}```")
    bot.add_cog(Anime(bot))
    bot.add_cog(Ciencia(bot))     
    bot.add_cog(Dog(bot))
    bot.add_cog(Art(bot))
    #bot.add_cog(Run(bot))
    bot.add_cog(Fogo(bot))
    bot.add_cog(Gato(bot))
    bot.add_cog(Triste(bot))
    bot.add_cog(News(bot))
    bot.add_cog(Osu(bot))
    bot.add_cog(OsuBeatMap(bot))
async def shop() -> dict:
    with open('shop.json','r',encoding='utf-8') as f:
        return dict(json.load(f))
class Economia():
    class Atm(commands.Cog):
        @commands.command(name='atm',aliases=['money','coin','coins','dinheiro','meudinheiro','mymoney'])
        async def atm(self,ctx,user: discord.Member=None):
            user = user or ctx.author
            dados = await UDados()
            embed = discord.Embed(title=f'Conta bancaria de {user.name}',description=f'A Conta bancaria é o lugar onde tem informações de economia do usuario\n\nSeu dinheiro: **{dados["Users"][str(user.id)]["money"]}**\nSeus Gold Coins: **{dados["Users"][str(user.id)]["gold"]}**')
            await ctx.send(embed=embed)
    class Daily(commands.Cog):
        @commands.command(name='daily',aliases=['diaria','day'])
        @commands.cooldown(1,24000,commands.BucketType.member)
        async def daily(self,ctx):
            dados = await UDados()
            rand = randrange(400,800)
            dados['Users'][str(ctx.author.id)]['money'] += rand
            await salvar(dados)
            embed = discord.Embed(title=f'Recompensa diaria de {ctx.author.name}',description=f'Você pegou sua recompensa diaria de hoje, para pegar a proxima pegue no proxima dia\n\nVocê ganhou {rand} moedas!')
            embed.set_thumbnail(url='https://media.discordapp.net/attachments/765971397524062220/788833032382840882/gift.png')
            await ctx.send(embed=embed)
        '''@commands.Cog.listener()
        async def on_command_error(self,ctx,error):
            if isinstance(error, commands.CommandOnCooldown):
                await ctx.send(f":x: | ** Você precisa esperar {error.retry_after // 180} Horas para pegar o prêmio diario**")
            else:
                await ctx.send(error)'''
        ####################evento lá fodase on_commands error n se esqueça pau no anus
    class TopMoney(commands.Cog):
        @commands.command(name='topmoney',aliases=['rankdinheiro','rankcoin'])
        async def top_money(self,ctx,index:int=1):
            print(index*10)
            pages=[]
            dic={}
            lista=[]
            msg=""
            isa=0
            dados = await UDados()
            for i in dados['Users']:
                user = bot.get_user(int(i))
                dic[dados['Users'][i]['money']] = user.name
                lista.append(dados['Users'][i]['money'])
            lista = sorted(lista,reverse=True)
            for g in lista:
                if g == 0:
                    await ctx.send(msg)
                    break
                isa += 1
                if isa >= index*10-9:
                    try:
                        msg = msg +'\n'+ dic[g] + ' - ' + str(g) + 'cs'
                    except IndexError:
                        await ctx.send(msg)
                elif isa >= index*10:
                    await ctx.send(msg)
                    return
    class Pay(commands.Cog):
        @commands.command(name='pay',aliases=['pagar'])
        async def pay(self,ctx,user:discord.Member=None,dinheiro:int=1):
            if user == None:
                await ctx.send(":x: | **Você precisa informar um membro**")
            elif user.id == ctx.author.id:
                await ctx.send(":x: | **Você não pode se pagar**")
            elif dinheiro <= 0:
                await ctx.send(":x: | **Você precisa dar um numero maior que 0**")
            else:
                dados = await UDados()
                if dinheiro > dados['Users'][str(ctx.author.id)]['money']:
                    await ctx.send(":x: | **Você não pode pagar essa quantidade**")
                else:
                    dados['Users'][str(ctx.author.id)]['money'] -= dinheiro
                    dados['Users'][str(user.id)]['money'] += dinheiro
                    await salvar(dados)
                    await ctx.send(f":question: | **Você deu {dinheiro}cs para {user.name}**")
    class Giveway(commands.Cog):        
        @commands.command(name='giveway',aliases=['sorteio','sortear'])
        async def giveway(self,ctx,horario=None,num: int=1,*,message:str='Sorteio'):
            if horario == None:
                await ctx.send(":x: | **Informe o tempo do sorteio e a mensagem**")
            else:
                embed = discord.Embed(title='Sorteio',description=f'\n{message}**\nNumero de ganhadores {num}\nTempo de sorteio {horario}**')
                msg = await ctx.send(embed=embed)
                horario = horario.lower()
                await msg.add_reaction('🎉')
                global vargv
                vargv[str(ctx.guild.id)] = {msg.id:{"time":horario,'ganhadores':num,'gar':[]}}   
                if horario[1] == 'm' or horario[2] == 'm':
                    horario = horario.replace('m','')
                    time=int(horario)
                    time = time * 60
                elif horario[1] == 'h' or horario[2] == 'h':
                    horario = horario.replace('h','')
                    time=int(horario)
                    time = time * 60 * 60
                elif horario[1] == 'd' or horario[2] == 'd':
                    horario = horario.replace('d','')
                    time=int(horario)
                    time = time * 60 * 60 * 60
                elif horario[1] == 's' or horario[2] == 's':
                    horario = horario.replace('s','')
                    time = int(horario)
                else:
                    await ctx.send("Formatos de horarios disponiveis [s/m/h/d]")
                    return
                await asyncio.sleep(time)
                msgA=''
                lk=[]
                krek=[]
                for i in range(num):
                    lk.append(random.choice(vargv[str(ctx.guild.id)][msg.id]['gar']))
                    user = ctx.guild.get_member(lk[i])
                    while user in krek:
                        lk.append(random.choice(vargv[str(ctx.guild.id)][msg.id]['gar']))
                        user = ctx.guild.get_member(lk[i])
                    msgA = msgA + user.mention + ','
                    krek.append(user)
                await ctx.send(f" 🎉 {msgA} Ganhou o sorteio!")                
        @commands.Cog.listener()
        async def on_reaction_add(self,reaction,user):
            global vargv
            if user.bot == True:
                return
            if reaction.emoji == '🎉':
                if str(reaction.message.guild.id) in vargv:
                    print(reaction.message.id)
                    print(vargv[str(reaction.message.guild.id)])
                    if reaction.message.id in vargv[str(reaction.message.guild.id)]:
                        vargv[str(reaction.message.guild.id)][reaction.message.id]['gar'].append(user.id)                        
    class Shop(commands.Cog):
        @commands.command(name='shop',aliases=['store','loja'])
        async def shop(self,ctx, index: int=1):
            shop=''
            with open('shop.json','r',encoding='utf-8') as f:
                shop = dict(json.load(f))
            try:
                msg=""
                isa=0
                embed = discord.Embed(title='Loja')
                embed.set_footer(text='Digite "next" para ir para a proxima página da loja ou "back" para voltar para a pagina anterior ou digite o ID do item para comprar ou visualizar')
                isa = 0
                msg = ""
                fu = False
                for d in range(index*10):
                    isa += 1 
                    if isa >= index*10-9:
                        try:
                            msg = msg +'\n'+ f' ID : **{isa}**  |  :dollar: ' + str(shop[str(isa)]['preco']) + ' - ' + shop[str(isa)]['name']
                        except KeyError as err:
                            embed.add_field(name=f'Pagina {index} ',value=msg)
                            msg = await ctx.send(embed=embed)
                            fu = True
                            break
                if isa == index*10:
                    if fu:
                        pass
                    else:
                        embed.add_field(name=f'Pagina {index} ',value=msg)
                        msg = await ctx.send(embed=embed)   
                try:
                    def checkMS(author,messagecheck):
                        def inner_check(message):
                            if message.author == author:
                                if message.content.lower() == messagecheck or message.content.lower() in messagecheck: return True
                                try: 
                                    if message.content.lower().split()[0] in shop: return True
                                except ValueError:
                                    return False
                                else: return False                            
                        return inner_check
                    ms = await bot.wait_for(event='message',check=checkMS(ctx.author,['next','back']),timeout=60)
                    if ms.content.lower() == 'next':
                        await msg.delete()
                        index += 1
                        await Economia.Shop.shop(self,ctx,index)
                    elif ms.content.lower() == 'back':
                        if index == 1:
                            index = 1
                            await msg.delete()
                            await Economia.Shop.shop(self,ctx,index)
                        else:
                            await msg.delete()
                            await Economia.Shop.shop(self,ctx,index-1)
                    else:
                        await msg.delete()
                        li = ms.content.lower().split(' ')
                        try: 
                            val = li[0]
                            await Economia.Comprar.comprar(self,ctx,val)
                        except ValueError: await ctx.send(":question: | **Você mandou uma mensagem diferente, caso queira comprar um item use o comando novamente**")    
                except asyncio.TimeoutError: await ctx.send(":x: | Loja: **Tempo esgotado**")
            except HTTPException as err:
                await ctx.send(':x: | Loja: **Pagina inexistente**')
                return    
    class Inventory(commands.Cog):
        @commands.command(name='inventory',aliases=['inventario','inv'])
        async def inventory(self,ctx,index: int=1):
            user = ctx.author
            shop=''
            with open('shop.json','r',encoding='utf-8') as f:
                shop = dict(json.load(f))
            ix = 0
            msg = ""
            dados = await UDados()
            inv = dict(dados['Users'][str(user.id)]['inventory'])
            embed = discord.Embed(title=f'Inventario de {str(user)}',description='Nome | Tipo do item | Usavel')
            for k,v in inv.items():
                ix += 1
                if ix >= index*10-10:
                    msg = msg + '\n' + f'**{k}** | {v["tip"]} | Usavel: {":white_check_mark:" if v["use"] else ":negative_squared_cross_mark:"}'
                if ix >= index*10:
                    break
            embed.add_field(name=f'Pagina {index}',value=msg if msg != "" else "Você não tem nenhum item, veja alguns itens usando o `.shop`!")  
            embed.set_footer(text='Use "info" para ver as informações ou usar o item')      
            msg = await ctx.send(embed=embed)
            def checkMS(author,messagecheck):
                def inner_check(message):
                    if message.author == author:
                        if message.content.lower() == messagecheck or message.content.lower() in messagecheck: return True
                        elif message.content.lower().split()[0] in ['info']: return True
                        else: return False
                return inner_check
            ms = await bot.wait_for(event='message',check=checkMS(ctx.author,'next'),timeout=60)
            if ms.content.lower() == 'next':
                await msg.delete()
                await ms.delete()
                index += 1
                await Economia.Inventory.inventory(self,ctx,index)
            elif 'info' in ms.content.lower():
                await msg.delete()
                await ms.delete()
                li = ms.content.split(' ')
                try: 
                    try: val = li[1]
                    except IndexError: return
                    try:
                        var = inv[val]
                    except KeyError:
                        try: 
                            try: 
                                var = inv[li[1] + ' ' + li[2]]
                            except IndexError: return
                        except KeyError:
                            await ctx.send(":x: | **Nome invalido! Verifique se você tem esse item em seu inventario** ")
                            return 
                    vard = ["Use \"voltar\" para voltar ao inventario","Use \"use\" para usar o item"]
                    embed = discord.Embed(title=f'Informações do item: {var["name"]}',description=f'\n`{var["desc"]}`\n\nUsavel: **{"Sim" if var["use"] else "Não"}** | Tipo do item: **{var["tip"]}**')
                    embed.set_footer(text=f"{vard[1]+' '+vard[0] if var['use'] else vard[0]}")
                    embed.set_thumbnail(url=var['preview'])
                    m = await ctx.send(embed=embed)
                    try: ms = await bot.wait_for(event='message',check=check(ctx.author,['usar','use','voltar','back']),timeout=60)
                    except asyncio.TimeoutError:
                        await ctx.send(':x: | Inventario: **Tempo esgotado**'); return
                    if ms.content.lower() == 'use' or ms.content.lower() == 'usar':
                        await m.delete()
                        await ms.delete()
                        dados['Users'][str(user.id)]['profile'][var['tipte']]['url'] = var['preview']
                        dados['Users'][str(user.id)]['profile'][var['tipte']]['name'] = var['name']
                        await ctx.send(f":question: | **Você usou o item {var['name']}**")
                        await salvar(dados)
                    else:
                        await ms.delete()
                        await m.delete()
                        await Economia.Inventory.inventory(self,ctx,index)
                except ValueError: await ctx.send(":x: | **Você usou a forma errada... aqui está o jeito certo `item <nome>`**")                
    class Comprar(commands.Cog):
        @commands.command(name='comprar',aliases=['buy'])
        async def comprar(self,ctx,index=None):
            shop=''
            with open('shop.json','r',encoding='utf-8') as f:
                shop = dict(json.load(f))
            if index == None:
                await ctx.send(":x: | ** Index invalida, para ver index válidas use o .shop **")
            else:
                d = await UDados()
                embed = discord.Embed(title=shop[index]['name'], description=f'\n\n`{shop[index]["desc"]}`\n\nPreco: {shop[index]["preco"]} | Você tem {d["Users"][str(ctx.author.id)]["money"]} | {":white_check_mark:" if d["Users"][str(ctx.author.id)]["money"] >= shop[index]["preco"] else ":x:"}\n\n{"Esse item é consumivel" if shop[index]["usa"] else "Esse item não é consumivel"} | Tipo do item: {shop[index]["categoria"]} | Autor: {shop[index]["author"] if shop[index]["author"] != None else "Nenhum / Indefinido"}')
                embed.set_footer(text='Reaja ✅ Para confirmar a compra ou ♻️ para comprar e usar',icon_url=ctx.author.avatar_url)
                embed.set_thumbnail(url=shop[index]["preview"])
                msg = await ctx.send(embed=embed)                
                await msg.add_reaction('✅')
                await msg.add_reaction('♻️')
                def checkr(reaction,user):
                    return user == ctx.message.author and reaction.emoji in ["✅","♻️"]
                try:
                    reac,user = await bot.wait_for('reaction_add',check=checkr,timeout=60)
                    if shop[index]["preco"] > d['Users'][str(ctx.author.id)]['money']:
                        await ctx.send(':x: | **Você não tem dinheiro suficiente para fazer essa compra**')
                    else:
                        if shop[index]['name'] not in d["Users"][str(ctx.author.id)]['inventory']:                        
                            d["Users"][str(ctx.author.id)]['inventory'][shop[index]['name']] = {
                                "name":shop[index]['name'],
                                "desc":shop[index]['desc'],
                                "tip":shop[index]['categoria'],
                                "use":shop[index]['usa'],
                                "cont":0,
                                "onetime":shop[index]["onetime"],
                                "preview":shop[index]["preview"],
                                "tipte":shop[index]['ti'],
                                "author":shop[index]['author']
                            }
                            await ctx.send(f":question: | **Você comprou {shop[index]['name']}** ")
                            d["Users"][str(ctx.author.id)]['money'] -= shop[index]["preco"]
                        else:
                            if shop[index]['onetime']:
                                await ctx.send(":x: | **Você só pode comprar isso 1 vez**")
                                return    
                            d["Users"][str(ctx.author.id)]['inventory'][shop[index]['name']]["cont"] += 1
                        if reac.emoji == '♻️':
                            d["Users"][str(ctx.author.id)]['profile'][shop[index]['ti']] = {'url':shop[index]['preview'],'name':shop[index]['name']}
                    await salvar(d)
                except asyncio.TimeoutError:
                    ms = await ctx.send(":x: | **Tempo excedido**")
                    await asyncio.sleep(3)
                    await ms.delete()
    bot.add_cog(TopMoney(bot))
    bot.add_cog(Inventory(bot))
    bot.add_cog(Giveway(bot))
    bot.add_cog(Pay(bot))
    bot.add_cog(Comprar(bot))
    bot.add_cog(Daily(bot))
    bot.add_cog(Atm(bot))
    bot.add_cog(Shop(bot))
class Dev():
    class Repo(commands.Cog):
        @commands.command(name='repo', aliases=['repositorio'])
        async def repo(self,ctx,author=None,nmrepo=None):
            re = requests.get(
                    f'https://api.github.com/repos/{author}/{nmrepo}',
                    params=[('-H', 'Accept: application/vnd.github.scarlet-witch-preview+json')],
                    )
            if re.status_code != 200:
                await ctx.send(":x: | **Algo deu errado**")
            else:
                rep = dict(re.json())
                embed = discord.Embed(title=f'Repositorio de {rep["owner"]["login"]}', description=f'\n\nNome do repositorio: **{rep["full_name"]}**\nDescrição: {rep["description"]}\nURL : https://github/{rep["owner"]["login"]}/{rep["name"]}\nLinguagem: {rep["language"]}\nQuantidade de estrelas: {rep["stargazers_count"]}\nForks: {rep["forks_count"]}'                
                )
                embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/776197504378732555/793430718525079572/25231.png')
                embed.set_image(url=rep['owner']['avatar_url'])
                embed.set_footer(text=f'Criado em {rep["created_at"]}',icon_url='https://cdn.discordapp.com/emojis/786911257596133426.png?v=1')
                await ctx.send(embed=embed)
    class Traduzir(commands.Cog):
        @commands.command(name='traduzir',aliases=['translate'])
        async def traduzir(self,ctx,de=None,para=None,*,mensagem=None):
            if de == None:
                await ctx.send(":x: | **Você fez do jeito incorreto, como usar: `.traduzir PtBr EnUs Olá mundo!` <- De português para inglês ou `.traduzir EnUs PtBr Hello World!` de inglês para português!**")
                return
            url = 'https://api.gotit.ai/Translation/v1.1/Translate'
            data = {"T":mensagem,"SL":de,"TL":para}
            data_json = json.dumps(data)
            userAndPass = base64.b64encode(b"2002-WaC/7LOO:RVJzQ3qynPtWLKH14JpWZ11PDaTyGZgPur+n5S/TdQwc").decode("ascii")
            headers = {'Content-type': 'application/json', "Authorization": "Basic %s" %  userAndPass}
            response = requests.post(url, data=data_json, headers=headers)
            if response.status_code != 200:
                print(response.status_code)
                await ctx.send(":x: | **Você fez do jeito incorreto, como usar: `.traduzir PtBr EnUs Olá mundo!` <- De português para inglês ou `.traduzir EnUs PtBr Hello World!` de inglês para português!")
                return
            js = response.json()
            await ctx.send(f'Texto traduzido: {js["result"]}') 
    class Short(commands.Cog):
        @commands.command(name='short',aliases=['encurtador','link'])
        async def short(self,ctx,link=None):
            if link == None: 
                await ctx.send(':x: | **Você esqueceu de colocar o link**')
                return
            s = pyshorteners.Shortener()
            await ctx.send(f':question: | **Aqui está o seu link:** {s.tinyurl.short(link)}')
    class QR(commands.Cog):
        @commands.command(name='qr',aliases=['qrcode'])
        async def qr(self,ctx,link=None):
            if link == None: 
                await ctx.send(':x: | **Você esqueceu de colocar o link**')
                return
            img = qrcode.make(link)
            img.save('nome_do_arquivo.png')
            arq = discord.File(open('nome_do_arquivo.png','rb'))#218 294
            msg = await ctx.send(file=arq)
    class hastebin(commands.Cog):
        @commands.command(name='hastebin')
        async def hastebin(self,ctx,file='txt',*,code=None):
            if code == None:
                try:
                    file = ctx.message.attachments
                    await file[0].save(f'krek.{file}')    
                    with open("krek.py",'r') as f:
                        code = f.read()
                except IndexError:
                    await ctx.send(":x: | **Você esqueceu de colocar o código, você pode tentar um arquivo ou escrever** Como usar: `.hastebin <py tem que ser a extensão do arquivo da linguagem> <code>`")
                    return
            req = requests.post('https://hastebin.com/documents',
            data=code)
            key = json.loads(req.content)   
            await ctx.send(f':question: | **Aqui está o link:** https://hastebin.com/{key["key"]} ')             
    class att(commands.Cog):
        @commands.command(name='att')
        async def att(self,ctx):
            if ctx.author.id not in devs:
                return
            a = None
            with open('dados.json','r') as f:
                a = json.load(f)
            for i in bot.guilds:
                a[str(i.id)] = '.'
            with open('dados.json','w') as f:
                json.dump(a,f)
            await ctx.send("FASASASASASS")
    class teste(commands.Cog):
        @commands.command(name='teste')
        async def teste(ctx):
            if ctx.author.id not in devs:
                return
            guilds = users.find_one()
            guids = users.find_one()
            for i in bot.users:
                guilds['Users'][str(i.id)]['mar'] = 0
                print(i)
            sets = {"$set":guilds}
            users.update_one(guids,sets)
            await ctx.send("De primeira caralho")
    class ping(commands.Cog):
        @commands.command(name='ping')
        async def ping(self,ctx):
            print("a")
            await ctx.send(f":question: | **Minha látencia é: {int(bot.latency * 1000)}**")
    class xko(commands.Cog):
        @commands.command(name='xko')
        async def xko(ctx, user: discord.User,qnt:int):
            if ctx.author.id not in devs:
                return
            d = await UDados()
            d['Users'][str(user.id)]['money'] += qnt
            await ctx.send(f"{random.randrange(10,100000)}")
            await salvar(d)
    bot.add_cog(hastebin(bot))
    bot.add_cog(att(bot))
    bot.add_cog(xko(bot))
    bot.add_cog(teste(bot))
    bot.add_cog(ping(bot))
    bot.add_cog(QR(bot))
    bot.add_cog(Short(bot))
    bot.add_cog(Repo(bot))
    bot.add_cog(Traduzir(bot))
class Social():
    class Profile(commands.Cog):
        @commands.command(name='profile',aliases=['perfil'])
        async def profile(self,ctx,user: discord.User=None):
            user = user or ctx.author
            async with ctx.channel.typing():
                temp = img.new('RGBA',(1400,1000))
                avt = user.avatar_url
                dad = await UDados()
                rp=()
                if dad['Users'][str(user.id)]['mar'] == 0:
                    rp = (318,124)
                    imga = img.open('pf.png')
                else:
                    imga = img.open('tempMa.png')
                    rp = (313,197)
                avt = requests.get(url=avt)
                foto = img.open(BytesIO(avt.content)).resize((302,302)).convert('RGBA')
                re = requests.get(url=dad['Users'][str(user.id)]['profile']['back-pf']['url'])
                backgr = img.open(BytesIO(re.content)).resize(temp.size)
                bigsize = (foto.size[0] * 3, foto.size[1] * 3)
                mask = img.new('L', bigsize, 0)
                draw = ImageDraw.Draw(mask)
                draw.ellipse((0,0) + bigsize, fill=255)
                mask = mask.resize(foto.size, img.ANTIALIAS)
                foto.putalpha(mask)
                output = ImageOps.fit(foto, mask.size, centering=(0.5, 0.5))
                output.putalpha(mask)
                backgr.copy()
                temp.paste(backgr,(0,0))
                
                imga.copy()
                temp.paste(imga,(0,0),imga)
                foto.copy()
                temp.paste(foto,(16,0), foto)
                draw = ImageDraw.Draw(temp)
                message = str(user)
                if len(message) > 15 : 
                    var = message[:15]
                    var = var + '...' 
                fonte = imgfont.truetype('ARIALBD.TTF', 43)
                draw.text((318,50),message,font=fonte,fill=(255,255,255))
                desc = textwrap.fill(dad['Users'][str(user.id)]['desc'],60,break_long_words=True)
                fonte = imgfont.truetype('ARIALBD.TTF', 34)
                draw.text((27,800),desc,font=fonte,fill=(255,255,255))
                fonte = imgfont.truetype('ARIALBD.TTF', 43)
                draw.text(rp,str(dad['Users'][str(user.id)]['rep']) + ' Reps',font=fonte,fill=(255,255,255))
                if dad['Users'][str(user.id)]['mar'] != 0:
                    fonte = imgfont.truetype('ARIALBD.TTF', 38)
                    us = bot.get_user(dad['Users'][str(user.id)]['mar'])
                    draw.text((317,130),f'Casado com: {us.name}',font=fonte,fill=(255,255,255))
                temp.save('pfout.png',otimize=True,quality=100)
                arq = discord.File(open('pfout.png','rb'))#218 294
                #261 112
            msg = await ctx.send(file=arq)
    class Desc(commands.Cog):
        @commands.command(name='desc',aliases=['sobre-mim','sobre'])
        async def desc(self,ctx,*,nova_desc=None):
            if nova_desc == None:
                await ctx.send(':x: | **Você esqueceu de colocar a descrição**')
            else:
                var=''
                dados = await UDados()
                if len(nova_desc) > 150: 
                    var = nova_desc[:150]
                    var = var  + '...'
                else:
                    var = nova_desc
                dados['Users'][str(ctx.author.id)]['desc'] = var
                await salvar(dados)

                await ctx.send(f":question: | **Pronto, descrição alterado para** ```{var}```")
    class Help(commands.Cog):
        @commands.command(name='help',aliases=['ajuda'])
        async def help(self,ctx):
            embed = discord.Embed(title=f'Olá {str(ctx.author)}!',description='**Parece que você precisa de ajuda...\n**\n**Quer ver meus comandos?**\n\a [Comandos](https://sphyx-6ffe7.web.app/pages/comandos.html)\n\a [TopGG](https://top.gg/bot/782737686238461952)\n\n**Está com alguma dúvida?**\n\a [FAQ](https://sphyx-6ffe7.web.app/pages/FAQ.html)\n\a [Server do discord](https://discord.gg/CG7spnTsKa)')
            embed.set_footer(text=f'{ctx.author.name} usou as {str(time.strftime("%H:%M", time.localtime()))}',icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
    class Rep(commands.Cog):
        @commands.command(name='rep',aliases=['reputação'])
        @commands.cooldown(1,48000,BucketType.user)
        async def rep(self,ctx,user: discord.User=None):
            if user == None:
                await ctx.send(':x: | **Você não informou um membro, agora só podera dar outro REP daqui a 1 dia**')
                
            else:
                dados = await UDados()
                dados['Users'][str(user.id)]['rep'] += 1
                await salvar(dados)
                await ctx.send(f":question: | **Você deu um ponto de reputação para {user.mention}**")
    class addBack(commands.Cog):
        @commands.command(name='addBack')
        async def addBack(self,ctx):
            if ctx.author.id in devs:
                msg = await ctx.send(":white_check_mark: | **Informe o nome do background**")
                def checkMS(author):
                        def inner_check(message):
                            if message.author == author:
                                return True  
                ms = await bot.wait_for(event='message',check=checkMS(ctx.author),timeout=30)
                shop=''
                with open('shop.json','r',encoding='utf-8') as f:
                    shop = dict(json.load(f))
                cont = shop['cont'] + 1
                shop['cont'] += 1
                shop[cont] = {}
                shop[cont]['name'] = ms.content
                await ms.delete()
                await msg.edit(content=':white_check_mark: | **Informe a descrição do shopground**')
                ms = await bot.wait_for(event='message',check=checkMS(ctx.author),timeout=30)
                shop[cont]['desc'] = ms.content
                await ms.delete()
                await msg.edit(content=":white_check_mark: | **Informe o preço do background**")
                ms = await bot.wait_for(event='message',check=checkMS(ctx.author),timeout=30)
                shop[cont]['preco'] = int(ms.content)
                await ms.delete()
                await msg.edit(content=":white_check_mark: | **Informe o LINK do background**")
                ms = await bot.wait_for(event='message',check=checkMS(ctx.author),timeout=30)
                shop[cont]['preview'] = ms.content
                await ms.delete()
                await msg.edit(content=":white_check_mark: | **Informe o author do background [Caso não tenha digite 'null']**")
                ms = await bot.wait_for(event='message',check=checkMS(ctx.author),timeout=30)
                shop[cont]['author'] = ms.content if ms.content != 'null' else None
                await ms.delete()
                await msg.edit(content="Aguarde...")
                shop[cont]['ti'] = 'back-pf'
                shop[cont]['categoria'] = 'BackGround Profile'
                shop[cont]['onetime'] = True
                shop[cont]['usa'] = True
                ig = img.new('RGBA',(1400,1000))
                re = requests.get(url=shop[cont]['preview'])
                im = img.open(BytesIO(re.content)).resize((1400,1000))
                im.copy()
                temp = img.open('kkk.png')
                temp.copy()
                ig.paste(im,(0,0))
                ig.paste(temp,(0,0),temp)
                ig.save('jsa.png',format='png')
                file = discord.File(open('jsa.png','rb'))
                await ctx.send('Aqui está um preview! Você quer realmente adicionar? Se sim digite "aceito"',file=file)
                try: 
                    ms = await bot.wait_for(event='message',check=check(ctx.author,'aceito'),timeout=30)
                    with open('shop.json','w') as f:
                        json.dump(shop,f,indent=4)
                except asyncio.TimeoutError: return
    class marry(commands.Cog):
        @commands.command(name='marry',aliases=['casar'])
        async def marry(self,ctx,user:discord.Member=None):
            if user == None:
                await ctx.send(":x: | **Você não informou o membro**")
                return
            dados = await UDados()
            if dados['Users'][str(ctx.author.id)]['mar'] != 0 or dados['Users'][str(user.id)]['mar'] != 0:
                await ctx.send(":x: | **Você ou ele(a) já está casado, para divorciar use `.divorcio`**")
                return
            msg = await ctx.send(f":question: | **Você quer mesmo se casar com {user.name}, vocês dois precisam pagar 4500 para se casar, {user.mention} se quiser se casar com {ctx.author.mention} reaja no anel!**")
            await msg.add_reaction('💍')
            def checkr(reaction,useraa):
                    return useraa == user and reaction.emoji in ["💍"]
            try:
                reac,user = await bot.wait_for('reaction_add',check=checkr,timeout=60)
                dado = await UDados()
                if dado['Users'][str(ctx.author.id)]['money'] < 4500 or dado['Users'][str(user.id)]['money'] < 4500:
                    await ctx.send(":x: | **Você não tem dinheiro para fazer o casamento!**")
                await ctx.send(f":heart: | **Parece que aconteceu um casamento :flushed:, {ctx.author.name} se casou com {user.name}**")
                dado['Users'][str(user.id)]['mar'] = ctx.author.id
                dado['Users'][str(ctx.author.id)]['mar'] = user.id
                dado['Users'][str(ctx.author.id)]['money'] -= 4500
                dado['Users'][str(user.id)]['money'] -= 4500
                await salvar(dado)
            except asyncio.TimeoutError:
                await ctx.send(":sob: | **Parece que o casamento não deu certo**")
    class divorcio(commands.Cog):
        @commands.command(name='divorcio')
        async def divorcio(self,ctx):
            dados = await UDados()
            if dados['Users'][str(ctx.author.id)]['mar'] == 0:
                await ctx.send(':x: | **Você não pode se divorciar com ninguem :thonk:**')
            else:
                msg = await ctx.send("Você tem certeza?")
                await msg.add_reaction('✅')
                def checkr(reaction,useraa):
                    return useraa == ctx.author and reaction.emoji in ["✅"]
                try:
                    reac,user = await bot.wait_for('reaction_add',check=checkr,timeout=60)
                    id = dados['Users'][str(ctx.author.id)]['mar']
                    dados['Users'][str(ctx.author.id)]['mar'] = 0
                    us = bot.get_user(id)
                    await ctx.send(f":sob: | **Você se divorciou de {us.name}**")
                    await salvar(dados)
                except asyncio.TimeoutError:
                    await ctx.send(':smiley: | **Parece que o casamento ainda não acabou**')
    bot.add_cog(Profile(bot))
    bot.add_cog(Help(bot))
    bot.add_cog(Rep(bot))
    bot.add_cog(marry(bot))
    bot.add_cog(divorcio(bot))
    bot.add_cog(addBack(bot))
    bot.add_cog(Desc(bot))
class TopGG(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.token = '@'
        self.dblpy = dbl.DBLClient(self.bot, self.token, webhook_path='/dblwebhook', webhook_auth=':+1:', webhook_port=5000)
    @commands.Cog.listener()
    async def on_dbl_vote(self,data):
        await data.user.send("Obrigado por votar")
        print("Alo")
bot.add_cog(TopGG(bot))
bot.run(token.token())
