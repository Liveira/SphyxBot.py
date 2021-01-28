import sys
sys.path.append('..')
from main import *
class config(commands.Cog):
        @commands.group(name='config',aliases=['cfg','configurar','cf'],invoke_without_command=True)
        @commands.before_invoke(usou)
        @commands.cooldown(1,5,commands.BucketType.member)
        async def cmdconfig(self,ctx):
            if await bl(ctx.author.id) == True:
                return
            embed = discord.Embed(title='Ajuda de configuração',description="""Esse painel mostrara como usar o config, somente pessoas com a permissão "Administrador" pode usar esse comando\n \n:question: **Para que serve?**\nServe para mudar, intervalo de XP, Media de XP, Configurações de canais de MUTE, Canal de bem vindo e etc...\n\n:question: **Quais são os comandos?**\n`xp-time` -> Muda o tempo de CoolDown de XP\n`mute-role` -> Mudar o cargo de mute\n`welcome-channel` -> Muda o chat para mandar as mensagem de bem vindo\n`welcome-msg` -> Muda a mensagem de bem vindo\n`leave-msg` -> Muda a mensagem de saida do membro\n`media-xp` -> Muda a media de xp que o usuario ganha no servidor\n`autorole` -> Quando um membro entra no servidor ele dá esse cargo automaticamente\n`slowmode` -> Muda o CoolDown de mensagems do chat\n`prefix` -> Muda o prefixo do bot\n`dmpu` -> Manda a mensagem na DM do usuario que foi punido\n`automessage` -> quando um usuario entra no servidor essa mensagem vai ser enviada no DM automaticamente do membro\n\n:grey_question: **Perguntas Frequentes**\n**Como eu tiro o sistema de "Bem Vindo/ AutoRole" ?** : Use o comando **del**, por exemplo "`del config welcome-channel`"\n\n**__Comandos que já tem essa função__**: \n`media-xp` <Desativa o XP por completo>\n`welcome-channel` <Desativa a mensagem de Boas Vindas por completo>\n\n**Ainda ficou com dúvida?** Entre no servidor de suporte do SphyX 'https://discord.gg/hReae7c67G'\n\n:globe_with_meridians: **Outros nomes**\n```cfg | config | configurar | cf```""")
            await ctx.send(embed=embed)            
        @cmdconfig.command(name='xp-time')
        @commands.has_permissions(kick_members=True)
        @commands.cooldown(1,5,commands.BucketType.member)
        async def xp_time(self,ctx,novo_valor: int=None):
            if novo_valor == None:
                await padrao(ctx,'configuração','xp-time','Serve para mudar o tempo de cooldown para ganhar o XP','`xp-time <Novo Valor: SEGUNDOS>*` -> Muda o CoolDown de XP','```xp-time```','Staff')
                #ctx: object,nomeEmbed: str,name: str,desc: str,como: str,aliases: str,perm: str)
            else:
                dados = await Dados(ctx.guild.id)
                ant = dados['config']['time_xp']
                dados['config']['time_xp'] = int(novo_valor)
                await ctx.send(f":question:  | **Tempo de CoolDown alterado para {novo_valor}!**")
                dados['contIDreg'] += 1
                cont = dados['contIDreg']
                dados['reg'][str(cont)] = {
                            'tipo':'XP_TIME',
                            'anVal':ant,
                            'dpVal':int(novo_valor),
                            'QmMd':ctx.author.name 
                }
                await salvarS(dados,ctx.guild.id)
                global log
                log = log + "\n" + f"XP_TIME alterado para {novo_valor} no servidor {ctx.guild.name}"
        @cmdconfig.command(name='mute-role')
        @commands.has_permissions(kick_members=True)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def mute_role(self,ctx,novo_cargo: discord.Role=None):
            if novo_cargo == None:
                await padrao(ctx,'configuração','mute-role','Serve para mudar o cargo de mute do servidor','`mute-role <Novo Valor: CARGO>*` -> Muda o cargo de mute','```mute-role```','Staff')
                #ctx: object,nomeEmbed: str,name: str,desc: str,como: str,aliases: str,perm: str)
            else:
                dados = await Dados(ctx.guild.id)
                ant = dados['config']['role_mute']
                dados['config']['role_mute'] = int(novo_cargo.id)
                await ctx.send(f":question:  | **Cargo de mute foi mudado para: {novo_cargo}!**")
                dados['contIDreg'] += 1
                cont = dados['contIDreg']
                dados['reg'][str(cont)] = {
                            'tipo':'MUTE_ROLE',
                            'anVal':ant,
                            'dpVal':int(novo_cargo.id),
                            'QmMd':ctx.author.name 
                }
                await salvarS(dados,ctx.guild.id)
                global log
                log = log + "\n" + f"MUTE_ROLE Alterado para {novo_cargo.name} no servidor {ctx.guild.name}"
        @cmdconfig.command(name='welcome-msg')
        @commands.has_permissions(kick_members=True)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def welcome_msg(self,ctx,*,novo_valor: str=None):
            if novo_valor == None:
                #ctx: object,nomeEmbed: str,name: str,desc: str,como: str,aliases: str,perm: str) 
                embed = discord.Embed(title='Ajuda de configuração',description='Esse painel mostrara como usar o welcome-msg, somente pessoas com a permissão "Administrador" pode usar esse comando\n\n :question:  **Para que serve?**\n\nServe para mudar a mensagem de boas vindas!\n\n\n :question: **Quais são os comandos?**\n\n`welcome-msg <nova mensagem>`\n\n:newspaper: **Guia**\n[mention] -> Menciona o usuario na mensagem\n[user] -> Coloca o nome do usuario (sem marcar)\n[usertag] -> Coloca o nome do usuario junto com a tag EX: NightterX#0311\n[guildname] -> Coloca o nome do servidor\n\n :globe_with_meridians: **Outros nomes**\n\n ```welcome-msg```')
                await ctx.send(embed=embed)
            else:
                dados = await Dados(ctx.guild.id)
                member = ctx.author
                ant = dados['config']['WelcomeMsg']
                dados['config']['WelcomeMsg'] = novo_valor
                dados['contIDreg'] += 1
                cont = dados['contIDreg']
                dados['reg'][str(cont)] = {
                            'tipo':'WELCOME_MESSAGE',
                            'anVal':ant,
                            'dpVal':novo_valor,
                            'QmMd':ctx.author.name 
                }
                await salvarS(dados,ctx.guild.id)
                global log
                log = log + "\n" + f"WELCOME_MESSAGE Alterado para {novo_valor} no servidor {ctx.guild.name}"
                mensagem = dados['config']['WelcomeMsg']
                mensagem = mensagem.replace('[mention]',member.mention)
                mensagem = mensagem.replace('[user]',member.name)
                mensagem = mensagem.replace('[usertag]',member.name + '#' + member.discriminator)
                mensagem = mensagem.replace('[guildname]',member.guild.name)
                await ctx.send(f":question:  | **A mensagem de boas vindas foi mudado para: {novo_valor}!\nSua mensagem ficou assim: {mensagem}**")
        @cmdconfig.command(name='leave-msg')
        @commands.has_permissions(kick_members=True)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def leave_msg(self,ctx,*,novo_valor: str=None):
            if novo_valor == None:
                #ctx: object,nomeEmbed: str,name: str,desc: str,como: str,aliases: str,perm: str) 
                embed = discord.Embed(title='Ajuda de configuração',description='Esse painel mostrara como usar o leave-msg, somente pessoas com a permissão "Administrador" pode usar esse comando\n\n :question:  **Para que serve?**\n\nServe para mudar a mensagem de boas vindas!\n\n\n :question: **Quais são os comandos?**\n\n`leave-msg <nova mensagem>`\n\n:newspaper: **Guia**\n[mention] -> Menciona o usuario na mensagem\n[user] -> Coloca o nome do usuario (sem marcar)\n[usertag] -> Coloca o nome do usuario junto com a tag EX: NightterX#0311\n[guildname] -> Coloca o nome do servidor\n\n :globe_with_meridians: **Outros nomes**\n\n ```leave-msg```')
                await ctx.send(embed=embed)
            else:
                dados = await Dados(ctx.guild.id)
                member = ctx.author
                ant = dados['config']['LeaveMsg']
                dados['config']['LeaveMsg'] = novo_valor
                dados['contIDreg'] += 1
                cont = dados['contIDreg']
                dados['reg'][str(cont)] = {
                            'tipo':'LEAVE_MESSAGE',
                            'anVal':ant,
                            'dpVal':novo_valor,
                            'QmMd':ctx.author.name 
                }
                await salvarS(dados,ctx.guild.id)
                global log
                log = log + "\n" + f"LEAVE_MESSAGE Alterado para {novo_valor} no servidor {ctx.guild.name}"
                mensagem = dados['config']['LeaveMsg']
                mensagem = mensagem.replace('[mention]',member.mention)
                mensagem = mensagem.replace('[user]',member.name)
                mensagem = mensagem.replace('[usertag]',member.name + '#' + member.discriminator)
                mensagem = mensagem.replace('[guildname]',member.guild.name)
                await ctx.send(f":question:  | **A mensagem de saida foi mudado para: {novo_valor}!\nSua mensagem ficou assim: {mensagem}**")
        @cmdconfig.command(name='welcome-channel')
        @commands.has_permissions(kick_members=True)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def welcome_channel(self,ctx,novo_canal: discord.TextChannel=None):
            if novo_canal == None:
                await padrao(ctx,'Moderação','welcome-channel','Muda o canal que o bot manda a mensagem de boas vindas! Caso não queira mais mensagems de boas vindas, só não faça nada','`welcome-channel <canal de texto>*` -> Muda o canal de boas vindas','welcome-channel','Staff')       
            else:
                dados = await Dados(ctx.guild.id)
                ant = dados['config']['welcome_channel']
                dados['config']['welcome_channel'] = int(novo_canal.id)
                dados['contIDreg'] += 1
                cont = dados['contIDreg']
                dados['reg'][str(cont)] = {
                            'tipo':'WELCOME_CHANNEL',
                            'anVal':ant,
                            'dpVal':novo_canal.id,
                            'QmMd':ctx.author.name 
                }
                await salvarS(dados,ctx.guild.id)
                global log
                log = log + "\n" + f"WELCOME_CHANNEL Alterado para {novo_canal.name} no servidor {ctx.guild.name}"
                await ctx.send(f":question:  | **Canal alterado para {novo_canal}**")
        @cmdconfig.command(name='media-xp')
        @commands.has_permissions(kick_members=True)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def media_xp(self,ctx,novo_valor=None):
            if novo_valor == None:
                await padrao(ctx,'Moderação','media-xp','Muda a media de Xp que o usuario ganha no servidor','`media-xp <xp>*` -> Muda a media de xp','media-xp','Staff')       
            else:
                dados = await Dados(ctx.guild.id)
                ant = dados['config']['mediaxp']
                dados['config']['mediaxp'] = int(novo_valor)
                dados['contIDreg'] += 1
                cont = dados['contIDreg']
                dados['reg'][str(cont)] = {
                            'tipo':'AVERAGE_XP',
                            'anVal':ant,
                            'dpVal':novo_valor,
                            'QmMd':ctx.author.name 
                }
                await salvarS(dados,ctx.guild.id)
                global log
                log = log + "\n" + f"AVERAGE_XP Alterado para {novo_valor} no servidor {ctx.guild.name}"
                await ctx.send(f":question:  | **A Media de XP foi alterada para {novo_valor}**")
        @cmdconfig.command(name='slowmode',aliases=['slow','cd','cooldown'])
        @commands.has_permissions(kick_members=True)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def slowmode(self,ctx,chat: discord.TextChannel=None,tempo=0):
            if chat == None:
                await padrao(ctx,'Moderação','slowmode','Muda o tempo de cooldown de um chat em especifico sem limites','`slowmode <chat>* tempo*` -> Muda o tempo de CoolDown de um chat','``` slowmode | slow | cd | cooldown```','Staff')
                #ctx: object,nomeEmbed: str,name: str,desc: str,como: str,aliases: str,perm: str)
    
            else:
                await chat.edit(slowmode_delay = int(tempo))
                dados = await Dados(ctx.guild.id)
                cont = dados['contIDreg']
                dados['reg'][str(cont)] = {
                            'tipo':'SLOWMODE_CHANGE',
                            'dpVal':int(tempo),
                            'QmMd':ctx.author.name 
                }
                await salvarS(dados,ctx.guild.id)
                await ctx.send(f":question:  | **O CoolDown do chat {chat} foi alterado para {tempo}**")
                global log
                log = log + "\n" + f"SLOWMODE Alterado para {tempo} no servidor {ctx.guild.name}"
        @cmdconfig.command(name='prefix',aliases=['prefixo'])
        @commands.has_permissions(kick_members=True)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def prefix(self,ctx,prefix=None):
            if prefix != None:
                dados = await Dados(ctx.guild.id)
                
                if prefix in dados['prefix']:
                    await ctx.send(":warning: | **Já tem esse prefixo**")
                else:
                    dados['prefix'][1] = prefix
                    cont = dados['contIDreg']
                    dados['reg'][str(cont)] = {
                            'tipo':'PREFIX_CHANGE',
                            'dpVal':prefix,
                            'QmMd':ctx.author.name 
                }
                    await salvarS(dados,ctx.guild.id)
                    global log
                    log = log + "\n" + f"AVERAGE_XP Alterado para {prefix} no servidor {ctx.guild.name}"
                    await ctx.send(f":question: | **Prefixo alterado para \"{prefix}\" **")
            else:
                await padrao(ctx,"Moderação",'prefix','Muda o prefixo do bot do servidor! Mude para oque quiser letras e etc...','`prefix <novo prefixo>*`  ','```prefix | prefixo```','Staff')
        @cmdconfig.group(name='autorole',invoke_without_command=True)
        @commands.has_permissions(kick_members=True)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def cmdautorole(self,ctx,role: discord.Role=None):
                await padrao(ctx,'Moderação','autorole','Da um cargo automatico quando a pessoa entra no servidor','`add <cargo>*` -> Muda o cargo de Autorole\n`edit <index> <cargo>* <novo index>` -> Edita a posição do cargo\n`list` -> lista todos as autoroles','```autorole```','Staff')
        @cmdautorole.command(name='add',aliases=['adicionar'])
        @commands.has_permissions(kick_members=True)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def add(self,ctx,role: discord.Role=None):
            if role == None:
                await padrao(ctx,'Moderação','add autorole','Serve para adicionar um cargo automatico!','`add <cargo>*` -> Adiciona um cargo no autorolelist','```add```',"Staff")
            else:
                dados = await Dados(ctx.guild.id)
                dados['config']['controle'] += 1
                cont = dados['config']['controle']
                dados['config']['autorole'][str(cont)] = {
                    'roleid':role.id
                }
                cont = dados['contIDreg']
                dados['reg'][str(cont)] = {
                            'tipo':'AUTOROLE_CHANGE',
                            'dpVal':role.id,
                            'QmMd':ctx.author.name 
                }
                await salvarS(dados,ctx.guild.id)
                await ctx.send(":question: | **Um cargo de autorole foi adicionado**")
        @cmdautorole.command(name='list',aliases=['listar'])
        @commands.has_permissions(kick_members=True)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def list(self,ctx):
            dados = await Dados(ctx.guild.id)
            msg=""
            for i in dados["config"]['autorole']:
                role = ctx.guild.get_role(dados["config"]['autorole'][str(i)]['roleid'])
                msg = msg + "\n" + str(i) +"  -  "+  role.name
            embed=discord.Embed(title='Lista do AutoRole',description='Aqui vai mostrar todos os cargos em ordem que estão no seu autorole')
            embed.add_field(name='INDEX    |     CARGO  ',value=f'```\n{msg}```')
            embed.set_footer(text='Está gostando do SphyX? Doe! .donate ',icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        @cmdautorole.command(name='remove',aliases=['remover'])
        @commands.has_permissions(kick_members=True)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def remover(self,ctx,index=None):
            if index == None:
                await padrao(ctx,'Moderação','autorole remove','Serve para tirar um cargo de um autorole, coloque o index do cargo que você quer remover e pronto!','`autorole remove <index autorole>`','```remove | remover```','Staff')
            else:
                dados = await Dados(ctx.guild.id)
                try:
                    ant = dados['config']['autorole'][index]['roleid']
                    del dados['config']['autorole'][index]
                except KeyError:
                    await ctx.send(":x: | **Você colocou um Index inválido, para saber os index de cada cargo use o \"config autorole list\"**")    
                    return
                await salvarS(dados,ctx.guild.id)
                role = ctx.guild.get_role(ant)
                await ctx.send(f":question: | **Pronto! O Cargo {role.name}**")
        @cmdconfig.command(name='des',aliases=['desativar','del'])
        @commands.has_permissions(kick_members=True)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def des(self,ctx,tipo=None):
            if tipo == None:
                await padrao(ctx,'Moderação','des','Desativa uma função do bot, seja ele autorole, mensagems de boas vindas e entre outros...','`des <tipo>*` -> Desativa a função de acordo com o tipo que você digitou!\n**Tipos existentes**\nwelcome-channel -> Desativa as mensagems de boas vindas\nautorole -> Desativa o autorole\nmedia-xp -> Desativa o xp','```des | desativiar | del```','Staff')
            else:
                tipo = tipo.replace("-","_")
                dados = await Dados(ctx.guild.id)
                if not tipo in dados['config']:
                    await ctx.send(":x: | **Tipo invalido!**")
                else:
                    dados['config'][tipo] = 0
                    await ctx.send(f":question:  | **A função {tipo} foi desativado(a)**")
                await salvarS(dados,ctx.guild.id)
        @cmdconfig.command(name='dmpu')
        @commands.has_permissions(kick_members=True)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def dmpu(self,ctx,tipo=None):
            if tipo == None:
                await padrao(ctx,'Moderação','dmpu','Quando ativado o usuario que levou algum tipo de punição por exemplo Warn, o bot vai diretamente no DM dele avisar','`dmpu ativar ou desativar` -> Desativa ou Ativa a mensagem de punição na DM','```dmpu```','Staff')
            else: 
                tipo = tipo.lower()
                dados = await Dados(ctx.guild.id)
                if tipo == 'ativar':
                    dados['config']['dmpu'] = 1
                    await ctx.send(":question: | **Mensagems de punição na DM foram ativados**")
                elif tipo == 'desativar':
                    dados['config']['dmpu'] = 0
                    await ctx.send(":question: | **Mensagems de punição na DM foram desativados**")
                else:
                    await ctx.send(":x: | **Use `ativar` ou `desativar`**")
                await salvarS(dados,ctx.guild.id)
        @cmdconfig.command(name='automessage')
        @commands.has_permissions(kick_members=True)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def atmessage(self,ctx,*,nova_mensagem=None):
            if nova_mensagem == None:
                await padrao(ctx,'Moderação','automessage','Quando ativo os proximos membros que entrarem no servidor vão receber uma mensagem de boas vindas escrito por você!','`automessage <nova_mensagem>*`','```automessage```','Staff')
            else:
                dados = await Dados(ctx.guild.id)
                dados['config']['automessage'] = nova_mensagem
                cont = dados['contIDreg']
                dados['reg'][cont] = {
                            'tipo':'AUTO_MESSAGE',
                            'dpVal':nova_mensagem,
                            'QmMd':ctx.author.name 
                }
                await salvarS(dados,ctx.guild.id)
                global log
                log = log + "\n" + f"AVERAGE_XP Alterado para {prefix} no servidor {ctx.guild.name}"
        @cmdconfig.command(name='leave-channel')
        @commands.has_permissions(kick_members=True)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def leave_channel(self,ctx,novo_canal: discord.TextChannel=None):
            if novo_canal == None:
                await padrao(ctx,'Moderação','leave-channel','Muda o canal que o bot manda a mensagem de saida!','`leave-channel <canal de texto>*` -> Muda o canal de saida','leave-channel','Staff')       
            else:
                dados = await Dados(ctx.guild.id)
                ant = dados['config']['leave_channel']
                dados['config']['leave_channel'] = int(novo_canal.id)
                dados['contIDreg'] += 1
                cont = dados['contIDreg']
                dados['reg'][str(cont)] = {
                            'tipo':'LEAVE_CHANNEL',
                            'anVal':ant,
                            'dpVal':novo_canal.id,
                            'QmMd':ctx.author.name 
                }
                await salvarS(dados,ctx.guild.id)
                global log
                log = log + "\n" + f"LEAVE_CHANNEL Alterado para {novo_canal.name} no servidor {ctx.guild.name}"
                await ctx.send(f":question:  | **Canal alterado para {novo_canal}**")
def setup(self):
    bot.add_cog(config(bot))