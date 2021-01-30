import sys
sys.path.append('..')
from main import *
from lxml import html
from _requests import *
tree = reqSTRING('https://pypi.org/simple/')
package_list = [package for package in tree.xpath('//a/text()')]
class Dev(commands.Cog):
        @commands.command(name='repo', aliases=['repositorio'])
        @commands.before_invoke(usou)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def repo(self,ctx,author=None,nmrepo=None):
            if await bl(ctx.author.id) == True:
                return
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
        ''' Traduzir(commands.Cog):
            @commands.command(name='traduzir',aliases=['translate'])
            @commands.before_invoke(usou)
            @commands.cooldown(1,5,commands.BucketType.member)
            @blacklists()
            async def traduzir(self,ctx,de=None,para=None,*,mensagem=None):
                if await bl(ctx.author.id) == True:
                    print("ALO")
                    return
                if de != None:
                    try:
                        print("ALO")
                        RE = Translator(from_lang=de,to_lang=para)
                    except:
                        await ctx.send(":x: | **Me desculpe, mas eu não consegui traduzir esse texto**")
                        return
                    await ctx.send(f'Texto traduzido: {RE.translate(mensagem)}') '''
        @commands.command(name='short',aliases=['encurtador','link'])
        @commands.before_invoke(usou)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def short(self,ctx,link=None):
            if await bl(ctx.author.id) == True:
                return
            if link == None: 
                await ctx.send(':x: | **Você esqueceu de colocar o link**')
                return
            s = pyshorteners.Shortener()
            await ctx.send(f':question: | **Aqui está o seu link:** {s.tinyurl.short(link)}')
        @commands.command(name='qr',aliases=['qrcode'])
        @commands.before_invoke(usou)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def qr(self,ctx,link=None):
            if await bl(ctx.author.id) == True:
                return
            if link == None: 
                await ctx.send(':x: | **Você esqueceu de colocar o link**')
                return
            img = qrcode.make(link)
            img.save('nome_do_arquivo.png')
            arq = discord.File(open('nome_do_arquivo.png','rb'))#218 294
            msg = await ctx.send(file=arq)
        @commands.command(name='hastebin')
        @commands.before_invoke(usou)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def hastebin(self,ctx,file='txt',*,code=None):
            if await bl(ctx.author.id) == True:
                return
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
        @commands.command(name='att',hidden=True)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def att(self,ctx):
            if ctx.author.id not in devs:
                return
            a=[]
            for i in bot.users:
                a.append({"_id":i.id,'nome':i.name,'mar':0,'desc':'Eu sou uma pessoa misteriosa, mas eu posso mudar minha descrição usando .desc','rep':0,"xp_time":0,'money':0,'gold':0,'inventory':{"Padrão": {"name": "Padrão","desc": "Background padrão","tip": "BackGround Profile","use": True,"cont": 0,"onetime": True,"preview": "https://media.discordapp.net/attachments/776197504378732555/795800876383338496/default.png?width=642&height=459","tipte": "back-pf","author": "SphyX Team"}},'profile':{'back-pf':{'url':'https://media.discordapp.net/attachments/776197504378732555/795800876383338496/default.png?width=642&height=459','name':"Padrão"}}})
            users.insert_many(a)
            await ctx.send("FASASASASASS")
        @commands.command(name='teste',hidden=True)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def teste(ctx):
            if await bl(ctx.author.id) == True:
                return
            guilds = users.find_one()
            guids = users.find_one()
            for i in bot.users:
                guilds['mar'] = 0
                print(i)
            sets = {"$set":guilds}
            users.update_one(guids,sets)
            await ctx.send("De primeira caralho")
        @commands.group(name='ping',invoke_without_command=True)
        @commands.before_invoke(usou)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def ping(self,ctx):
            if await bl(ctx.author.id) == True:
                return
            await ctx.send(f":question: | **Minha látencia é: {int(bot.latency * 1000)}**")
        @ping.command(name='shard',aliases=['shards'])
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def shard(self,ctx):
            msg = f'[Quantidade total de SHARDS: {bot.shard_count} | ShardID do servidor: {ctx.guild.shard_id}]\n[ID|Ping|Está desligado?]'
            for i in bot.shards:
                s = bot.get_shard(i)
                msg = msg + '\n' + f'{"*"if s.id == ctx.guild.shard_id else ""}[{s.id}\t|{int(s.latency*1000)}\t|{s.is_closed()}\t]'
            
            await ctx.send('```python\n'+msg+'\n```')
        @commands.command(name='xko',hidden=True)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def xko(self,ctx, user: discord.User,qnt):
            if ctx.author.id not in devs:
                return
            d = await UDados(user.id)
            d['money'] += int(qnt)
            await ctx.send(f"{random.randrange(10,100000)}")
            await salvar(d,user.id)
        @commands.command(hidden=True)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def eval(self,ctx,*,code):
            if ctx.author.id not in devs:
                return

            lv = {
                'discord':discord,
                'ctx':ctx,
                'commands':commands,
                'bot':bot,
                'channel':ctx.channel,
                'author':ctx.author,
                'message':ctx.message,
                'guild':ctx.guild,
            }    
            stdout = StringIO(code)
            try:
                with contextlib.redirect_stdout(stdout):
                    exec(
                        f"async def funcao():\n{textwrap.indent(code,'   ')}",lv
                    )
                    obj = await lv['funcao']()
                    resultado = f"\n{obj}\n"
            except Exception as e:
                resultado = f"ERRO: {e.args}"
            await ctx.send(embed=discord.Embed(title=':inbox_tray: **Entrada**',description=f'```python\n{code}\n```'))   
            await ctx.send(embed=discord.Embed(title=':outbox_tray: **Saida**',description='```python\n'+str(resultado)+'```'))        
        @commands.command(name='html',aliases=['markdowntohtml'])
        @commands.before_invoke(usou)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def html(self,ctx,*,message):
            if await bl(ctx.author.id) == True:
                return
            mark = markdown.Markdown()
            hml = mark.convert(message)
            msg = await ctx.send(":question: | **Reaja :envelope_with_arrow: para receber os últimos 2000 caracteres no seu DM, reaja :computer: para eu mandar o código inteiro ou reaja :printer: para eu mandar um preview**")
            await msg.add_reaction('📩')
            await msg.add_reaction('💻')
            await msg.add_reaction('🖨')
            def checkr(reaction,user):
                return user == ctx.message.author and reaction.emoji in ["📩","💻","🖨"]
            try:
                reac,user = await bot.wait_for('reaction_add',check=checkr,timeout=60)
                if reac.emoji == '💻':
                    req = requests.post('https://hastebin.com/documents',data=hml)
                    key = json.loads(req.content)   
                    await ctx.send(f':question: | **Aqui está o código:** https://hastebin.com/{key["key"]}')
                elif reac.emoji == '📩':
                    await ctx.author.send(f"```html\n{hml[:1980]}...\n```")
                    await ctx.message.add_reaction("📩")
                elif reac.emoji == '🖨':
                    msg = await ctx.send("Aguarde...")
                    mk = str(hml)
                    fi = mk
                    hml = '<!DOCTYPE html>\n<html>\n\t<head>\n\t\t<meta charset="utf-8">\n\t\t<meta name="viewport" content="width=800 height=600">\n\t\t<title>a</title>\n\t\t<style>\n\t\t\tbody{\n\t\t\t\tbackground-color: black;\n\t\t\t}\n\t\t\ttext{\n\t\t\t\tfont-size: 38px;\n\t\t\t\tcolor: white;\n\t\t\t\tfont-family: Arial, Helvetica, sans-serif;\n\t\t\t\ttext-indent: 50px;\n\t\t\t}\n\t\t\t</style>\n\t</head>\n\t<body>\n\t<text>\n'+fi+'\n\t</text>\n\t</body>\n</html>'
                    options = GrabzItImageOptions.GrabzItImageOptions()
                    options.format = "jpg"
                    grabzIt.HTMLToImage(hml, options)
                    grabzIt.SaveTo("result.jpg")
                    f = discord.File('result.jpg')
                    await ctx.send(file=f)
                    await msg.delete()
                    await ctx.author.send(f"Entrada...```html\n{hml}\n```")
            except asyncio.TimeoutError:
                await ctx.send(":x: | **Tempo esgotado...**")
        @commands.command()
        @commands.before_invoke(usou)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def invite(self,ctx):
            if await bl(ctx.author.id) == True:
                return
            emo = bot.get_emoji(798585999692791820)
            await ctx.send(embed=discord.Embed(title='Me adicione!',description=f":flushed: | **Opa, você quer me adicionar no servidor? Se sim, muito obrigado, se você me adicionar vai faltar {100 - 1 - len(bot.guilds) } servidores para eu ganhar verificado!** [Link de convite](https://discord.com/api/oauth2/authorize?client_id=782737686238461952&permissions=8&scope=bot)"))
        @commands.command()
        @commands.before_invoke(usou)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def vote(self, ctx):
            if await bl(ctx.author.id) == True:
                return
            await ctx.send("Vote em mim! https://top.gg/bot/782737686238461952/vote")
        @commands.command(name='ocr',aliases=['digitalizar'],hidden=True)
        async def ocr(self,ctx: commands.Context):
            return
            '''atch: Message = ctx.message
            atch = atch.attachments
            fot=""
            if atch[0] != None:
                if atch[0].size >= 1:
                    if atch[0].width != None: 
                        fot = atch[0].url
            else:
                if ultimafoto[str(ctx.guild.id)] == None:
                    await ctx.send(":x: | **Não encontrei nenhuma foto ou você não informou a foto**")
                    return
                else:
                    fot = ultimafoto[str(ctx.guild.id)]
            a = pytesseract.image_to_string(img.open(BytesIO(requests.get(fot).content)),lang='ptbr')
            await ctx.send(f'```\n{a}\n```')'''
        @commands.command(name='regex',aliases=['re'])
        @commands.before_invoke(usou)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def regex(self,ctx,regex,*,string):
            if await bl(ctx.author.id) == True:
                return
            try:
                a = re.search(regex,string)
                if a == None:
                    await ctx.send(":question: | **String não deu match**")
                else:
                    await ctx.send(f":question: | **MATCH: {a.groups()} | {a.string}**")
            except:await ctx.send(":x: | **Formato inválido**")
        @commands.command(name='ram',aliases=['rm'])
        @commands.before_invoke(usou)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def ram(self,ctx):
            if ctx.author.id not in devs: return
            await ctx.send(f"Ram: {discloud.ram()}")
        @commands.command()
        @commands.before_invoke(usou)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def pypi(self, ctx,repo:str):       
            if repo in package_list:
                j = reqJSON(f'https://pypi.org/pypi/{repo}/json')['info']
                await ctx.send(embed = discord.Embed(title=f'Blibioteca: {j["name"]} | v{j["version"]}',description=f"{j['summary']}\n\n**Versão do python: **{j['requires_python']}\n**Página inicial: ** {j['home_page']}\n**Link para o PyPi: **{j['package_url']}\n**Licença: **{j['license']}\n**Criador: ** {j['author']}"))
def setup(self):
    bot.add_cog(Dev(bot))