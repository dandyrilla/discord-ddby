import uuid
import requests
from os.path import join as opj
from datetime import datetime, timedelta


from discord.ext import commands


city_info = {
    'San Francisco': {'name': '샌프란시스코', 'nation': 'USA',         'utcoffset': -7, 'lat': 37.774929, 'lon': -122.419416},
    'Boston':        {'name': '보스턴',       'nation': 'USA',         'utcoffset': -4, 'lat': 42.360082, 'lon': -71.058880},
    'Reykjavík':     {'name': '레이캬비크',   'nation': 'Iceland',     'utcoffset': 0,  'lat': 64.126521, 'lon': -21.817439},
    'Seoul':         {'name': '서울',         'nation': 'South Korea', 'utcoffset': 9,  'lat': 37.566535, 'lon': 126.977969},
    'Bangkok':       {'name': '방콕',         'nation': 'South Korea', 'utcoffset': 7,  'lat': 13.756331, 'lon': 100.501765},
}


class Worldtime(object):

    def __init__(self, utcoffset, name, lat, lon):

        self.name = name
        self.lat = lat
        self.lon = lon

        self.td = timedelta(hours=utcoffset)
        self.now = datetime.utcnow() + self.td
        self.ymd = self.now.strftime('%Y-%m-%d')
        self.hms = self.now.strftime('%I:%M:%S')

        self.apm = self.now.strftime('%p')
        self.apm_kor = {'AM': '오전', 'PM': '오후'}[self.apm]

        url  = 'https://api.sunrise-sunset.org/json'
        url += '?lat={:.6f}&lng={:.6f}&date=today'.format(self.lat, self.lon)
        res = requests.get(url).json()['results']

        self.sunrise   = datetime.strptime(res['sunrise'], '%I:%M:%S %p') + self.td
        self.sunset    = datetime.strptime(res['sunset'],  '%I:%M:%S %p') + self.td
        self.daylength = tuple(map(int, res['day_length'].split(':')))

        is_daytime = (self.sunrise.time() <= self.now.time() < self.sunset.time())
        self.icon = (':new_moon_with_face:', ':sun_with_face:')[is_daytime]

    def __str__(self):
        col = (self.ymd, self.apm_kor, self.hms, self.icon, self.name)
        return ' '.join(col)


@commands.command(pass_context=True)
async def now(ctx):
    """세계의 관심 도시들의 현재 시각을 나타냅니다."""

    # city_names = ('San Francisco', 'Boston', 'Reykjavík', 'Seoul')
    city_names = ('Boston', 'Reykjavík', 'Seoul', 'Bangkok')

    content = ''

    for city_name in city_names:

        city = city_info[city_name]
        wt = Worldtime(city['utcoffset'], city['name'], city['lat'], city['lon'])
        content += str(wt) + '\n'

        # sunrise = wt.sunrise.time().strftime('%I:%M:%S %p')
        # sunset  = wt.sunset.time().strftime('%I:%M:%S %p')
        # dl = '{}시간 {}분 {}초'.format(*wt.daylength)

    dt_now = datetime.now()
    dt_arr = datetime.strptime('2018-08-13 16:40:00', '%Y-%m-%d %H:%M:%S')
    delta  = dt_arr - dt_now
    days, r = divmod(delta.total_seconds(), 86400)
    hours, r = divmod(r, 3600)
    minutes, r = divmod(r, 60)
    content += '* 학성쓰 도착까지 {:d}일 {:d}시간 {:d}분 남음.'.format(int(days), int(hours), int(minutes)) + '\n'

    await ctx.bot.say(content)


@commands.command(pass_context=True)
async def nowclock(ctx):
    """(In development)"""

    channel = ctx.message.channel

    wt1 = Worldtime(-7, 'San Francisco, USA')
    wt2 = Worldtime(-4, 'Boston, USA')
    wt3 = Worldtime(0, 'Reykjavík, Iceland')
    wt4 = Worldtime(9, 'Seoul, South Korea')
    wts = [wt1, wt2, wt3, wt4]

    uid = str(uuid.uuid4())
    tmp_dir = config['tmp_dir']
    out_file_svg = opj(tmp_dir, uid + '.svg')
    out_file_png = opj(tmp_dir, uid + '.png')

    # write(out, out_file_svg)
    # svg2png(out_file_svg)

    # await bot.send_file(channel, file_png)


@commands.command(pass_context=True)
async def wakeup_haksung(ctx):
    """학성쓰를 깨웁니다."""

    server = ctx.message.server
    # user = server.get_member('337949273230671872')  # 나초
    # user = server.get_member('412570117705039883')  # 후레이크
    user = server.get_member('349139749887279106')  # 학성쓰

    city = city_info['Boston']
    wt = Worldtime(city['utcoffset'], city['name'], city['lat'], city['lon'])
    wt_p = wt.now.strftime('%p')
    wt_h = wt.now.strftime('%I')
    wt_m = wt.now.strftime('%M')

    content = '{}, 그만 자고 일어나요!\n'.format(user.mention)
    content += '지금은 거기 시간으로 {} {}시 {}분 입니뗀!'.format({'AM': '오전', 'PM': '오후'}[wt_p], wt_h, wt_m)

    await ctx.bot.say(content)


@commands.command(pass_context=True)
async def wakeup_flake(ctx):
    """후레이크님을 깨웁니다."""

    server = ctx.message.server
    user = server.get_member('412570117705039883')  # 후레이크

    city = city_info['Bangkok']
    wt = Worldtime(city['utcoffset'], city['name'], city['lat'], city['lon'])
    wt_p = wt.now.strftime('%p')
    wt_h = wt.now.strftime('%I')
    wt_m = wt.now.strftime('%M')

    content = f'{user.mention}, 그만 자고 일어나요!\n'
    content += '지금은 거기 시간으로 {} {}시 {}분 입니뗀!'.format({'AM': '오전', 'PM': '오후'}[wt_p], wt_h, wt_m)

    await ctx.bot.say(content)
