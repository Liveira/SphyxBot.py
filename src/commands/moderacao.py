import sys
sys.path.append('..')
from main import *
class mod(commands.Cog):
    @commands.group(name='warn' ,aliases=['avisar'] , invoke_without_command=True)
    @commands.has_permissions(kick_members=True)
    @commands.before_invoke(usou)
    @commands.cooldown(1,5,commands.BucketType.member)
    async def cmdwarn(self, ctx, user: discord.Member=None, *, Motivo='Não especificado'):
        if await bl(ctx.author.id) == True:
            return
        elif user == None:
            await padrao(ctx,'Moderação','warn','Serve para avisar membros, quando se usa em uma pessoa, é registrado +1 warn nos registro do usuario','`warn <user>* <motivo>` -> Serve para avisar o usuario\n`list <user>*` -> Serve para ver o registro de warns, motivo, e quem deu warn\n`edit <user> <motivo>` -> Serve para alterar o motivo do warn','```warn | avisar```','Staff')
        elif user.id == ctx.author.id:
            await ctx.send(":x: | **Você não pode se \"Auto avisar\"**")
            return
        elif user.top_role >= ctx.author.top_role:
            await ctx.send(":x: | **Seu cargo está abaixo do usuario**")
            return
        else:
            dados = await Dados(ctx.guild.id)
            userID = user.id
            if str(user.id) not in dados['users']:
                dados['users'][str(user.id)] = {'warns':0,'ficha':{},'fichamute':{},'contmute':0} 
            dados['users'][str(userID)]['warns'] += 1
            cont = dados['users'][str(userID)]['warns']
            dados['users'][str(userID)]['ficha'][str(cont)] = {
                "Motivo":Motivo,
                "ID":cont,
                "Staff":ctx.author.name
            }
            await salvarS(dados,ctx.guild.id)
            await ctx.send(f'{user.name} Levou warn, motivo: {Motivo}, Já é o {cont}° Warn que ele já tem')
            if dados['config']['dmpu'] == 0:
                pass
            else:
                await user.send(f"Você tomou warn, motivo: {Motivo}, evite o maximo levar warn.")
            await loga(f'{user.name} levou warn no servidor {ctx.guild.name}, motivo {Motivo}')
    @cmdwarn.command(name='check',aliases=['list'])
    @commands.has_permissions(kick_members=True)
    @commands.cooldown(1,5,commands.BucketType.member)
    async def check(self,ctx,user: discord.Member=None):
        if user == None:
            await padrao(ctx,'Moderação','list','Serve para listar todos os warns de um determinado membro, alem de listar, ele mostra todas as informações que podem ser úteis!','```warn list <user>*```','```Listar | Check```','Staff')
        else:
            msg=''
            dados = await Dados(ctx.guild.id)
            try:
                for i in dados['users'][str(user.id)]['ficha']:
                    msg = msg + '\n' + str(dados['users'][str(user.id)]['ficha'][str(i)]['ID']) + ' - ' + dados['users'][str(user.id)]['ficha'][i]['Motivo'] + ' - ' + dados['users'][str(user.id)]['ficha'][i]['Staff']
                embed = discord.Embed(title=f'Ficha de {user.name}',description='```INDEX|MOTIVO|STAFF\n'+msg+'\n```')
                await ctx.send(embed=embed)
            except KeyError:
                await ctx.send(":x: | **Esse usuario nunca teve um aviso**")
    @cmdwarn.command(name='edit',aliases=['editar'])
    @commands.has_permissions(kick_members=True)
    @commands.cooldown(1,5,commands.BucketType.member)
    async def edit(self,ctx,user: discord.Member=None,index=None,novomotivo='Não especificado'):
        if user == None:
            await padrao(ctx,'Moderação','edit','Serve para editar um determinado warn','```warn edit <user>* <index>* <novo_motivo>*```','```edit | editar```','Staff')
        else:
            dados = await Dados(ctx.guild.id)
            try:
                if index == None or index not in dados['ficha']:
                    await ctx.send(":x: | **Index inválida, para saber as index válidas use o `warn list <member>`**")
                else:
                    dados['ficha'][index]['Motivo'] = novomotivo
                    await salvarS(dados,ctx.guild.id)
                    await ctx.send(":question: | **Warn editado com sucesso**")
            except KeyError:
                await ctx.send(":x: | **Esse usuario nunca teve um aviso**")
    @cmdwarn.command(name='all')
    @commands.has_permissions(kick_members=True)
    @commands.cooldown(1,5,commands.BucketType.member)
    async def all(self,ctx):
        dados = await Dados(ctx.guild.id)
        us = dados['users']
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
    @commands.command(name='unwarn',aliases=['desavisar'])
    @commands.has_permissions(kick_members=True)
    @commands.before_invoke(usou)
    @commands.cooldown(1,5,commands.BucketType.member)
    async def unwarn(self,ctx,user:discord.Member=None,index: int=None,*,motivo='Não especificado'):
        if await bl(ctx.author.id) == True:
            return
        if user == None:
            await padrao(ctx,'Moderação','unwarn','Serve para remover o warn de um membro','`unwarn <user> <index> <motivo>','```unwarn | desavisar ```','Staff')
        elif user.id == ctx.author.id:
                await ctx.send(":x: | **Você não pode tirar o seu próprio aviso**")
                return
        elif user.top_role >= ctx.author.top_role:
            await ctx.send(":x: | **Seu cargo está abaixo do usuario**")
            return
        else:
            try:
                dados = await Dados(ctx.guild.id)
                if dados['warns'] == 0:
                    await ctx.send(":x: | **O Usuario não tem avisos**")
                    return
                else:
                    dados['warns'] -= 1
                    if index == None:
                        index = dados['warns']
                    del dados['ficha'][str(index)]
                    await salvarS(dados,ctx.guild.id)
                    await ctx.send(f":question: | **O Aviso do usuario {user.name} foi removido!**")
                    if dados['config']['dmpu'] == 1:
                        await user.send(":warning: | **Seu aviso foi removido**")  
                    global log
                    log = log + '\n' + f'{user.name} warn retirado no servidor {ctx.guild.name}'
            except KeyError:
                await ctx.send(':x: | **Esse usuario não tem avisos**')             
    @commands.command(name='kick',aliases=['expulsar'])
    @commands.has_permissions(kick_members=True)
    @commands.before_invoke(usou)
    @commands.cooldown(1,5,commands.BucketType.member)
    async def kick(self,ctx,member : discord.Member=None,motivo = "Não especificado"):
        if await bl(ctx.author.id) == True:
            return
        if member == None:
            await padrao(ctx,'Moderação','kick','Expulsa um membro','`.kick <user>* motivo`','```kick | expulsar```','Staff')
        else:
            await member.kick()
            dados = await Dados(ctx.guild.id)
            if dados['config']['dmpu'] != 0:
                await member.send(f":x: | **Você foi expulso do servidor {ctx.guild.name}, motivo: {motivo}**")                
            await ctx.guild.ban(member,reason=motivo)      
            await ctx.send(f":question: | **O Usuario {member.name} foi expulso do servidor**")
    @commands.group(name='mute',aliases=['mutar','silenciar','tempmute'], invoke_without_command=True)
    @commands.has_permissions(kick_members=True)
    @commands.before_invoke(usou)
    @commands.cooldown(1,5,commands.BucketType.member)
    async def cmdmute(self,ctx,user: discord.Member=None,tempoMute=None,*,motivo='Não especificado'):
        if await bl(ctx.author.id) == True:
            return
        if user == None:
            await padrao(ctx,'Moderação','mute','Serve para mutar um usuario por um determinado tempo, caso não coloque nenhum tempo o tempo vai ser automaticamente inderteminado ou permanente','`mute <user>* <tempo> <motivo>` -> Silencia um membro\n`list <user>*`','```mute | silenciar | mutar```','Staff')
            return
        elif user.top_role >= ctx.author.top_role:
            await ctx.send(":x: | **Seu cargo está abaixo do usuario**")
            return
        dados = await Dados(ctx.guild.id)
        time=1
        role=None
        ant = tempoMute
        if dados['config']['role_mute'] == 0:
            await ctx.send(":x: | **Você não configurou o cargo de mute! Configure usando o comando** `config mute-role <cargo>`")
            return
        else:
            role = ctx.guild.get_role(dados['config']['role_mute'])
        if tempoMute == None:
            pass
        else:
            try:
                tim = int(re.search("^([0-9]+[1-6]*)([smhd])$",tempoMute).group(1))
                d = re.search("^([0-9]+[1-6]*)([smhd])$",tempoMute).group(2)
                ti = {"s":1,"m":60,"h":60*60,"d":60*60*60}
                try:
                    time = tim * ti[d]
                except KeyError:
                    await ctx.send(":x: | **Formato invalido... Formatos corrretos: [ s | m | d | h ] / 10d -> 10 Dias**")
            except AttributeError:
                motivo = tempoMute + ' ' + motivo
                tempoMute = None
        if tempoMute == None:
            await user.add_roles(role)
            await ctx.send(f":question: | **O Usuario: {user.name} foi mutado por um tempo inderterminado, motivo: {motivo}**")
            if dados['config']['dmpu'] == 1:
                try:await user.send(f"Você está **Mutado** por tempo inderteminado, motivo: {motivo}")                        
                except:await ctx.send(":x: | Erro ao mandar mensagem na DM: **DM Bloqueada**")           
        else:
            await user.add_roles(role)
            cont=0 
            await ctx.send(f":question: | **O Usuario: {user.name} foi mutado por {ant}, motivo: {motivo}**")
            print(time)
            if dados['config']['dmpu'] == 1:
                    try:await user.send(f"Você está **Mutado** por {ant}, motivo: {motivo}")
                    except:await ctx.send(":x: | Erro ao mandar mensagem na DM: **DM Bloqueada**")
        if user.id not in dados['users']:
            dados['users'][str(user.id)] = {'warns':0,'ficha':{},'fichamute':{},'contmute':0,'mute':{}}
        dados['users'][str(user.id)]['contmute'] += 1
        cont = dados['users'][str(user.id)]['contmute']
        dados['users'][str(user.id)]['fichamute'][str(cont)] = {
                "Motivo":motivo,
                "tempo":ant,
                "ID":cont,
                "Staff":ctx.author.name
            }
        global log
        log = log + '\n' + f'{user.name} levou mute no servidor {ctx.guild.name} por o tempo {ant}, motivo: {motivo}'
        if tempoMute==None:
            await salvarS(dados,ctx.guild.id)
            return
        if time >= 60:
            dados['users'][str(user.id)]['mute'] = {
                'temp':datetime.datetime.now(),
                'time':time,
                'id':user.id
            }
            await salvarS(dados,ctx.guild.id)
        else:
            await asyncio.sleep(time)        
            await user.remove_roles(role)
    @cmdmute.command(name='check',aliases=['list'])
    @commands.has_permissions(kick_members=True)
    @commands.cooldown(1,5,commands.BucketType.member)
    async def check(self,ctx,user: discord.Member=None):
        if user == None:
            await padrao(ctx,'Moderação','mute check','Serve para listar todos os mutes do membro mostrando o motivo, o tempo do mute, e quem mutou!','`mute check <user>*` -> lista todos os mutes do membro','```check | list```','Staff')
        else:
            msg=''
            dados = await Dados(ctx.guild.id)
            for i in dados['fichamute']:
                msg = msg + '\n' + str(dados['users'][str(user.id)]['fichamute'][i]['ID']) + ' - ' + dados['users'][str(user.id)]['fichamute'][i]['Motivo'] + ' - ' +dados['users'][str(user.id)]['fichamute'][i]['tempo']+'  -  '+ dados['fichamute'][i]['Staff']
            embed = discord.Embed(title=f'Ficha de {user.name}',description='```INDEX|MOTIVO|TEMPO|STAFF\n'+msg+'\n```')
            await ctx.send(embed=embed)           
    @cmdmute.command(name='edit',aliases=['editar'])
    @commands.has_permissions(kick_members=True)
    @commands.cooldown(1,5,commands.BucketType.member)
    async def edit(self,ctx,user: discord.Member=None,index=None,novomotivo='Não especificado'):
        if user == None:
            await padrao(ctx,'Moderação','edit','Serve para editar um determinado mute','```mute edit <user>* <index>* <novo_motivo>*```','```edit | editar```','Staff')
        else:
            dados = await Dados(ctx.guild.id)
            if index == None or index not in dados['fichamute']:
                await ctx.send(":x: | **Index inválida, para saber as index válidas use o `mute list <member>`**")
            else:
                dados['fichamute'][index]['Motivo'] = novomotivo
                await salvarS(dados,ctx.guild.id)
                await ctx.send(":question: | **Mute editado com sucesso**")
    @commands.command(name='unmute',aliases=['desmutar'])
    @commands.has_permissions(kick_members=True)
    @commands.before_invoke(usou)
    @commands.cooldown(1,5,commands.BucketType.member)
    async def unmute(self,ctx,user: discord.Member=None):
        if await bl(ctx.author.id) == True:
            return
        if user == None:
            await padrao(ctx,'Moderação','unmute','Serve para desmutar membros que já estão mutados','`unmute <user>*` -> desmuta o usuario`','```unmute | desmute```','Staff')
        else:
            dados = await Dados(ctx.guild.id)
            role = ctx.guild.get_role(dados['config']['role_mute'])
            if role not in user.roles:
                await ctx.send(f":x: | **{user.name} não está mutado**")
                return
            else:
                await user.remove_roles(role)
                await ctx.send(f":question: | **{user.name} foi desmutado**")
    @commands.command(name='ban',aliases=['banir'])
    @commands.has_permissions(ban_members=True)
    @commands.before_invoke(usou)
    @commands.cooldown(1,5,commands.BucketType.member)
    async def ban(self,ctx,user:discord.User=None,*,motivo='Não especificado'):
        if await bl(ctx.author.id) == True:
            return
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
            print("a")
        dados = await Dados(ctx.guild.id)
        if dados['config']['dmpu'] != 0:
            try:await user.send(f":x: | **Você foi banido do servidor {ctx.guild.name}, motivo: {motivo}**")                
            except:await ctx.send(":x: | Erro ao mandar mensagem na DM: **DM Bloqueada**")
        await ctx.guild.ban(user,reason=motivo) 
        await ctx.send(f":question: | **O Usuario {user.name} foi banido do servidor**")
    @commands.command(name='unban',aliases=['desbanir'])
    @commands.has_permissions(ban_members=True)
    @commands.before_invoke(usou)
    @commands.cooldown(1,5,commands.BucketType.member)  
    async def unban(self,ctx,user: discord.User=None):
        if await bl(ctx.author.id) == True:
            return
        if user == None:
            await padrao(ctx,'Moderação','unban','Serve para desbanir um usuario!','`unban <user>*` -> Desban em um usuario','```unban | desbanir```','Staff')
        else:
            await ctx.guild.unban(user)
            await ctx.send(f":question: | **O Usuario {user.name} foi desbanido**")
    @commands.command(name='serverinfo',aliases=['guildinfo'])
    @commands.before_invoke(usou)
    @commands.cooldown(1,5,commands.BucketType.member)
    async def serverinfo(self,ctx, guild: int=None):
        if await bl(ctx.author.id) == True:
            return
        rol=[]
        fi=""
        if guild != None:
            guild = bot.get_guild(guild)
            if guild == None:
                await ctx.send(":x: | **Servidor não encontrado... Talvez eu não esteja dentro do servidor :thinking: **")
                return
            rol = guild.roles
            for i in rol:
                if len(fi) > 1900:break
                fi = fi + " @" + i.name
        else:
            guild = ctx.guild
            rol = guild.roles
            for i in rol:
                if len(fi) > 1900:break
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
                try:await m.delete()
                except:pass
                await msgA.delete()    
                return
            if msg.content.lower() == "1":
                await msgA.delete()
                try:await msg.delete()
                except:pass
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
                        try:await msg.delete()
                        except:pass
                        em = ''
                        for i in guild.emojis:
                            if len(em) > 1900:break
                            em = em + ' ' + str(i)
                        embed = discord.Embed(title=f'Informações do servidor {guild.name} | Pagina 3',description=f'Emojis: \n{em}')
                        embed.set_footer(text='Digite "voltar" para voltar ou digite "3" para avançar')
                        mi = await ctx.send(embed=embed)
                        try:
                            msg = await bot.wait_for('message', check=check(ctx.author,["voltar","3"]), timeout=10)
                            if msg.content.lower() == 'voltar':
                                try:await msg.delete()
                                except:pass
                                await mi.delete()
                                pass
                            elif msg.content.lower() == '3':
                                try:await msg.delete()
                                except:pass
                                await mi.delete()
                                embed = discord.Embed(title=f'Informações do servidor {guild.name} | Pagina 4',description=f'Cargos: \n{fi}')
                                embed.set_footer(text='Digite "voltar" para voltar')
                                mo = await ctx.send(embed=embed)
                                try:
                                    msg = await bot.wait_for('message', check=check(ctx.author,["voltar"]), timeout=10)
                                    if msg.content.lower() == 'voltar':
                                        try:await msg.delete()
                                        except:pass
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
    @commands.command(name='userinfo',aliases=['memberinfo'])
    @commands.before_invoke(usou)
    @commands.cooldown(1,5,commands.BucketType.member)
    async def userinfo(self,ctx,user: discord.User=None):
        if await bl(ctx.author.id) == True:
            return
        user = user or ctx.author
        try:
            member = ctx.guild.get_member(user.id)
            embed = discord.Embed(title=f'Informações do usuario **{str(user)}**', description=f'\nConta criada em: **{user.created_at.date()}** | Entrou no servidor em: **{member.joined_at.date()}** | Booster desde: **{"Nunca" if member.premium_since == None else member.premium_since.date()}**\nID Do usuario `{user.id}` | Tag: **{user.discriminator}** | Apelido: **{member.display_name}**\n')  
        except MemberNotFound:                
            embed = discord.Embed(title=f'Informações do usuario {str(user)}', description=f'\nConta criada em: {user.created_at.date()}\n ID: `{user.id}`\n')  
        embed.set_thumbnail(url=user.avatar_url)  
        await ctx.send(embed=embed)  
    class ticket(commands.Cog):
        @commands.command(name='ticket',aliases=['tick'])
        @commands.has_permissions(manage_channels=True)
        @commands.before_invoke(usou)
        @commands.cooldown(1,5,commands.BucketType.member)
        async def ticket(self,ctx,canal: discord.TextChannel=None,idmensagem: int=None):
            if await bl(ctx.author.id) == True:
                return
            if canal == None or idmensagem == None:
                await ctx.send(":x: | **Para criar um sistema de tickets informe o canal de texto onde tem a mensagem e o id da mensagem para eu reagir e assim ativando o sistema de tickets**")
            else:
                msg = await canal.fetch_message(idmensagem)
                await msg.add_reaction('📤')
                dados = await Dados(ctx.guild.id)
                dados["tick"][idmensagem] = True
                await salvarS(dados,ctx.guild.id)
        @commands.Cog.listener()
        async def on_raw_reaction_add(self, payload):
            channel = await bot.fetch_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            user = await message.guild.fetch_member(payload.user_id)
            if user.bot == True:return
            emojiA = payload.emoji
            dados = await Dados(message.guild.id)
            if str(message.id) in dados['tick']:
                if dados['tick'][str(message.id)]:
                    overwrites = {
                        message.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                        user: discord.PermissionOverwrite(read_messages=True)
                    }
                    ch = await message.guild.create_text_channel("tick-"+str(user),overwrites=overwrites)
                    await ch.send(f":white_check_mark: | **{user.mention}, você abriu um ticket espere uma pessoa responder ao seu pedido!**")
        @commands.command(name='close',aliases=['fechar','close_request'])
        @commands.has_permissions(kick_members=True)
        @commands.cooldown(1,5,commands.BucketType.member)
        async def close_request(self,ctx,user: discord.Member=None):
            if user == None:
                await ctx.send(":x: | **Informe o membro do ticket para fechar**")
            else:
                print(f'tick-{str(user).replace("#","").lower()}')
                ch = discord.utils.get(ctx.guild.channels, name='tick-'+str(user).replace('#','').lower())
                if ch == None:
                    await ctx.send(":x: | **Algo deu errado... Verifique se você usou o comando corretamente**")
                await ch.delete()
                await ctx.send(':white_check_mark: | **Pronto!**')
    @commands.command(name='botinfo')
    @commands.before_invoke(usou)
    @commands.cooldown(1,5,commands.BucketType.member)
    async def botinfo(self,ctx):
        if await bl(ctx.author.id) == True:
            return
        embed = discord.Embed(title=f'Olá {ctx.author.name}! Bem vindo as minhas informações.',description=f'\n\n**Estou ligado desde:** {time.localtime(ti).tm_mday}/{time.localtime(ti).tm_mon} as {time.localtime(ti).tm_hour}:{time.localtime(ti).tm_min}\nVocê sabia que eu sou **OpenSource?** -> [GitHub](https://github/Liveira/SphyxBot.py)\n\nDono do Bot: NightterX/Nightter/Liveira\nData de criação... {bot.user.created_at.date()}\nSite oficial do bot: [SphyX](https://tinyurl.com/y7dgym54) | [FAQ](https://tinyurl.com/yamfp9qp)\nServer de suporte: [SphyX Community](https://discord.gg/CG7spnTsKa)\nTotal de membros: {len(bot.users)}\nTotal de servidores: {len(bot.guilds)}\nTotal de emojis: {len(bot.emojis)}\nTotal de comandos: {len(bot.commands)}\n\n\n**Informações técnicas**\n\nLinguagem: [Python](https://python.org)\nBlibioteca: [Discord.py](https://discordpy.readthedocs.io/en/latest/api.html)\nHost: Discloud ( Plano platina )\nBot feito apartir do **ZERO**\n\n**Como surgiu o SphyX?** : No começo de tudo, eu ( Nightter ) estava criando um bot de discord para um servidor de terraria e o bot estava indo muito bem, deu um pouco de trabalho mas consegui terminar, e depois disso um amigo meu falou que seria legal criar um bot global e aqui estamos, no começo era para o bot se chamar Nez, mas decidimos que ia ser SphyX...')
        await ctx.send(embed=embed)
    @commands.command(name='nuke')
    @commands.before_invoke(usou)
    @commands.cooldown(1,5,commands.BucketType.member)
    async def nuke(self,ctx,ch: discord.TextChannel=None):
        if await bl(ctx.author.id) == True:
            return
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
    @commands.command()
    @commands.before_invoke(usou)
    @commands.cooldown(1,5,commands.BucketType.member)
    async def emoji(self, ctx, emoji: discord.PartialEmoji=None):
        if await bl(ctx.author.id) == True:
            return
        await ctx.send(embed = discord.Embed(title=f"Informações do emoji {emoji.name}", description=f"\nAnimado: {'Sim' if emoji.animated else 'Não'}\nData de criação: {emoji.created_at.date()}\nID: `{emoji.id}`\nURL: `{emoji.url}`").set_thumbnail(url=emoji.url))
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    @commands.before_invoke(usou)
    @commands.cooldown(1,5,commands.BucketType.member)
    async def lock(self, ctx, channel: discord.TextChannel=None):
        if await bl(ctx.author.id) == True:
            return
        channel = channel or ctx.channel
        kek = channel.overwrites
        if not kek[ctx.guild.default_role].send_messages:
            await ctx.send(':x: | **O canal escolhido já não tem permissão de enviar mensagens**')
            return
        await channel.edit(overwrites={
            ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False),
        })
        await ctx.send(f":question: | **Canal bloqueado | {channel.mention}!**")
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    @commands.before_invoke(usou)
    @commands.cooldown(1,5,commands.BucketType.member)
    async def unlock(self, ctx, channel: discord.TextChannel=None):
        if await bl(ctx.author.id) == True:
            return
        channel = channel or ctx.channel
        kek = channel.overwrites
        if kek[ctx.guild.default_role].send_messages:
            await ctx.send(':x: | **O canal escolhido já tem permissão de enviar mensagens**')
            return
        await channel.edit(overwrites={
            ctx.guild.default_role: discord.PermissionOverwrite(send_messages=True),
        })
        await ctx.send(f":question: | **Canal desbloqueado | {channel.mention}!**")
    @commands.command()
    @commands.has_permissions(manage_emojis=True)
    @commands.before_invoke(usou)
    @commands.cooldown(1,5,commands.BucketType.member)
    async def addemoji(self,ctx: commands.Context,nm=None,emoji: commands.Greedy[discord.Emoji]=None,link=None):
        if await bl(ctx.author.id) == True:
            return
        a = ''
        nam = ''
        if link == None and emoji == None:
            await ctx.send(":x: | **Você esqueceu de colocar o link ou emoji para adicionar**")
        if nm == None:
            await ctx.send(":x: | **Formato errado! Aqui está um formato certo `.addemoji <nome> <emoji ou link>`")
        if nm != None and link != None:
            nam = nm
            a = requests.get(link).content
        if nm != None and emoji != None:
            nam = nm
            emoji = bot.get_emoji(emoji[0].id)
            a = requests.get(emoji.url).content
        a=await ctx.guild.create_custom_emoji(name=nam.lower().replace("?",""),image=a)
        await ctx.send(f":question: | **Emoji adicionado!** {str(a)}")
    '''class clean(commands.Cog):
    @commands.group(name='clean')
    async def clean(self, ctx):
        await padrao(ctx,'Moderação','clean','OBS: **Essa função é extremamente perigosa! Use com cuidado** | Essa função limpa algo que você especificou por exemplo, `.clean channels remove` <- Nesse caso ele vai remover todos os canais e isso funciona com todas as funções como emojis, canais e cargos facilitando a vida!')'''
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    @commands.before_invoke(usou)
    @commands.cooldown(1,5,commands.BucketType.member)
    @blacklists()
    async def clear(self,ctx,num:int=None):
        if num == None:
            await ctx.send(":x: | **Você esqueceu de colocar a quantidade de mensagens**")
        else:
            d = await ctx.channel.purge(limit=num)
            await ctx.send(f":question: | **{len(d)} menssagens foram apagadas**")
    @commands.group(name='tag',aliases=['tags'],invoke_without_command=True)
    @commands.before_invoke(usou)
    @commands.cooldown(1,5,commands.BucketType.member)
    @blacklists()
    async def tag(self,ctx,tagName=None):
        if tagName == None:
            msg = ""
            dados = await Dados(ctx.guild.id)
            try:
                for i in dados['tag']:
                    msg += f"{', ' if msg != '' else ''}{dados['tag'][i]['nome']}"
                await ctx.send('```\n'+msg+'\n```')
            except Exception as ex:
                print(ex.args)
                await ctx.send(":x: | **Esse servidor não possui a função de TAGS...** Peça para um administrador usar o comando `.tags add`!")
        else:
            dados = await Dados(ctx.guild.id)
            try:
                rol = discord.utils.get(ctx.guild.roles,name=tagName)
                if rol in ctx.author.roles:
                    await ctx.author.remove_roles(rol)
                    await ctx.send(":question: | **Tag removida**")
                    return
                elif dados['tag'][tagName]['req'] == 0:
                    rol = discord.utils.get(ctx.guild.roles,name=tagName)
                    await ctx.author.add_roles(rol)
                    await ctx.send(":question: | **Tag adicionada**")
                else:      
                    role = ctx.guild.get_role(dados['tag'][tagName]['req'])
                    if role in ctx.author.roles:
                        rol = discord.utils.get(ctx.guild.roles,name=tagName)
                        await ctx.author.add_roles(rol)
                        await ctx.send(":question: | **Tag adicionada**")
                    else:
                        await ctx.send(f":x: | **Você não cumpre os requisitos! Você precisa ter o cargo `{role.name}`**")
            except Exception as ex:
                await ctx.send(f":x: | **Tag invalida** : {ex.args}")
    @tag.command(name='add',aliases=['adicionar'])
    @commands.before_invoke(usou)
    @commands.cooldown(1,5,commands.BucketType.member)
    @commands.has_permissions(manage_roles=True)
    @blacklists()
    async def add(self,ctx,nomeTag,requisitos: discord.Role=None):
        if ctx.guild.me.guild_permissions.manage_roles == False:
            await ctx.send(":x: | **Não posso ativar essa opção por falta de permissões, preciso de pemissão de gerenciar cargos para ativar essa opção**")
            return
        dados = await Dados(ctx.guild.id)
        try:
            if nomeTag in dados['tag']:
                await ctx.send(":x: | **Tag já existente**")
                return
            dados['tag'][nomeTag] = {
                'nome':nomeTag,
                'req':requisitos.id if requisitos != None else 0 
            }
        except KeyError:
            dados['tag'] = {}
            dados['tag'][nomeTag] = {
                'nome':nomeTag,
                'req':requisitos.id if requisitos != None else 0
            }
        await ctx.guild.create_role(name=nomeTag)
        await ctx.send(f":question: | **Tag adicionada!**\nNome: **{nomeTag}**\nRequisitos: **{'Nenhum' if requisitos == None else requisitos.name}**")
        await salvarS(dados,ctx.guild.id)
    @tag.command(name='remove',aliases=['remover'])
    @commands.before_invoke(usou)
    @commands.cooldown(1,5,commands.BucketType.member)
    @commands.has_permissions(manage_roles=True)
    @blacklists()
    async def remove(self,ctx,nomeTag):
        d = await Dados(ctx.guild.id)
        try:
            try:
                del d['tag'][nomeTag]
                await salvarS(d,ctx.guild.id)
                await ctx.send(":question: | **Tag removida**")
            except KeyError:await ctx.send(":x: | **Essa tag não existe**")
        except KeyError: await ctx.send(":x: | **O servidor ainda não ativou as Tags!**")
    @commands.command(name='antialt')
    @commands.before_invoke(usou)
    @commands.cooldown(1,5,commands.BucketType.member)
    @commands.has_permissions(manage_roles=True)
    @blacklists()
    async def antialt(self,ctx,dias_de_conta=10):
        dados = await Dados(ctx.guild.id)
        try:
            if dados['antialt'] != {}:
                dados['antialt'] = {}
                await salvarS(dados,ctx.guild.id)  
                await ctx.send(":question: | **O antialt foi desligado**")
            else:
                if ctx.guild.me.guild_permissions.ban_members == False:
                    await ctx.send(":x: | **Não posso ativar essa opção por falta de permissões, preciso de pemissão de banir membros para ativar essa opção**")
                    return
                dados['antialt'] = {
                "day":dias_de_conta
                }
                await salvarS(dados,ctx.guild.id)
                await ctx.send(f":question: | **Todas as contas com menos de {dias_de_conta} dias de criação serão banidos!**")
        except:
            if ctx.guild.me.guild_permissions.ban_members == False:
                await ctx.send(":x: | **Não posso ativar essa opção por falta de permissões, preciso de pemissão de banir membros para ativar essa opção**")
                return
            dados['antialt'] = {
                "day":dias_de_conta
            }
            await salvarS(dados,ctx.guild.id)
            await ctx.send(f":question: | **Todas as contas com menos de {dias_de_conta} dias de criação serão banidos!**")
def setup(self):
    bot.add_cog(mod(bot))