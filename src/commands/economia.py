import sys
sys.path.append('..')
from main import *
class Economia(commands.Cog):
        @commands.command(name='atm',aliases=['money','coin','coins','dinheiro','meudinheiro','mymoney'])
        @commands.before_invoke(usou)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def atm(self,ctx,user: discord.Member=None):
            if await bl(ctx.author.id) == True:
                return
            user = user or ctx.author
            dados = await UDados(user.id)
            embed = discord.Embed(title=f'Conta bancaria de {user.name}',description=f'A Conta bancaria é o lugar onde tem informações de economia do usuario\n\nSeu dinheiro: **{dados["money"]}**\nSeus Gold Coins: **{dados["gold"]}**')
            await ctx.send(embed=embed)
        @commands.command(name='daily',aliases=['diaria','day'])
        @commands.cooldown(1,24000,commands.BucketType.member)
        @commands.before_invoke(usou)
        async def daily(self,ctx):
            if await bl(ctx.author.id) == True:
                return
            dados = await UDados(ctx.author.id)
            rand = randrange(400,800)
            dados['money'] += rand
            await salvar(dados,ctx.author.id)
            embed = discord.Embed(title=f'Recompensa diaria de {ctx.author.name}',description=f'Você pegou sua recompensa diaria de hoje, para pegar a proxima pegue no proxima dia\n\nVocê ganhou {rand} moedas!')
            embed.set_thumbnail(url='https://media.discordapp.net/attachments/765971397524062220/788833032382840882/gift.png')
            await ctx.send(embed=embed)
        @daily.error
        async def err(self,ctx,error):
            if isinstance(error, CommandOnCooldown):
                await ctx.send(":x: | **Você já resgatou sua recompensa diaria**")
        @commands.command(name='topmoney',aliases=['rankdinheiro','rankcoin'])
        @commands.before_invoke(usou)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def topmoney(self,ctx,index:int=1):
            if await bl(ctx.author.id) == True:
                return
            msg=""
            nm=index*10-10
            isa=0
            get = users.find({}).sort('money', pymongo.DESCENDING).skip(index*10-10).limit(10)
            for i in get:

                a=bot.get_user(int(i['_id']))
                if a==None:
                    isa = i['nome']
                else:
                    isa = a.name
                nm+=1
                msg = msg +f'\n#{nm} | **{isa}** - {i["money"]}'
            try:await ctx.send(msg)
            except:await ctx.send(':x: | **Não achei nenhum resultado...**')
        @commands.command(name='pay',aliases=['pagar'])
        @commands.before_invoke(usou)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def pay(self,ctx,user:discord.Member=None,dinheiro:int=1):
            if await bl(ctx.author.id) == True:
                return
            if user == None:
                await ctx.send(":x: | **Você precisa informar um membro**")
            elif user.id == ctx.author.id:
                await ctx.send(":x: | **Você não pode se pagar**")
            elif dinheiro <= 0:
                await ctx.send(":x: | **Você precisa dar um numero maior que 0**")
            else:
                dados = await UDados(ctx.author.id)
                outro = await UDados(user.id)
                if dinheiro > dados['money']:
                    await ctx.send(":x: | **Você não pode pagar essa quantidade**")
                else:
                    dados['money'] -= dinheiro
                    outro['money'] += dinheiro
                    await salvar(dados,ctx.author.id)
                    await salvar(outro,user.id)
                    await ctx.send(f":question: | **Você deu {dinheiro}cs para {user.name}**")
        @commands.command(name='giveway',aliases=['sorteio','sortear'])
        @commands.before_invoke(usou)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def giveway(self,ctx,horario=None,num: int=1,*,message:str='Sorteio'):
            if await bl(ctx.author.id) == True:
                return
            if horario == None:
                await ctx.send(":x: | **Informe o tempo do sorteio e a mensagem**")
            else:
                
                horario = horario.lower()
                
                global vargv
                dados = await Dados(ctx.guild.id)
                try:
                    tim = int(re.search("^([0-9]+[1-6]*)([smhd])$",horario).group(1))
                    d = re.search("^([0-6]+)([smhd])$",horario).group(2)
                    ti = {"s":1,"m":60,"h":60*60,"d":60*60*60}
                    time = tim * ti[d]
                    
                except:
                    await ctx.send("Formatos de horarios disponiveis [s/m/h/d]")
                    return
                embed = discord.Embed(title='SphyX Giveway',description=f'\n🎉 | **{message}**\n🏆 | **Ganhadores**: {num}\n⏰ | **Pendente**').set_footer(text=f'Acaba em ->  ')
                embed.timestamp = datetime.datetime.now() + delt(time)
                msg = await ctx.send(embed=embed)
                await msg.add_reaction('🎉')
                if not 'GV' in dados:
                    dados['GV'] = {}
                dados['GV'][str(msg.id)] = {
                    "gar":[],
                    "premio":message,
                    "chan":ctx.channel.id
                }
                
                if time < 61:
                    await asyncio.sleep(time)
                    msgA=''
                    lk=[]
                    krek=[]
                    for i in range(num):
                        if dados['GV'][str(msg.id)]['gar'] == []:
                            await msg.edit(embed= discord.Embed(title='SphyX Giveway',description=f'\n🎉 | **{message}**\n🏆 | **Ganhadores**: Ninguém... \n⏰ | **Concluida**').set_footer(text=f'Acabou ás ->  '))
                            await ctx.send("👀 | **Ninguém participou do sorteio**")
                            del dados['GV'][str(msg.id)]
                            return
                        lk.append(random.choice(dados['GV'][str(msg.id)]['gar']))
                        user = ctx.guild.get_member(lk[i])
                        while user in krek:
                            lk.append(random.choice(dados['GV'][str(msg.id)]['gar']))
                            user = ctx.guild.get_member(lk[i])
                        msgA = msgA + user.mention + ','
                        krek.append(user)
                    await ctx.send(f" 🎉 {msgA} Ganhou | **{dados['GV'][str(msg.id)]['premio']}") 
                    del dados['GV'][str(msg.id)]               
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
        @commands.command(name='shop',aliases=['store','loja'])
        @commands.before_invoke(usou)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def shop(self,ctx, index: int=1):
            if await bl(ctx.author.id) == True:
                return
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
        @commands.command(name='inventory',aliases=['inventario','inv'])
        @commands.before_invoke(usou)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def inventory(self,ctx,index: int=1):
            if await bl(ctx.author.id) == True:
                return
            user = ctx.author
            shop=''
            with open('shop.json','r',encoding='utf-8') as f:
                shop = dict(json.load(f))
            ix = 0
            msg = ""
            dados = await UDados(ctx.author.id)
            inv = dict(dados['inventory'])
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
                        print(val)
                        var = inv[val]
                    except KeyError:
                        try: 
                            try: 
                                var = inv[li[1] + ' ' + li[2]]
                                try: 
                                    var = inv[li[1] + ' ' + li[2] + ' ' + li[3]]
                                except IndexError:
                                    return
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
                        dados['profile'][var['tipte']]['url'] = var['preview']
                        dados['profile'][var['tipte']]['name'] = var['name']
                        await ctx.send(f":question: | **Você usou o item {var['name']}**")
                        await salvar(dados,ctx.author.id)
                    else:
                        await ms.delete()
                        await m.delete()
                        await Economia.Inventory.inventory(self,ctx,index)
                except ValueError: await ctx.send(":x: | **Você usou a forma errada... aqui está o jeito certo `item <nome>`**")                
        @commands.command(name='comprar',aliases=['buy'])
        @commands.before_invoke(usou)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def comprar(self,ctx,index=None):
            if await bl(ctx.author.id) == True:
                return
            shop=''
            with open('shop.json','r',encoding='utf-8') as f:
                shop = dict(json.load(f))
            if index == None:
                await ctx.send(":x: | ** Index invalida, para ver index válidas use o .shop **")
            else:
                d = await UDados(ctx.author.id)
                embed = discord.Embed(title=shop[index]['name'], description=f'\n\n`{shop[index]["desc"]}`\n\nPreco: {shop[index]["preco"]} | Você tem {d["money"]} | {":white_check_mark:" if d["money"] >= shop[index]["preco"] else ":x:"}\n\n{"Esse item é consumivel" if shop[index]["usa"] else "Esse item não é consumivel"} | Tipo do item: {shop[index]["categoria"]} | Autor: {shop[index]["author"] if shop[index]["author"] != None else "Nenhum / Indefinido"}')
                embed.set_footer(text='Reaja ✅ Para confirmar a compra ou ♻️ para comprar e usar',icon_url=ctx.author.avatar_url)
                embed.set_thumbnail(url=shop[index]["preview"])
                msg = await ctx.send(embed=embed)                
                await msg.add_reaction('✅')
                await msg.add_reaction('♻️')
                def checkr(reaction,user):
                    return user == ctx.message.author and reaction.emoji in ["✅","♻️"]
                try:
                    reac,user = await bot.wait_for('reaction_add',check=checkr,timeout=60)
                    if shop[index]["preco"] > d['money']:
                        await ctx.send(':x: | **Você não tem dinheiro suficiente para fazer essa compra**')
                    else:
                        if shop[index]['name'] not in d['inventory']:                        
                            d['inventory'][shop[index]['name']] = {
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
                            d['money'] -= shop[index]["preco"]
                        else:
                            if shop[index]['onetime']:
                                await ctx.send(":x: | **Você só pode comprar isso 1 vez**")
                                return    
                            d['inventory'][shop[index]['name']]["cont"] += 1
                        if reac.emoji == '♻️':
                            d['profile'][shop[index]['ti']] = {'url':shop[index]['preview'],'name':shop[index]['name']}
                    await salvar(d,ctx.author.id)
                except asyncio.TimeoutError:
                    ms = await ctx.send(":x: | **Tempo excedido**")
                    await asyncio.sleep(3)
                    await ms.delete()
def setup(self):
    bot.add_cog(Economia(bot))