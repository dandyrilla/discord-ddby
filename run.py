from ddby.bot import bot

if __name__ == '__main__':
    token = open('token.txt').read()
    bot.run(token)
