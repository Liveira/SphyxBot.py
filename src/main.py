'''
          SPHYXBOT
 TODOS OS DIREITOS RESEVADOS
  MIT LICENSE 2020 - 2021
      LIVEIRA;DREAMCAT
'''
import sys
import asyncio
from io import *
import contextlib,re
from json import decoder
from operator import iand
from random import randrange
import time,calendar
from discord.abc import GuildChannel, User
from discord.errors import HTTPException
from discord.ext.commands.cooldowns import BucketType
from discord.ext.commands.core import is_owner
from discord.message import Message
from mal import *
from dateutil.relativedelta import relativedelta as delt
import requests
import subprocess
from GrabzIt import GrabzItImageOptions
from GrabzIt import GrabzItClient
from osuapi import OsuApi, ReqConnector
import discord,json,datetime,random,os,textwrap
from PIL import Image as img, ImageDraw
from PIL import ImageFont as imgfont
from PIL import ImageDraw as imgdraw
from PIL import ImageOps
from discord.ext import commands,tasks
from discord.ext.commands.errors import BotMissingPermissions, ChannelNotFound, ChannelNotReadable, CheckFailure, CommandInvokeError, CommandNotFound, CommandOnCooldown, EmojiNotFound, MemberNotFound, MissingPermissions, RoleNotFound, UserNotFound
from discord.flags import Intents
from dpymenus import Page, PaginatedMenu
from requests.api import request
import base64
import dbl
import pyshorteners
import qrcode,pymongo
import markdown
import discloud
from didyoumean import didyoumean
### Setando config DYM
didyoumean.threshold = 0.6
#from translate import Translator
intents = intents = discord.Intents.all()
log = ""
ultimafoto={}
vargv={}
dtemp={}
config = dict(json.load(open('config.json','r')))
colDown={}
cl = pymongo.MongoClient(config['mongo'])
db = cl['Usuarios']
users = db['Users']
servers = db['Servers']
blacklist = db['BlackList']
grabzIt = GrabzItClient.GrabzItClient(config['gab1'],config['gab2'])
devs=[771369636906139668,800043671340580894,437679061251391488,563448056125587457,638020094076649493,390654720286392331]
def check(author,messagecheck):
    def inner_check(message):
        if message.author == author:
            if message.content.lower() == messagecheck or message.content.lower() in messagecheck: return True
            else: return False
    return inner_check
verif={
    "low":"Fraco",
    "none":"Fraco",
    "medium":"Medio",
    "high":"Alto",
    "table_flip":"Alto (╯°□°）╯︵ ┻━┻ ",
    "extreme" : "ExTrEmO",
    "double_table_flip":"EXTREMO",
    "very_high":"Extremo"
}
async def Dados(sv) -> json:
    x = servers.find({"_id":sv}).limit(1)
    lis=[]
    for i in x:
        return i
ti = time.time() 
async def UDados(user: discord.User) -> json:
    x = users.find({"_id":user}).limit(1)
    lis=[]
    for i in x:
        return i
osu = OsuApi(config['osu'], connector=ReqConnector())
def prefix(bot,message):
    x = servers.find({"_id":message.guild.id}).limit(1)
    lis=[]
    for i in x:
        lis.append(i)
    return commands.when_mentioned_or(*lis[0]['prefix'])(bot, message)
bot = commands.AutoShardedBot(command_prefix=prefix,case_insensitive=True,intents=intents)
bot.remove_command('help')
epoch = datetime.datetime.utcfromtimestamp(0)
@tasks.loop(seconds=30)
async def blCheck():
    global blacklist
    for i in blacklist.find():
        if datetime.datetime.now() >= i['time']:
            blacklist.delete_one({"_id":i['_id']})
blCheck.start()
@bot.event
async def on_ready():
    await outroloop()
async def listallservers():
    d = []
    for i in servers.find().distinct('_id'):
        d.append(i)
    return d
async def listallusers():
    d = []
    for i in users.find().distinct('_id'):
        d.append(i)
    return d
