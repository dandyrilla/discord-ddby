import random
import discord
from discord.ext import commands


@commands.command(pass_context=True)
async def hello(ctx):
    """인사를 합니다."""

    greetings = [
        '안녕하세요. 오늘 식사는 든든히 하셨나요?',
        '오늘 날씨는 어때요? 저는 아직 밖에 나가보질 못해서요.',
        '심심하신가요? 뗀뗀보야가 같이 놀아드릴게요.',
        '이번 라운드 보급상자는 당신에게 떨어질 거예요.',
        '뗀뗀보야의 원어민 발음이 궁금한가요? 그 분께 여쭤보세요.',
        '어서오세요! 오늘 야식으로 :poultry_leg:을 먹어봐요!',
        '요즘 무슨 영화가 재미있어요? 제게 추천 좀 해주세요.',
        '배그가 안될때는 가끔 오버워치로 기분전환을 해봐요.',
        '오늘의 할일은 내일로, 내일의 아침은 오늘의 야식으로.',
        '누가 저를 여기로 보냈는지 모르겠지만, 열심히 해볼게요!',
        '제 이름이요? 아마도 GISA 라는 분이 지어주셨다던데...',
        '혹시 통영이란 곳을 아시나요? 제가 태어난 곳이예요.',
    ]

    content = random.choice(greetings) + '\n'
    await ctx.bot.say(content)


@commands.command(pass_context=True)
async def echo(ctx, *args):
    """
    앵무새처럼 말한 내용을 따라합니다.

    d:echo 내 말 따라하지마.
    내 말 따라하지마.
    """
    text = ' '.join(args)
    await ctx.bot.say(text)


@commands.command(pass_context=True)
async def choose(ctx, *choices):
    """
    여러 선택지 중에 하나를 임의로 골라줍니다.

    d:choose 짜장 짬뽕
    짜장
    d:choose 월 화 수 목 금 토 일
    목
    """

    if len(choices) >= 2:
        content = random.choice(choices)
    else:
        content = '2개 이상의 선택지를 입력해주세요.'

    await ctx.bot.say(content)


# @bot.command()
# async def send(channel_id: str, *content: str):
#     """특정 채널로 메시지를 보냅니다."""
#     # 348770419605635094  pubg-general
#     # 418762118138167296  mmm-general
#     channel = discord.utils.get(bot.get_all_channels(), id=channel_id)
#     await bot.send_message(channel, ' '.join(content))


@commands.group(pass_context=True)
async def info(ctx):
    """정보를 보여줍니다."""

    if ctx.invoked_subcommand is None:
        await ctx.bot.say(f"No, '{ctx.subcommand_passed}' is not cool.")


@info.command(name='channel', pass_context=True)
async def info_channel(ctx):

    channel = ctx.message.channel

    embed = discord.Embed(title='CHANNEL INFO')
    embed.description = 'Information for the current channel'
    embed.colour = discord.Colour.light_grey()
    # embed.colour = discord.Colour(0xff0000)

    embed.add_field(name='name', value=channel.name)
    embed.add_field(name='server', value=channel.server)
    embed.add_field(name='id', value=channel.id)
    embed.add_field(name='type', value=channel.type)

    embed.set_footer(text='produced by ddby')

    await ctx.bot.send_message(channel, embed=embed)


@commands.command(pass_context=True)
async def leave(ctx):
    """서버에서 내보냅니다."""
    server = ctx.message.server
    await ctx.bot.leave_server(server)
