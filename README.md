# SphyxBot.py
Um bot de discord brasileiro feito totalmente em Python feito por mim

# Posso copiar e colar?
Sim, o bot é Open Source mas ainda sim você precisar dar os creditos

# O que tem no bot?

- Comandos de moderação
- Comandos de diversão
- Comandos de economia 
-------------------------
        Funções
- Autorole (Multiplo)
- Sistema de entrada e saida com mensagens totalmente personalizado
- Sistema de XP TOTALMENTE personalizado
- Sistema de mudar prefixo do bot
- E Bot totalmente configuravel


[![Discord Bots](https://top.gg/api/widget/782737686238461952.svg)](https://top.gg/bot/782737686238461952)

# SphyX Bot
Atualmente o SphyX conta com mais de 8 funções e 50 comandos ( Contando com SUB Comandos )



O Bot é [Open Source]('https://github.com/Liveira/SphyXbot.py')!

# Comandos

| Guia     | Descrição |Exemplos             |
|:--------:|:-----------:|:------------:
| *        | Obrigatorio| `<user>*`
| º        | Podem ser usados variveis| `<message>º`
| =        | Valores já pré-definidos | `<motivo = 'Não especificado'>`     
 
| Moderação                                     |
|:---------------------------------------------:|

| Nome          | Desc          | Como usar      |
| ------------- |:------------- | :----- |
| ban           | Bane um usuário | `.ban <user>* <motivo = 'Não especificado'>`|
| unban           | Retira um banimento de usuário | `.unban <user>* <motivo = 'Não especificado'>`|
| mute           | Silencia um usuário | `.mute <user>* <motivo = 'Não especificado'>`|
| mute list           |Lista todos os mutes de um usuário | `.mute list <user>*`|
| mute edit          | Edita um mute de um usuário | `.mute edit <user>* <index = ultimo mute>`|
| warn          | Avisa um usuário | `.warn <user>* <motivo  = 'Não especificado'>`|
| warn list          | Lista todos os warns de um usuário | `.warn <user>*`|
| warn edit           | Edita um warn de um usuário | `.ban <user>* <index = ultimo warn>`|
| warn all           | Lista todos os warns por ranking | `.warn all`|
| kick | Expulsa um usuário | `.kick <user>* <motivo = 'Não especificado'>`

| Configuração                                  |
|:---------------------------------------------:|

| Nome          | Desc          | Como usar      |
| ------------- |:------------- | :----- |
|config| Manda todos os comandos de configuração | `.config`
|config xp-time| Muda o tempo de cooldown para ganhar o XP|`.config xp-time <novo tempo>*`
|config media-xp| Muda a media de XP que o membro ganha|`.config media-xp <Nova media>*`
|config mute-role| Muda o cargo de mute do servidor|`.config mute-role <cargo>*`
|config welcome-msg| Muda a mensagem de boas vindas| `.config welcome-msg <mensagem>*º`
|config leave-msg| Muda a mensagem de saida|`.config leave-msg <mensagem>*º`
|config welcome-channel| Muda o chat de mandar as mensagens de boas vindas e saida | `.config welcome-channel <canal>*`
|config slowmode | Muda o SlowMode de um chat sem limites | `.config slowmode <canal>*`
|config prefix | Muda o prefixo do bot | `.config prefix <novo prefixo>*`
| config autorole | Função de cargo automatico quando um membro entra | `.config autorole`
| config autorole add | Adiciona um cargo automatico para o autorole | `.config autorole add <cargo>*`
| config autorole list | Lista todos os cargos do autorole | `.config autorole list`
| config autorole remove | Remove um cargo do autorole  |`.config autorole remove <index>*`
| config des | Desativa uma função  < welcome-channel / media-xp > | `.config des <função>*`
| config dmpu | Ativa ou desativa a mensagem de punição no DM| `.config dmpu <ativar ou desativar>`
| config atmessage | Muda a mensagem de boas vindas na DM do membro|`.config atmessage <messagem>*º`

| Funções extras                                  |
|:---------------------------------------------:|

| Nome          | Desc          | Como usar      |
| ------------- |:------------- | :----- |
|rr        |Coloca ReactionRole em uma mensagem| `.rr <canal onde está a  mensagem>* <id da mensagem>* <emoji>* <cargo>*`
|ticket    | Coloca a função de tickets em uma mensagem|`.ticket <canal onde esta a mensagem>* <id da mensagem>*`
|close    | Fecha um ticket de um membro|`.close <membro>`
| giveway | Crie um sorteio para seus membros! | `.giveway <tempo do sorteio>* <numero de ganhadores>* <mensagem>*`

| Diversão                                  |
|:---------------------------------------------:|

| Nome          | Desc          | Como usar      |
| ------------- |:------------- | :----- |
| cat | Manda uma mensagem aleatoria de um gato | `.cat`
| dog | Manda uma mensagem aleatoria de um cachorro | `.dog`
| ciencia | Será que a ciência foi longe demais? | `.ciencia <membro> ou <foto> ou <ultima foto>`
| art | Isso... Isso é lindo | `.art <membro> ou <foto> ou <ultima foto>`
| fogo | Queimar coisas dentro da água não faz muito sentido | `.fogo <membro> ou <foto> ou <ultima foto>`
|triste | Realmente triste... | `.triste <membro> ou <foto> ou <ultima foto>`
|news | Nas noticias de hoje o... | `.news [<membro> ou <foto> ou <ultima foto> ou <mensagem>] <mensagem>`
|osu | Mostre o seu perfil do Osu! para seus amigos | `.osu <nome da conta>`
|osubeatmap | Mostre um beatmap legal! | `.osubeatmap <id do beatmap>`

| Economia                                  |
|:---------------------------------------------:|

| Nome          | Desc          | Como usar      |
| ------------- |:------------- | :----- |
| atm | Mostra sua carteira | `.atm <membro>`
| daily | Pegue a sua recompensa diaria | `.daily`
| topmoney | Veja o top global de dinheiro|`.topmoney`
| pay | Pague para alguem | `.pay <membro>*`
| shop | Veja a loja de itens do SphyX | `.shop <pagina=1>`
|inventory| Veja o seu inventario de itens ou usar um item| `.inventory`
|comprar| Caso você já saiba o ID do item para comprar, compre direto! | `.comprar <id>`

| Dev                                  |
|:---------------------------------------------:|

Aviso rapido, esta categoria é feita exclusivamente para desenvolvedores, seja WEB, GAME ou até mesmo bot dev

| Nome          | Desc          | Como usar      |
| ------------- |:------------- | :----- |
| repo | Procure um repositorio do github| `.repo <nome do criador do repositorio>* <nome do repositorio>*`
|traduzir| Traduza uma mensagem | `.traduzir <EnUs ou PtBr>* <EnUs ou PtBr>* <mensagem>* `
| short | encurta um link | `.short <link>*`
| qr | Manda um código QR com o link | `.qt <link>*`
| hastebin | Mande o código diretamente para o hastebin | `.hastebin < extensão do arquivo > <código ou arquivo do código>*`

| Social                                  |
|:---------------------------------------------:|


| Nome          | Desc          | Como usar      |
| ------------- |:------------- | :----- |
| perfil | Manda o perfil| `.perfil <membro>`
| desc | Muda a dewscrição do seu perfil | `.desc <nova desc>* não pode ser maior que 100 caracteres`
| help | Quer ajuda? Use esse comando | `.help`

| Variaveis                                 |
|:---------------------------------------------:|

| Nome       | Descrição | Exemplo|
|:----------:|:-------------|:--------------------|
| `[user]`   | Manda o nome do membro sem marcar | Nightter |
| `[usertag]`   | Manda o nome do membro com tag sem marcar | Nightter#4540 |
| `[mention]`   | Menciona o membro | @Nightter#4540 |
| `[guildname]`   | Manda o nome do servidor | Servidor dos amigos |