async def padrao(ctx: object,nomeEmbed: str,name: str,desc: str,como: str,aliases: str,perm: str) -> None:
    if perm == "Staff":
        embed = discord.Embed(title=f'Ajuda de {nomeEmbed}',description=f'Esse painel mostrara como usar o {name}, somente a Staff podem usar esse comando\n\n :question:  **Para que serve?**\n\n {desc}\n\n\n :question: **Quais são os comandos?**\n\n {como} \n\n** :globe_with_meridians: Outros nomes**\n {aliases}')
    else:
        embed = discord.Embed(title=f'Ajuda de {nomeEmbed}',description=f'Esse painel mostrara como usar o {name}, todos podem usar esse comando\n\n :question:  **Para que serve?**\n\n {desc}\n\n\n :question: **Quais são os comandos?**\n\n {como} \n\n** :globe_with_meridians: Outros nomes**\n {aliases}')
    await ctx.send(embed=embed)
async def salvar(dados,id):
    sets = {"$set":dados}
    users.update_one(users.find_one({"_id":id}),sets)
async def salvarS(dados,id):
    sets = {"$set":dados}
    servers.update_one(servers.find_one({"_id":id}),sets)
async def CConta(user: discord.Member):
    if str(user.id) in await listallusers():
        return
    else:
        if user.bot == True:
            return
        users.insert_one({"_id":user.id,'nome':user.name,'mar':0,'desc':'Eu sou uma pessoa misteriosa, mas eu posso mudar minha descrição usando .desc','rep':0,"xp_time":0,'money':0,'gold':0,'inventory':{"Padrão": {"name": "Padrão","desc": "Background padrão","tip": "BackGround Profile","use": True,"cont": 0,"onetime": True,"preview": "https://media.discordapp.net/attachments/776197504378732555/795800876383338496/default.png?width=642&height=459","tipte": "back-pf","author": "SphyX Team"}},'profile':{'back-pf':{'url':'https://media.discordapp.net/attachments/776197504378732555/795800876383338496/default.png?width=642&height=459','name':"Padrão"}}})
async def GCConta(guild: discord.Guild):
    if str(guild.id) in await listallservers():
        return
    else:
        servers.insert_one({"_id":guild.id,'nome':guild.name,'users':{},'config':{'time_xp':30,'role_mute':0,'welcome_channel':0,'leave_channel':0,'mediaxp':10,'WelcomeMsg':'[mention] bem vindo! ','LeaveMsg':'[mention] saiu do servidor!','dmpu':0,'autorole':{},'controle':0,'rr':{},'rrcont':0},'reg':{},'prefix':['.','dasdas'],'contIDreg':0,'automessage':0,'tick':{}})
async def loga(message):
    channel = bot.get_channel(785611411043647578)
    await channel.send('**L O G**\n' + message)   
async def loop():
    while True:
        await asyncio.sleep(60)
        cont=0
        for i in bot.shards:
            await bot.change_presence(activity=discord.Game(name=f".help | Eu estou em {len(bot.guilds)} servidores e monitorando {len(bot.users)} Usuários! Shard {i}/{len(bot.shards)-1} | https://discord.gg/CG7spnTsKa", type=1),shard_id=i)
        contU=0
        a=[]
        contD=0
        s=False
        us = await listallusers()
        sv = await listallservers()
        async for guild in bot.fetch_guilds(limit=None):
            cont+=1
            if guild.id not in sv:
                await GCConta(guild)
            async for member in guild.fetch_members(limit=None): 
               #     dados['Servers'][str(guild.id)]['users'][str(member.id)] = {'warns':0,'ficha':{},'fichamute':{},'contmute':0,'xp':0,'msg':0,'xp_time':0} 
                if member.id not in us:
                    contU += 1      
                    if member.bot == True:
                        pass
                    else:
                        a.append({"_id":member.id,'nome':member.name,'mar':0,'desc':'Eu sou uma pessoa misteriosa, mas eu posso mudar minha descrição usando .desc','rep':0,"xp_time":0,'money':0,'gold':0,'inventory':{"Padrão": {"name": "Padrão","desc": "Background padrão","tip": "BackGround Profile","use": True,"cont": 0,"onetime": True,"preview": "https://media.discordapp.net/attachments/776197504378732555/795800876383338496/default.png?width=642&height=459","tipte": "back-pf","author": "SphyX Team"}},'profile':{'back-pf':{'url':'https://media.discordapp.net/attachments/776197504378732555/795800876383338496/default.png?width=642&height=459','name':"Padrão"}}})
                        s=True

        if s:
            users.insert_many(a)
        channel = bot.get_channel(785611411043647578)
        await channel.send(f'\n------------------\n[{str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))}]\nFoi registrado: {contU} contas\nFoi registrado: {contD} contas de {cont} Servidores"\n------------------\n\n')
        for i in await listallservers():
            d = await Dados(i)
            
            for h in d['users']:
                x = d['users'][h]
                try:
                    if x['mute']=={}:
                        continue
                    else:
                        td = x['mute']['temp'] + delt(seconds=x['mute']['time'])
                        if datetime.datetime.now() >= td:
                            guild: discord.Guild = bot.get_guild(i)
                            try:
                                us: discord.Member = guild.get_member(x['mute']['id'])
                                rol = guild.get_role(d['config']['role_mute'])
                                await us.remove_roles(rol)
                                d['users'][str(x['mute']['id'])]['mute'] = {}
                                await salvarS(d,i)
                            except Exception as e:
                                continue
                except:pass
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
async def bl(id:int):
    try:
        if blacklist.find({"_id":id})[0]['blacklisted'] == True:
            return True
        else:
            return False
    except Exception as ex:
        return False   
