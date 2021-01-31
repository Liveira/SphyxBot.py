import sys
sys.path.append('..')
from main import *
class Div(commands.Cog):
        @commands.command(name='gato',aliases=['cat','gatos','gatoaleatorio','randomcat'])
        @commands.before_invoke(usou)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def cat(self,ctx):
            if await bl(ctx.author.id) == True:
                return
            url = requests.get(url='https://aws.random.cat/meow')
            js = url.json()
            embed = discord.Embed(title='Gato Aleatorio')
            embed.set_image(url=js['file'])
            await ctx.send(embed=embed)
        @commands.command(name='cachorro',aliases=['dog','cachorros','cachorroaleatorio','randomdog'])
        @commands.before_invoke(usou)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def dog(self,ctx):
            if await bl(ctx.author.id) == True:
                return
            url = requests.get(url='https://dog.ceo/api/breeds/image/random')
            js = url.json()
            embed = discord.Embed(title='Cachorro Aleatorio')
            embed.set_image(url=js['message'])
            await ctx.send(embed=embed)
        @commands.command(name='ciencia',aliases=['acienciafoilongedemais','simounao'])
        @commands.before_invoke(usou)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def ciencia(self,ctx,user: discord.User=None):
            if await bl(ctx.author.id) == True:
                return
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
        @commands.command(name='art',aliases=['arte'])
        @commands.before_invoke(usou)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def art(self,ctx,user: discord.User=None):
            if await bl(ctx.author.id) == True:
                return
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
        @commands.command(name='fogo',aliases=['fire'])
        @commands.before_invoke(usou)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def fogo(self,ctx,user: discord.User=None):
            if await bl(ctx.author.id) == True:
                return
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
        @commands.command(name='triste',aliases=['sad'])
        @commands.before_invoke(usou)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def triste(self,ctx,user: discord.User=None):
            if await bl(ctx.author.id) == True:
                return
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
        @commands.command(name='news',aliases=['noticia','noticias'])
        @commands.before_invoke(usou)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def news(self,ctx,user: commands.Greedy[discord.Member]=None,*,message=f'Noticias CHOCANTES! O Servidor morreu por falta de membros'):
            if await bl(ctx.author.id) == True:
                return
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
                fonte = imgfont.truetype('ARIALBD.TTF', 30)
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
        @commands.command(name='anime')
        @commands.before_invoke(usou)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def anime(self,ctx,*,nome: str=None):
            if await bl(ctx.author.id) == True:
                return
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
        @commands.command(name='osu',invoke_without_command=True)
        @commands.before_invoke(usou)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def osu(self,ctx,*,user: str=None):
            if await bl(ctx.author.id) == True:
                return
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
        @commands.command(name='osubeatmap')
        @commands.before_invoke(usou)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def beatmap(self,ctx,beatmap=None):
            if await bl(ctx.author.id) == True:
                return
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
        @commands.command(name='run')
        @commands.before_invoke(usou)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def run(self,ctx,*,code=None):
            if await bl(ctx.author.id) == True:
                return
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
        @commands.command(name='avatar')
        @commands.before_invoke(usou)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def avatar(self,ctx,user: discord.User=None):
            if await bl(ctx.author.id) == True:
                return
            user = user or ctx.author
            await ctx.send(embed=discord.Embed(title=f'Avatar de {user.name}').set_image(url=user.avatar_url))
        @commands.command(name='servericon')
        @commands.before_invoke(usou)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def servericon(self,ctx,guild: int=None):
            if await bl(ctx.author.id) == True:
                return
            if guild!=None:
                guild = bot.get_guild(guild)
                if guild == None:
                    await ctx.send(":x: | **Não achei nenhum servidor...**")
                    return
            else:
                guild = ctx.guild
            await ctx.send(embed=discord.Embed(title=f'Icone do servidor {guild.name}').set_image(url=guild.icon_url))
        @commands.command()
        @commands.before_invoke(usou)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def calendario(self, ctx,ano:int,mes:int):
            if await bl(ctx.author.id) == True:
                return
            await ctx.send(f"```python\n{calendar.month(ano,mes)}\n```")
        @commands.command(aliases=['dado','dados'])
        @commands.before_invoke(usou)
        @commands.cooldown(1,5,commands.BucketType.member)
        @blacklists()
        async def dice(self, ctx, dice):
            if await bl(ctx.author.id) == True:
                return
            match = re.search("^(0*[1-9][0-9]*)d(0*[1-9][0-9]*)(?:\+*([0-9]+))??$",dice)
            if match == None:
                await ctx.send(":x: | **Formato inválido...** | Exemplos: `.dice 10d20` ou `.dice 10d20+6`\n**10** <- Quantidade de dados | d |**20** <- Quantidade de lados | + ( Opcional ) **6** <- Acréscimo bruto |")
                return
            qntdad = int(match.group(1))
            qntlad = int(match.group(2))
            result = 0
            lis = []
            for i in range(1,qntdad):
                l = random.randrange(0,qntlad)
                result += l
                lis.append(l)
            if match.group(3) != None:
                result += int(match.group(3))
                lis.append(f'+ {match.group(3)}')
            await ctx.send(f":question: | **Aqui o resultado {result}** | {lis}")
        '''class lol(commands.Cog):
            @commands.command()
            @commands.before_invoke(usou)
            @commands.cooldown(1,120,commands.BucketType.guild)
            @blacklists()
            async def lol(self, ctx, user: discord.User=None):
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
                    sb = StickBug(img.open(BytesIO(requests.get(foto).content)))
                    sb.video_resolution = (1280, 720)
                    sb.lsd_scale = 0.5
                    sb.save_video('lol.mp4')
                    arq = discord.File(open('lol.mp4','rb'))
                await ctx.send(file=arq)
                discord.utils.get('poetico', bot.emojis)'''
def setup(self):
    bot.add_cog(Div(bot))