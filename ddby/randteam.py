import random
from types import SimpleNamespace
from discord.ext import commands


sessions = {}


def get_session(server_id):

    global sessions

    if server_id in sessions:
        session = sessions[server_id]
    else:
        session = SimpleNamespace()
        session.maxsize = 4
        session.members = []
        sessions[server_id] = session

    return session


def show_members(session):
    nmembers = len(session.members)

    if nmembers == 0:
        result = '현재 리스트에 아무도 없습니다.\n'
    else:
        result = f'현재 {nmembers}명의 멤버가 리스트에 있습니다.\n'
        for i, name in enumerate(session.members):
            result += f'- 멤버 {i+1:d}: {name}\n'

    result += '\n'
    result += f'팀 당 최대 인원수: {session.maxsize}명'

    return result


def escape_markdown(string_in):
    table = {'*': '\*', '_': '\_'}
    string_out = ''.join(tuple(table.get(c, c) for c in string_in))
    return string_out


def get_string_members(team):
    dpnames = []
    for name in team.members:
        dpname = escape_markdown(name)
        is_leader = (name == team.leader)
        if is_leader:
            dpname = '__**' + dpname + '**__'
        dpnames.append(dpname)

    out = f'{team.name} ({team.size}명): '
    out += ', '.join(dpnames)

    return out


@commands.command(pass_context=True)
async def add(ctx, *names: str):
    """리스트에 멤버를 추가합니다."""

    server = ctx.message.server
    session = get_session(server.id)

    nmembers_old = len(session.members)

    for name in names:
        if name in session.members: continue
        session.members.append(name)

    nmembers_new = len(session.members)
    nmembers_add = nmembers_new - nmembers_old

    result = '뗀뗀보야가 {}명의 멤버를 리스트에 추가했습니다.\n\n'.format(nmembers_add)
    result += show_members(session)

    await ctx.bot.say(result)


@commands.command(name='del', pass_context=True)
async def _del(ctx, *names: str):
    """리스트로부터 멤버를 삭제합니다."""

    server = ctx.message.server
    session = get_session(server.id)

    nmembers_old = len(session.members)

    if nmembers_old == 0:
        result = '현재 리스트에 아무도 없어서 지울 수 있는 멤버가 없네요.'

    else:

        members_new = [name for name in session.members if name not in names]
        session.members = members_new
        nmembers_new = len(session.members)
        num_deleted = nmembers_old - nmembers_new

        if num_deleted == 0:
            result = '리스트에 변함이 없습니다.\n\n'
        else:
            result = f'뗀뗀보야가 {num_deleted}명의 멤버를 리스트에서 제외했습니다.\n\n'

        result += show_members(session)

    await ctx.bot.say(result)


@commands.command(pass_context=True)
async def show(ctx):
    """현재 리스트를 보여줍니다."""

    server = ctx.message.server
    session = get_session(server.id)

    result = show_members(session)
    await ctx.bot.say(result)


@commands.command(pass_context=True)
async def clear(ctx):
    """리스트를 깨끗이 지웁니다."""

    server = ctx.message.server
    session = get_session(server.id)

    session.members = []
    result = '뗀뗀보야가 멤버 리스트를 초기화 하였습니다.'

    await ctx.bot.say(result)


# p_num = re.compile('^[0-9]+$')
@commands.command(pass_context=True)
async def size(ctx, maxsize: int):
    """팀 당 멤버수를 조정합니다."""

    server = ctx.message.server
    session = get_session(server.id)

    if maxsize == 0:
        result = '이게 말이냐 방구냐! 팀을 없애버리려 하다니...'

    elif session.maxsize == maxsize:
        result = ':angry: 아니, 바꾸기 전에 확인부터 하라뗀!\n'
        result += '팀 최대 인원수는 원래 {}명 이었다뗀!'.format(session.maxsize)

    else:
        maxsize_old = session.maxsize
        session.maxsize = maxsize
        maxsize_new = session.maxsize
        result = '팀 최대 인원수가 {}명에서 {}명으로 변경되었습니다.'.format(maxsize_old, maxsize_new)

    await ctx.bot.say(result)


@commands.command(pass_context=True)
async def ddby(ctx):
    """뗀뗀보야를 외치며 랜덤 매칭을 합니다."""

    server = ctx.message.server
    session = get_session(server.id)

    if len(session.members) <= 1:
        result = '이런, 리스트에 친구들이 없어요.\n'
        result += '먼저 리스트에 친구들 이름을 넣어주세요.'

    else:
        members = session.members[:]
        random.shuffle(members)

        result = ':raised_hand: 뗀:arrow_right:뗀:arrow_right:보:arrow_lower_right::arrow_upper_right:야! :raised_hand:\n'
        result += '\n'

        i = 0
        while True:

            s = (i + 0) * session.maxsize
            e = (i + 1) * session.maxsize
            _members = members[s:e]
            if len(_members) == 0:
                break

            team = SimpleNamespace()
            team.name = f'Team {i+1}'
            team.leader = _members[0]
            team.members = _members
            team.size = len(team.members)
            result += get_string_members(team) + '\n'
            i += 1

    await ctx.bot.say(result)
