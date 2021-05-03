# Requirements
import discord 
from discord.ext import commands, tasks
from datetime import datetime
import random

'''
    TOKEN para verifcar a autenticidade da aplicação
'''
TOKEN = '<insira-o-token-aqui>'

bot = commands.Bot(command_prefix='')

empty_square = '⬛' 
fully_square = '🟩'

number = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', 
          '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
          
empty_progress = empty_square+empty_square+empty_square+empty_square+empty_square+empty_square+empty_square+empty_square+empty_square+empty_square

'''
    Calcular porcentagem
'''
def percent_calc(current, total):
    try:
        percent_actual = int((current * 100) / total)
    except:
        percent_actual = 0

    try:
        number_active_square = (percent_actual - (percent_actual % 10)) / 10
    except:
        number_active_square = 0

    progress = ''

    for i in range(1, 10):
        if i <= number_active_square:
            progress += '🟩'
        else:
            progress += '⬛'

    return (progress, percent_actual)

'''
    Lógica de votação
'''
class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Online')

    '''
        Quando adicionar uma reação faça
    '''
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, data):
        if(data.member != self.bot.user):
            channel = self.bot.get_channel(data.channel_id)
            msg = await channel.fetch_message(data.message_id)
            embed = msg.embeds[0]

            i = 0
            react_count = []
            react_total = 0
            for reaction in msg.reactions:
                react_count.append(reaction.count-1)
                react_total += reaction.count-1
            
            for field in embed.fields:
                progress_bar = percent_calc(react_count[i], react_total)
                embed.set_field_at(index=i, name=f'{field.name}', value=f'{progress_bar[0]} {progress_bar[1]}%', inline=False)
                i += 1

            await msg.edit(embed=embed)

    '''
        Quando remover uma reação faça
    '''
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, data):
        if(data.member != self.bot.user):
            channel = self.bot.get_channel(data.channel_id)
            msg = await channel.fetch_message(data.message_id)
            embed = msg.embeds[0]

            i = 0
            react_count = []
            react_total = 0
            for reaction in msg.reactions:
                react_count.append(reaction.count-1)
                react_total += reaction.count-1
            
            for field in embed.fields:
                progress_bar = percent_calc(react_count[i], react_total)
                embed.set_field_at(index=i, name=f'{field.name}', value=f'{progress_bar[0]}  {progress_bar[1]}%', inline=False)
                i += 1

            await msg.edit(embed=embed)

    '''
        Quando digitarem v + argumentos realize
    '''
    @commands.command(name='v')
    async def create_poll(self, ctx, question, *answers):
        if(len(answers) > 10):
            await ctx.send('A lista deve conter no máximo 10 opções!')
            return

        ''' 
            Criação de Embed
        '''
        embed = discord.Embed(title=f'{ question }',
                              colour=ctx.author.colour,
                              timestamp=datetime.utcnow())

        embed.set_author(name=f'''{str(ctx.message.author).split('#')[0]}''', icon_url=ctx.message.author.avatar_url)

        i = 0
        for answer in answers:
            answer = f'{number[i]}. {answer}'
            embed.add_field(name=answer, value=f'{empty_progress} 0%', inline=False)
            i += 1
 
        embed.set_footer(text='Desenvolvido por Guido. 😎\nPara votar, selecione uma reação abaixo.\n')

        embed_sent = await ctx.send(embed=embed)

        i = 0
        for answer in answers:
            await embed_sent.add_reaction(number[i])
            i += 1

bot.add_cog(Poll(bot))
bot.run(TOKEN)