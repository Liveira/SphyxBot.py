import sys

from discord.ext.commands.core import Group
sys.path.append('..')
from main import *
class Social(commands.Cog):
        @commands.command(name='profile',aliases=['perfil'])
        @commands.before_invoke(usou)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def profile(self,ctx,user: discord.User=None):
            if await bl(ctx.author.id) == True:
                return
            user = user or ctx.author
            async with ctx.channel.typing():
                temp = img.new('RGBA',(1400,1000))
                avt = user.avatar_url
                dad = await UDados(user.id)
                rp=()
                if dad['mar'] == 0:
                    rp = (318,124)
                    imga = img.open('pf.png')
                else:
                    imga = img.open('tempMa.png')
                    rp = (313,197)
                avt = requests.get(url=avt)
                foto = img.open(BytesIO(avt.content)).resize((302,302)).convert('RGBA')
                re = requests.get(url=dad['profile']['back-pf']['url'])
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
                desc = textwrap.fill(dad['desc'],60,break_long_words=True)
                fonte = imgfont.truetype('ARIALBD.TTF', 34)
                draw.text((27,800),desc,font=fonte,fill=(255,255,255))
                fonte = imgfont.truetype('ARIALBD.TTF', 43)
                draw.text(rp,str(dad['rep']) + ' Reps',font=fonte,fill=(255,255,255))
                if dad['mar'] != 0:
                    fonte = imgfont.truetype('ARIALBD.TTF', 38)
                    us = bot.get_user(dad['mar'])
                    draw.text((317,130),f'Casado com: {us.name}',font=fonte,fill=(255,255,255))
                temp.save('pfout.png',otimize=True,quality=100)
                arq = discord.File(open('pfout.png','rb'))#218 294
                #261 112
            msg = await ctx.send(file=arq)
            arq.close()

        @commands.command(name='desc',aliases=['sobre-mim','sobre'])
        @commands.before_invoke(usou)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def desc(self,ctx,*,nova_desc=None):
            if await bl(ctx.author.id) == True:
                return
            if nova_desc == None:
                await ctx.send(':x: | **Você esqueceu de colocar a descrição**')
            else:
                var=''
                dados = await UDados(ctx.author.id)
                if len(nova_desc) > 150: 
                    var = nova_desc[:150]
                    var = var  + '...'
                else:
                    var = nova_desc
                dados['desc'] = var
                await salvar(dados,ctx.author.id)

                await ctx.send(f":question: | **Pronto, descrição alterado para** ```{var}```")

        @commands.command(name='help',aliases=['ajuda'])
        @commands.before_invoke(usou)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def help(self,ctx):
            if await bl(ctx.author.id) == True:
                return
            embed = discord.Embed(title=f'Olá {str(ctx.author)}!',description='**Parece que você precisa de ajuda...\n**\n**Quer ver meus comandos?**\n\a [Comandos](https://sphyx-6ffe7.web.app/pages/comandos.html)\n\a [TopGG](https://top.gg/bot/782737686238461952)\n\n**Está com alguma dúvida?**\n\a [FAQ](https://sphyx-6ffe7.web.app/pages/FAQ.html)\n\a [Server do discord](https://discord.gg/CG7spnTsKa)')
            embed.set_footer(text=f'{ctx.author.name} usou as {str(time.strftime("%H:%M", time.localtime()))}',icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        @commands.command(name='helpclassic',aliases=['ajudaclassico'])
        @commands.before_invoke(usou)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def helpclassic(self,ctx, name=None):    
            if name != None:
                command: commands.Command() = bot.get_command(name)
                if command == None:
                    pass
                else:
                    await ctx.send(embed=discord.Embed(title=f'Comando {command.name}').add_field(name='Outros nomes',value='-> ' + str(command.aliases).replace('['," ").replace(']'," ").replace("'",' ')).add_field(name='Como usar',value=command.brief))
                    return
            s = ""
            inc = 0
            acr = 20
            emb = discord.Embed(title='Ajuda clássico...')
            for i in bot.cogs:
                if i == "events":continue
                c = bot.get_cog(i)
                for cmd in c.get_commands():
                    inc += 1
                    s += f'{inc} - {cmd.name}\n'
                emb.add_field(name=c.qualified_name,value=s)
                s=""
            await ctx.send(embed=emb)

        @commands.command(name='rep',aliases=['reputação'])
        @commands.cooldown(1,48000,BucketType.user)
        @commands.before_invoke(usou)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def rep(self,ctx,user: discord.User=None):
            if await bl(ctx.author.id) == True:
                return
            if user == None:
                await ctx.send(':x: | **Você não informou um membro**')
                a = bot.get_command('rep')
                a.reset_cooldown(ctx)
            else:
                if user.id == ctx.author.id:
                    await ctx.send(":x: | **Você não pode dar reputação para você mesmo**")
                    a = bot.get_command('rep')
                    a.reset_cooldown(ctx)
                    return
                dados = await UDados(user.id)
                dados['rep'] += 1
                await salvar(dados,user.id)
                await ctx.send(f":question: | **Você deu um ponto de reputação para {user.mention}**")

        @commands.command(name='addBack')
        @commands.before_invoke(usou)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def addBack(self,ctx):
            if await bl(ctx.author.id) == True:
                return
            if ctx.author.id in devs:
                msg = await ctx.send(":white_check_mark: | **Informe o nome do background**")
                def checkMS(author):
                        def inner_check(message):
                            if message.author == author and ctx.guild == message.guild:
                                return True  
                            else: return False
                        return inner_check
                ms = await bot.wait_for(event='message',check=checkMS(ctx.author),timeout=60)
                shop=''
                with open('shop.json','r',encoding='utf-8') as f:
                    shop = dict(json.load(f))
                cont = shop['cont'] + 1
                shop['cont'] += 1
                shop[cont] = {}
                shop[cont]['name'] = ms.content
                await ms.delete()
                await msg.edit(content=':white_check_mark: | **Informe a descrição do background**')
                ms = await bot.wait_for(event='message',check=checkMS(ctx.author),timeout=60)
                shop[cont]['desc'] = ms.content
                await ms.delete()
                await msg.edit(content=":white_check_mark: | **Informe o preço do background**")
                ms = await bot.wait_for(event='message',check=checkMS(ctx.author),timeout=60)
                shop[cont]['preco'] = int(ms.content)
                await ms.delete()
                await msg.edit(content=":white_check_mark: | **Informe o LINK do background**")
                ms = await bot.wait_for(event='message',check=checkMS(ctx.author),timeout=60)
                shop[cont]['preview'] = ms.content
                await ms.delete()
                await msg.edit(content=":white_check_mark: | **Informe o author do background [Caso não tenha digite 'null']**")
                ms = await bot.wait_for(event='message',check=checkMS(ctx.author),timeout=60)
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

        @commands.command(name='marry',aliases=['casar'])
        @commands.before_invoke(usou)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def marry(self,ctx,user:discord.Member=None):
            if await bl(ctx.author.id) == True:
                return
            if user == None:
                await ctx.send(":x: | **Você não informou o membro**")
                return
            dados = await UDados(ctx.author.id)
            outro = await UDados(user.id)
            if dados['mar'] != 0 or outro['mar'] != 0:
                await ctx.send(":x: | **Você ou ele(a) já está casado, para divorciar use `.divorcio`**")
                return
            msg = await ctx.send(f":question: | **Você quer mesmo se casar com {user.name}, vocês dois precisam pagar 4500 para se casar, {user.mention} se quiser se casar com {ctx.author.mention} reaja no anel!**")
            await msg.add_reaction('💍')
            def checkr(reaction,useraa):
                    return useraa == user and reaction.emoji in ["💍"]
            try:
                reac,user = await bot.wait_for('reaction_add',check=checkr,timeout=60)
                dado = await UDados(ctx.author.id)
                outro = await UDados(user.id)
                if dado['money'] < 4500 or outro['money'] < 4500:
                    await ctx.send(":x: | **Você não tem dinheiro para fazer o casamento!**")
                    return
                await ctx.send(f":heart: | **Parece que aconteceu um casamento :flushed:, {ctx.author.name} se casou com {user.name}**")
                outro['mar'] = ctx.author.id
                dado['mar'] = user.id
                dado['money'] -= 4500
                outro['money'] -= 4500
                await salvar(dado,ctx.author.id)
                await salvar(outro,user.id)
            except asyncio.TimeoutError:
                await ctx.send(":sob: | **Parece que o casamento não deu certo**")

        @commands.command(name='divorcio')
        @commands.before_invoke(usou)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def divorcio(self,ctx):
            if await bl(ctx.author.id) == True:
                return
            dados = await UDados(ctx.author.id)
            if dados['mar'] == 0:
                await ctx.send(':x: | **Você não pode se divorciar com ninguem :thonk:**')
            else:
                msg = await ctx.send("Você tem certeza?")
                await msg.add_reaction('✅')
                def checkr(reaction,useraa):
                    return useraa == ctx.author and reaction.emoji in ["✅"]
                try:
                    reac,user = await bot.wait_for('reaction_add',check=checkr,timeout=60)
                    id = dados['mar']
                    dados['mar'] = 0
                    us = bot.get_user(id)
                    o = await UDados(us.id)
                    o['mar'] = 0
                    await us.send(f':sob: | **{ctx.author.name} se divorciou de você..., você pode ter feito algo que ele(a) não gostou...**')
                    await ctx.send(f":sob: | **Você se divorciou de {us.name}**")
                    await salvar(dados,ctx.author.id)
                    await salvar(o,us.id)
                except asyncio.TimeoutError:
                    await ctx.send(':smiley: | **Parece que o casamento ainda não acabou**')
def setup(self):
    bot.add_cog(Social(bot))