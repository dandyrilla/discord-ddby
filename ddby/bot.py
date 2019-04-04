import os
import json
import pickle
import logging

import discord
from discord.ext import commands
from .misc import hello, echo, choose, info, leave
from .randteam import add, _del, show, clear, size, ddby


# logger
logging.basicConfig(format='%(asctime)-15s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# bot
bot = commands.Bot(command_prefix='d:', description='dden-dden-bo-ya!')


# region utils

def omd(path):
    os.makedirs(path, exist_ok=True)
    return path


def write(out, out_file_txt):
    """write text into file"""
    with open(out_file_txt, 'w') as out_f:
        out_f.write(out)


def pickle_load(in_file_dat):
    """load pickled object"""
    with open(in_file_dat, 'rb') as in_f:
        obj = pickle.load(in_f)
    return obj


def pickle_dump(obj, out_file_dat):
    """dump pickled object"""
    out_dir = os.path.dirname(out_file_dat)
    if out_dir: omd(out_dir)
    with open(out_file_dat, 'wb') as out_f:
        pickle.dump(obj, out_f)


def json_load(in_file_json):
    with open(in_file_json) as in_f:
        data = json.load(in_f)
    return data


def svg2png(in_file_svg):
    java      = 'C:/PROGRA~1/Java/jre1.8.0_171/bin/java'
    batik_jar = 'D:/pycharm-projects/ddby/bin/batik-1.9/batik-rasterizer-1.9.jar'
    cmdl  = java
    cmdl += ' -Xmx6g'
    cmdl += f' -jar {batik_jar}'
    cmdl += f' {in_file_svg} >nul'
    os.system(cmdl)

# endregion


@bot.event
async def on_ready():

    logger.info('Logged in as: '
                f'user.name={bot.user.name}, '
                f'user.id={bot.user.id}, '
                f'discord.__version__={discord.__version__}')

    bot_nick = '뗀뗀보야'
    for server in bot.servers:
        # print(server.id, server.name, sep='\t')
        # 348770419605635093	PUBG 싸움마당
        # 418760599598792717	테스트를하자
        user = discord.utils.find(lambda m: m.name == 'ddby', server.members)
        if user.nick != bot_nick:
            await bot.change_nickname(user, bot_nick)


# @bot.event
# async def on_voice_state_update(before, after):
#     for channel in before.server.channels:
#         if channel.name == 'general':
#             await bot.send_message(channel, f'on_voice_state_update: {before.voice.voice_channel} -> {after.voice.voice_channel}')


# @bot.event
# async def on_message(message):
#     print(message.author, message.content)
#     await bot.process_commands(message)


cmdlist = [hello, echo, choose, info, leave,
           add, _del, show, clear, size, ddby]
for cmd in cmdlist:
    bot.add_command(cmd)