async def usou(self,ctx):
    channel = bot.get_channel(785611411043647578)
    await channel.send(embed=discord.Embed(title=ctx.message.guild.name).add_field(name='Quem mandou?',value=ctx.message.author.name).add_field(name='Chat da mensagem',value=ctx.message.channel).add_field(name='Comando',value=ctx.message.content).set_thumbnail(url=ctx.message.author.avatar_url))
def blacklists():
    def checar(ctx):
        try:
            if blacklist.find({"_id":id})[0]['blacklisted'] == True:
                return False
            else:
                return True
        except Exception as ex: 
            return True
    return commands.check(checar)
def blackli(id:int, temp:int):
    blacklist.insert_one({'_id':id, "blacklisted":True,"time":datetime.datetime.now() + delt(seconds=temp)})
class events(commands.Cog): 
    @commands.Cog.listener()
    async def on_ready(self):
        ch = bot.get_channel(785511008533086279)
        await ch.send(embed = discord.Embed(title='Status SPX',description=f'\n\nMessagem: Estou online! Acordei com {int(bot.latency * 1000)}ms...\n\n{"Estou bem rápido para responder comandos... <:doglushed:798290013468360734>  " if int(bot.latency *1000) < 40 else "Posso demorar um pouco para responder os comandos... :pensive:"}'))
        print('.................')
        print('Sphyx está ligado!')
        print('.................')
        print('       LOG       ')
        print('                 ')
        for i in bot.shards:
            await bot.change_presence(activity=discord.Game(name=f".help | Eu estou em {len(bot.guilds)} servidores e monitorando {len(bot.users)} Usuários! Shard {i}/{len(bot.shards)-1} | https://discord.gg/CG7spnTsKa", type=1),shard_id=i)
    @commands.Cog.listener()
    async def on_message(self,message):
        try:
            global ultimafoto
            yeah = message.attachments
            try:
                if yeah[0].size > 0:
                    if 'png' or 'jpeg' in yeah[0].filename:
                        ultimafoto[message.guild.id]= yeah
            except IndexError:
                pass
        except TypeError as error:
            await loga(f'Evento: ON_MESSAGE | Conteudo da mensagem: {message.content}\nERRO NO SERVIDOR {message.guild.name} : '+ error)
        if message.author.bot != True:
            dados = await Dados(message.guild.id)
            '''dadosU = await UDados(message.author.id)
            var = None
            config = dados['config']'''
            if  message.content == f"<@!{bot.user.id}>" or message.content == f"<@{bot.user.id}>":
                await message.reply(f":question: | `{dados['prefix'][0] if dados['prefix'][1] == 'dasdas' else dados['prefix'][1]}help` **<- Comando de ajuda**")
            '''xp = dados['users'][str(message.author.id)]['xp']
            dados['users'][str(message.author.a id)]['msg'] += 1'''
            user = message.author
            if user.id in await listallusers():
                pass
            else:
                await CConta(user)
            #time_diff = (datetime.datetime.utcnow() - epoch).total_seconds() - dados['Servers'][str(message.guild.id)]['users'][str(message.author.id)]['xp_time']
            #if time_diff >= config['time_xp']:
                   #dados['Servers'][str(message.guild.id)]['users'][str(message.author.id)]['xp'] += int(randrange(int(int(config['mediaxp']) /2),int(int(config['mediaxp']))))
                   #dados['Servers'][str(message.guild.id)]['users'][str(message.author.id)]['xp_time'] = (datetime.datetime.utcnow() - epoch).total_seconds()'''
    @commands.Cog.listener()
    async def on_guild_join(self,guild):
        lo = await guild.audit_logs(action=discord.AuditLogAction.bot_add).flatten()
        use = lo[0].user
        await use.send("Obrigado por me adicionar!\n\nEu tenho algumas informações que podem ser úteis para você, caso queira configurar o seu servidor você usa o comando `.config` que ele vai listar todos os comandos e como usar cada um, enfim muito obrigado por me adicionar!\n\nVocê pode tentar ir no meu discord oficial! -> https://discord.gg/CG7spnTsKa \nOu ver os meus comandos -> https://tinyurl.com/y99phkrp")
        await bot.get_user(563448056125587457).send(f"Arrombado entrei no servidor: {guild.name} | Membros: {len(guild.members)} | Dono: {guild.owner.name}")
        dados = await Dados(guild.id)
        user={}
        lista=[]
        fi = False
        if guild.id in await listallservers():
            await use.send("Pelo que eu vi aqui parece que eu já entrei nesse servidor, todas as configurações que estavam antes foram aplicados agora...")
            return
        await GCConta(guild)
        async for i in guild.fetch_members(limit=None):
            if i.bot != True:
                #dados['Servers'][str(guild.id)]['users'][str(i.id)] = {'warns':0,'ficha':{},'fichamute':{},'contmute':0,'xp':0,'msg':0,'xp_time':0}
                #print(dados['Servers'][str(guild.id)]['users'][str(i.id)])
                if str(user.id) in await listallusers():
                    continue
                else:
                    if user.bot == True:
                        pass
                    else:
                        fi = True
                        lista.append({"_id":i.id,'nome':user.name,'mar':0,'desc':'Eu sou uma pessoa misteriosa, mas eu posso mudar minha descrição usando .desc','rep':0,"xp_time":0,'money':0,'gold':0,'inventory':{"Padrão": {"name": "Padrão","desc": "Background padrão","tip": "BackGround Profile","use": True,"cont": 0,"onetime": True,"preview": "https://media.discordapp.net/attachments/776197504378732555/795800876383338496/default.png?width=642&height=459","tipte": "back-pf","author": "SphyX Team"}},'profile':{'back-pf':{'url':'https://media.discordapp.net/attachments/776197504378732555/795800876383338496/default.png?width=642&height=459','name':"Padrão"}}})
        if fi:
            users.insert_many(lista)
        await bot.change_presence(activity=discord.Game(name=f".help | Eu estou em {len(bot.guilds)} servidores e {len(bot.users)} Usuários!", type=1))
    @commands.Cog.listener()
    async def on_member_join(self,member: discord.Member):
        dados = await Dados(member.guild.id)
        try:
            if (datetime.datetime.now() - delt(days=1) - member.created_at).days*-1 >= dados['antialt']['day']:
                print(dados['antialt']['day'])
                #await member.ban()
                return
        except:pass
        for i in dados['config']['autorole']:
            role = member.guild.get_role(dados['config']['autorole'][i]['roleid'])
            await member.add_roles(role)
        mensagem = dados['config']['WelcomeMsg']
        mensagem = mensagem.replace('[mention]',member.mention)
        mensagem = mensagem.replace('[user]',member.name)
        mensagem = mensagem.replace('[usertag]',member.name + '#' + member.discriminator)
        mensagem = mensagem.replace('[guildname]',member.guild.name)
        channel = bot.get_channel(int(dados['config']['welcome_channel']))        
        await channel.send(mensagem)
        try:
            await CConta(member)
        except:pass
        #dados['users'][str(member.id)] = {'warns':0,'ficha':{},'fichamute':{},'contmute':0,'xp':0,'msg':0,'xp_time':0} 
        if dados['config']['automessage'] != 0:
            mensagem = dados['config']['automessage']
            mensagem = mensagem.replace('[mention]',member.mention)
            mensagem = mensagem.replace('[user]',member.name)
            mensagem = mensagem.replace('[usertag]',member.name + '#' + member.discriminator)
            mensagem = mensagem.replace('[guildname]',member.guild.name)
            await member.send(f'Mensagem enviada do servidor {member.guild.name};\n'+mensagem)    
        try: evt = dados['config']['eventlog']
        except KeyError:return
        if evt['chid'] != None:
            if evt['newmemb']:
                ch: GuildChannel = bot.get_guild(member.guild.id).get_channel(evt['chid'])
                embed = discord.Embed(title=f'Novo membro {member.name}.')
                embed.add_field(name='Membro', value=member.name)
                embed.timestamp = datetime.datetime.now()
                embed.set_thumbnail(url=member.author.avatar_url)
    @commands.Cog.listener()
    async def on_member_remove(self,member):
        dados = await Dados(member.guild.id)
        mensagem = dados['config']['LeaveMsg']
        mensagem = mensagem.replace('[mention]',member.mention)
        mensagem = mensagem.replace('[user]',member.name)
        mensagem = mensagem.replace('[usertag]',member.name + '#' + member.discriminator)
        mensagem = mensagem.replace('[guildname]',member.guild.name)
        channel = bot.get_channel(int(dados['config']['leave_channel'] if dados['config']['leave_channel'] != 0 else dados['config']['welcome_channel']))        
        try:await channel.send(mensagem)
        except:pass
        try: evt = dados['config']['eventlog']
        except KeyError:return
        if evt['chid'] != None:
            if evt['leftmemb']:
                ch: GuildChannel = bot.get_guild(member.guild.id).get_channel(evt['chid'])
                embed = discord.Embed(title=f'O Membro {member.name} saiu.')
                embed.add_field(name='Membro', value=member.name)
                embed.timestamp = datetime.datetime.now()
                embed.set_thumbnail(url=member.avatar_url)
    ######################## EVENT LOG
    @commands.Cog.listener()
    async def on_message_delete(self,message: Message):
        dados = await Dados(message.guild.id)
        try:evt = dados['config']['eventlog']
        except KeyError:return
        if evt['msgdel'] == False:
            return
        else:
            if evt['chid'] != None:
                ch: GuildChannel = bot.get_guild(message.guild.id).get_channel(evt['chid'])
                embed = discord.Embed(title=f'Mensagem apagada por {message.author.name}.')
                embed.add_field(name='Canal', value=message.channel.mention)
                embed.add_field(name='Mensagem', value=message.content)
                embed.timestamp = datetime.datetime.now()
                embed.set_thumbnail(url=message.author.avatar_url)
                await ch.send(embed=embed)
    @commands.Cog.listener()
    async def on_bulk_message_delete(self,messages):
        dados = await Dados(messages[0].guild.id)
        try:evt = dados['config']['eventlog']
        except IndexError:return
        if evt['msgdel'] == False:
            return
        else:
            if evt['chid'] != None:
                msg = ''
                for i in messages:
                    msg = msg + i.content 
                req = requests.post('https://hastebin.com/documents',data=msg)
                key = json.loads(req.content)   
                ch: GuildChannel = bot.get_guild(messages[0].guild.id).get_channel(evt['chid'])
                embed = discord.Embed(title=f'Mensagens apagada por {messages[0].author.name}.')
                embed.add_field(name='Canal', value=messages[0].channel.mention)
                embed.add_field(name='Mensagens', value=f'https://hastebin.com/{key["key"]}')
                embed.timestamp = datetime.datetime.now()
                embed.set_thumbnail(url=messages[0].author.avatar_url)
                await ch.send(embed=embed)
    @commands.Cog.listener()
    async def on_message_edit(self,message,dps):
        if message.content == dps.content:
            return
        dados = await Dados(message.guild.id)
        try:evt = dados['config']['eventlog']
        except IndexError:return
        if evt['editmsgs'] == False:
            return
        else:
            if evt['chid'] != None:
                ch: GuildChannel = bot.get_guild(message.guild.id).get_channel(evt['chid'])
                embed = discord.Embed(title=f'Mensagem editado por {message.author.name}.')
                embed.add_field(name='Canal', value=message.channel.mention)
                embed.add_field(name='Antes', value=message.content)
                embed.add_field(name='Depois', value=dps.content)
                embed.timestamp = datetime.datetime.now()
                embed.set_thumbnail(url=message.author.avatar_url)
                await ch.send(embed=embed)
    @commands.Cog.listener()
    async def on_member_ban(self,guild,user):
        dados = await Dados(guild.id)
        try:evt = dados['config']['eventlog']
        except IndexError:return
        if evt['leftmemb'] == False:
            return
        else:
            if evt['chid'] != None:
                ch: GuildChannel = bot.get_guild(guild.id).get_channel(evt['chid'])
                embed = discord.Embed(title=f'Membro banido {user.name}.')
                embed.add_field(name='Membro', value=user.name)
                embed.timestamp = datetime.datetime.now()
                embed.set_thumbnail(url=user.avatar_url)
                await ch.send(embed=embed)
    @commands.Cog.listener() 
    async def on_member_unban(self,guild,user):
        dados = await Dados(guild.id)
        try:evt = dados['config']['eventlog']
        except IndexError:return
        if evt['leftmemb'] == False:
            return
        else:
            ch: GuildChannel = bot.get_guild(guild.id).get_channel(evt['chid'])
            embed = discord.Embed(title=f'Usuario desbanido: {user.name}.')
            embed.add_field(name='Membro', value=user.name)
            embed.timestamp = datetime.datetime.now()
            embed.set_thumbnail(url=user.avatar_url)
            await ch.send(embed=embed)
    @commands.Cog.listener()
    async def on_command_error(self,ctx,error):
        if await bl(ctx.author.id) == True:return
        elif isinstance(error, MissingPermissions):
            await ctx.send(':x: | **Você não tem permissão para fazer isso...**')
        elif isinstance(error, MemberNotFound):
            await ctx.send(":x: | **Eu não consegui achar esse membro.**")
        elif isinstance(error, ChannelNotFound):
            await ctx.send(":x: | **Não consegui encontrar esse canal...**")
        elif isinstance(error, UserNotFound):
            await ctx.send(":x: | **Eu não consegui encontrar essa pessoa**")
        elif isinstance(error, ChannelNotReadable):
            await ctx.send(":x: | **Não consigo mandar mensagens no canal!**")
        elif isinstance(error, MissingPermissions):
            await ctx.send(":x: | **Eu não tenho permissões para fazer isso...**")
        elif isinstance(error, CommandOnCooldown):
            
            if ctx.command.name == 'daily':return
            elif ctx.author.id not in colDown:
                colDown[ctx.author.id] = {ctx.command.name:{'es':datetime.datetime.now() + delt(seconds=error.retry_after),'vz':0}}
            else:
                if ctx.command.name not in colDown[ctx.author.id]:
                    colDown[ctx.author.id][ctx.command.name] = {'es':datetime.datetime.now() + delt(seconds=error.retry_after),'vz':0} 

                colDown[ctx.author.id][ctx.command.name]['vz'] += 1
                error.cooldown.per += 10
                error.retry_after += 10
            if error.cooldown.per >= 50:
                try:
                    blackli(ctx.author.id,648000)
                    await ctx.send(":x: | **Sua conta foi banida por quebrar as regras do SphyX**\n**Motivo:** Flood de CMDs\n**Duração:** 3 Dias...")
                except:return
            else:await ctx.send(f":x: | **Espere {int(error.retry_after)} segundos para usar o comando novamente**")
        elif isinstance(error, CommandNotFound):
            if ctx.invoked_with == f"<@!{bot.user.id}>" or ctx.invoked_with == f"<@{bot.user.id}>":
                a = bot.get_command('ping')
                await a.__call__(ctx)
                return
            a = didyoumean.didYouMean(ctx.invoked_with.lower(),A)
            if a == None:return
            msg = await ctx.send(f":question: | Você quis dizer... **{a}**?")
            await msg.add_reaction('✅')
            def checkr(reaction,user):
                return user == ctx.message.author and reaction.emoji == '✅' and msg.id == reaction.message.id
            try:
                await bot.wait_for('reaction_add',check=checkr,timeout=15)
                b = bot.get_command(a)
                await b.__call__(ctx,**ctx.kwargs)
            except asyncio.TimeoutError:
                await msg.clear_reaction('✅') 
        elif isinstance(error, EmojiNotFound):
            await ctx.send(":x: | **Eu não encontrei esse emoji")   
        elif isinstance(error, CheckFailure):
            return
        else:
            await ctx.send(f":x: | **Aconteceu um erro inesperado...** ```{error.args}```Você pode reportar esse erro no servidor de suporte...")
bot.add_cog(events(bot))  
async def shop() -> dict:
    with open('shop.json','r',encoding='utf-8') as f:
        return dict(json.load(f)) 
A = []
for i in os.listdir('./commands'):
    if i.endswith(".py"):
        bot.load_extension('commands.'+i.replace(".py",''))
        print(f"Arquivo: {i} | Carregado com sucesso!")
for i in bot.commands:
    A.append(i.name)
    for x in i.aliases:
        A.append(x)

bot.run(config['token'])