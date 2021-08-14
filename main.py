import asyncio, discord, time, json
import datetime as dt
import openpyxl 
from game import *
from user import *
from discord.ext import commands
import os
import os.path
import openpyxl as oxl
from openpyxl import load_workbook, workbook, worksheet
from bs4 import BeautifulSoup
import bs4
import urllib.parse, urllib.request, urllib.error

game = discord.Game('!도움')
bot = commands.Bot(command_prefix="!", Status = discord.Status.online, activity = game)
token = open(r"C:\Users\user\Desktop\코딩\python project\디코(게임)봇\데이터파일\token.txt", "r").readline()

guilds_dict = {}
guilds_games = {}

@bot.event
async def on_guild_join(guild):
    guilds_dict.update({guild.name : guild.id})
    await None

@bot.event
async def on_guild_remove(guild):
    del guilds_dict[guild.name]
    await None

@bot.event
async def on_ready():
    print("I have logged in as {0.user}\n".format(bot))

@bot.command(aliases = ['안녕'])
async def hello(ctx):
    await ctx.send("안녕")

@bot.command()
async def 도움(ctx):
    embed = discord.Embed(title = "심심이(게임)", description = "게임 봇이 될 예정", color = 0x6E17E3) 
    embed.add_field(name = bot.command_prefix + "도움", value = "도움말을 봅니다", inline = False)
    embed.add_field(name = bot.command_prefix + "주사위", value = "주사위를 굴려 봇과 대결합니다", inline = True)
    embed.add_field(name = bot.command_prefix + "홀짝 [홀/짝] [돈]", value = "홀짝 게임을 합니다", inline = False)
    embed.add_field(name = bot.command_prefix + "회원가입/탈퇴", value = "각종 컨텐츠를 즐기기 위한 회원가입을 합니다/탈퇴", inline = True)
    embed.add_field(name = bot.command_prefix + "내정보", value = "자신의 정보를 확인합니다", inline = False)
    embed.add_field(name = bot.command_prefix + "정보 [대상]", value = "멘션한 [대상]의 정보를 확인합니다", inline = True)
    embed.add_field(name = bot.command_prefix + "송금 [대상] [돈]", value = "멘션한 [대상]에게 [돈]을 보냅니다", inline = False)
    embed.add_field(name = bot.command_prefix + "도박 [돈]", value = "[돈]을 걸어 도박을 합니다. 올인도 가능합니다", inline = True)
    embed.add_field(name = bot.command_prefix + "랭킹", value = "다른 사람과의 랭킹을 비교해보세요", inline = False)   
    embed.set_thumbnail(url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTR4kfoax-IA3rkGbfc2zYyO2HgMKK7nfbcZg&usqp=CAU")
    embed.set_footer(text = "게임용", icon_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTR4kfoax-IA3rkGbfc2zYyO2HgMKK7nfbcZg&usqp=CAU")
    await ctx.send(embed=embed)

@bot.command()
async def 따봉(ctx):
    embed = discord.Embed(title = "따봉", description = "따봉", color = 0x00FFFF)
    embed.set_thumbnail(url = "https://p-ac.namu.la/80/8029d3fd22eefc3ed87538b67ef7f70fa47e089997d9a93e6d69dc348b3326e9.jpg?type=orig")
    embed.set_footer(text = "따봉", icon_url = "https://p-ac.namu.la/80/8029d3fd22eefc3ed87538b67ef7f70fa47e089997d9a93e6d69dc348b3326e9.jpg?type=orig")
    await ctx.send(embed = embed)
    
@bot.command()
async def 주사위(ctx):
    result, _color, bot1, bot2, user1, user2, a, b = dice()

    embed = discord.Embed(title = "주사위 게임 결과", description = None, color = _color)
    embed.add_field(name = "심심이의 숫자 " + bot1 + "+" + bot2, value = ":game_die: " + a, inline = False)
    embed.add_field(name = ctx.author.name+"의 숫자 " + user1 + "+" + user2, value = ":game_die: " + b, inline = False)
    embed.set_footer(text="결과: " + result)
    await ctx.send(embed=embed)

@bot.command()
async def 도박(ctx, money):
    userExistance, userRow = checkUser(ctx.author.name, ctx.author.id)
    win = gamble()
    result = ""
    betting = 0
    _color = 0x000000
    if userExistance:
        print("DB에서 ", ctx.author.name, "을 찾았습니다.")
        cur_money = getMoney(ctx.author.name, userRow)

        if money == "올인":
            betting = cur_money
            if win:
                result = "성공"
                _color = 0x00ff56
                print(result)

                modifyMoney(ctx.author.name, userRow, int(0.5*betting))

            else:
                result = "실패"
                _color = 0xFF0000
                print(result)

                modifyMoney(ctx.author.name, userRow, -int(betting))
                addLoss(ctx.author.name, userRow, int(betting))

            embed = discord.Embed(title = "도박 결과", description = result, color = _color)
            embed.add_field(name = "배팅금액", value = betting, inline = False)
            embed.add_field(name = "현재 자산", value = getMoney(ctx.author.name, userRow), inline = False)

            await ctx.send(embed=embed)
            
        elif int(money) >= 10:
            if cur_money >= int(money):
                betting = int(money)
                print("배팅금액: ", betting)
                print("")

                if win:
                    result = "성공"
                    _color = 0x00ff56
                    print(result)

                    modifyMoney(ctx.author.name, userRow, int(0.5*betting))

                else:
                    result = "실패"
                    _color = 0xFF0000
                    print(result)

                    modifyMoney(ctx.author.name, userRow, -int(betting))
                    addLoss(ctx.author.name, userRow, int(betting))

                embed = discord.Embed(title = "도박 결과", description = result, color = _color)
                embed.add_field(name = "배팅금액", value = betting, inline = False)
                embed.add_field(name = "현재 자산", value = getMoney(ctx.author.name, userRow), inline = False)

                await ctx.send(embed=embed)

            else:
                print("돈이 부족합니다.")
                print("배팅금액: ", money, " | 현재자산: ", cur_money)
                await ctx.send("돈이 부족합니다. 현재자산: " + str(cur_money))
        else:
            print("배팅금액", money, "가 10보다 작습니다.")
            await ctx.send("10원 이상만 배팅 가능합니다.")
    else:
        print("DB에서 ", ctx.author.name, "을 찾을 수 없습니다")
        await ctx.send("도박은 회원가입 후 이용 가능합니다.")

    print("------------------------------\n")

@bot.command()
async def 랭킹(ctx):
    rank = ranking()
    embed = discord.Embed(title = "레벨 랭킹", description = None, color = 0x4A44FF)

    for i in range(0,len(rank)):
        if i%2 == 0:
            name = rank[i]
            lvl = rank[i+1]
            embed.add_field(name = str(int(i/2+1))+"위 "+name, value ="레벨: "+str(lvl), inline=False)

    await ctx.send(embed=embed) 

@bot.command()
async def 회원가입(ctx):
    print("회원가입이 가능한지 확인합니다.")
    userExistance, userRow = checkUser(ctx.author.name, ctx.author.id)
    if userExistance:
        print("DB에서 ", ctx.author.name, "을 찾았습니다.")
        print("------------------------------\n")
        await ctx.send("이미 가입하셨습니다.")
    else:
        print("DB에서 ", ctx.author.name, "을 찾을 수 없습니다")
        print("")

        Signup(ctx.author.name, ctx.author.id)

        print("회원가입이 완료되었습니다.")
        print("------------------------------\n")
        await ctx.send("회원가입이 완료되었습니다.")

@bot.command()
async def 탈퇴(ctx):
    print("탈퇴가 가능한지 확인합니다.")
    userExistance, userRow = checkUser(ctx.author.name, ctx.author.id)
    if userExistance:
        DeleteAccount(userRow)
        print("탈퇴가 완료되었습니다.")
        print("------------------------------\n")

        await ctx.send("탈퇴가 완료되었습니다.")
    else:
        print("DB에서 ", ctx.author.name, "을 찾을 수 없습니다")
        print("------------------------------\n")

        await ctx.send("등록되지 않은 사용자입니다.")

@bot.command()
async def 내정보(ctx):
    userExistance, userRow = checkUser(ctx.author.name, ctx.author.id)

    if not userExistance:
        print("DB에서 ", ctx.author.name, "을 찾을 수 없습니다")
        print("------------------------------\n")
        await ctx.send("회원가입 후 자신의 정보를 확인할 수 있습니다.")
    else:
        level, exp, money, loss = userInfo(userRow)
        rank = getRank(userRow)
        userNum = checkUserNum()
        expToUP = level*level + 6*level
        boxes = int(exp/expToUP*20)
        print("------------------------------\n")
        embed = discord.Embed(title="유저 정보", description = ctx.author.name, color = 0x62D0F6)
        embed.add_field(name = "레벨", value = level)
        embed.add_field(name = "순위", value = str(rank) + "/" + str(userNum))
        embed.add_field(name = "XP: " + str(exp) + "/" + str(expToUP), value = boxes * ":blue_square:" + (20-boxes) * ":white_large_square:", inline = False)
        embed.add_field(name = "보유 자산", value = money, inline = False)
        embed.add_field(name = "도박으로 날린 돈", value = loss, inline = False)

        await ctx.send(embed=embed)

@bot.command()
async def 정보(ctx, user: discord.User):
    userExistance, userRow = checkUser(user.name, user.id)

    if not userExistance:
        print("DB에서 ", user.name, "을 찾을 수 없습니다")
        print("------------------------------\n")
        await ctx.send(user.name  + " 은(는) 등록되지 않은 사용자입니다.")
    else:
        level, exp, money, loss = userInfo(userRow)
        rank = getRank(userRow)
        userNum = checkUserNum()
        print("------------------------------\n")
        embed = discord.Embed(title="유저 정보", description = user.name, color = 0x62D0F6)
        embed.add_field(name = "레벨", value = level)
        embed.add_field(name = "경험치", value = str(exp) + "/" + str(level*level + 6*level))
        embed.add_field(name = "순위", value = str(rank) + "/" + str(userNum))
        embed.add_field(name = "보유 자산", value = money, inline = False)
        embed.add_field(name = "도박으로 날린 돈", value = loss, inline = False)

        await ctx.send(embed=embed)

@bot.command()
async def 송금(ctx, user: discord.User, money):
    print("송금이 가능한지 확인합니다.")
    senderExistance, senderRow = checkUser(ctx.author.name, ctx.author.id)
    receiverExistance, receiverRow = checkUser(user.name, user.id)

    if not senderExistance:
        print("DB에서", ctx.author.name, "을 찾을수 없습니다")
        print("------------------------------\n")
        await ctx.send("회원가입 후 송금이 가능합니다.")
    elif not receiverExistance:
        print("DB에서 ", user.name, "을 찾을 수 없습니다")
        print("------------------------------\n")
        await ctx.send(user.name  + " 은(는) 등록되지 않은 사용자입니다.")
    else:
        print("송금하려는 돈: ", money)

        s_money = getMoney(ctx.author.name, senderRow)
        r_money = getMoney(user.name, receiverRow)

        if s_money >= int(money) and int(money) != 0:
            print("돈이 충분하므로 송금을 진행합니다.")
            print("")

            remit(ctx.author.name, senderRow, user.name, receiverRow, money)

            print("송금이 완료되었습니다. 결과를 전송합니다.")

            embed = discord.Embed(title="송금 완료", description = "송금된 돈: " + money, color = 0x77ff00)
            embed.add_field(name = "보낸 사람: " + ctx.author.name, value = "현재 자산: " + str(getMoney(ctx.author.name, senderRow)))
            embed.add_field(name = "→", value = ":moneybag:")
            embed.add_field(name="받은 사람: " + user.name, value="현재 자산: " + str(getMoney(user.name, receiverRow)))
                    
            await ctx.send(embed=embed)
        elif int(money) == 0:
            await ctx.send("0원을 보낼 필요는 없죠")
        else:
            print("돈이 충분하지 않습니다.")
            print("송금하려는 돈: ", money)
            print("현재 자산: ", s_money)
            await ctx.send("돈이 충분하지 않습니다. 현재 자산: " + str(s_money))

        print("------------------------------\n")


@bot.command()
async def reset(ctx):
    resetData()

@bot.command()
async def add(ctx, money):
    user, row = checkUser(ctx.author.name, ctx.author.id)
    addMoney(row, int(money))
    print("money")

@bot.command()
async def exp(ctx, exp):
    user, row = checkUser(ctx.author.name, ctx.author.id)
    addExp(row, int(exp))
    print("exp")

@bot.command()
async def lvl(ctx, lvl):
    user, row = checkUser(ctx.author.name, ctx.author.id)
    adjustlvl(row, int(lvl))
    print("lvl")

@bot.command()
async def 홀짝(ctx, face, money):
    userExistance, userRow = checkUser(ctx.author.name, ctx.author.id)
    forecast = coin()
    result = ""
    betting = 0
    _color = 0x000000
    if userExistance:
        cur_money = getMoney(ctx.author.name, userRow)
        if int(money) >= 10:
            if cur_money >= int(money):
                if face == "홀" or face == "짝":
                    if forecast == face:
                        result = "성공"
                        _color = 0x00ff56

                        betting = int(money)

                        modifyMoney(ctx.author.name, userRow, 0.5*betting)
                    else:
                        result = "실패"
                        _color = 0xFF0000

                        betting = int(money)
                        
                        modifyMoney(ctx.author.name, userRow, -int(betting))
                        addLoss(ctx.author.name, userRow, int(betting))

                    embed = discord.Embed(title = "홀짝게임 결과", description = result, color = _color)
                    embed.add_field(name = "배팅금액", value = betting, inline = False)
                    embed.add_field(name = "현재 자산", value = getMoney(ctx.author.name, userRow), inline = False)

                    await ctx.send(embed=embed)

                else:
                    await ctx.send("홀 또는 짝을 입력하세요")
            else:
                await ctx.send("돈이 부족합니다. 현재자산: " + str(cur_money))
        else:
            await ctx.send("10원 이상만 배팅 가능합니다.")
    else:
        await ctx.send("홀짝게임은 회원가입 후 이용 가능합니다.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content == "!reset":
        await bot.process_commands(message)
        return
    else:
        userExistance, userRow = checkUser(message.author.name, message.author.id)
        channel = message.channel
        if userExistance:
            levelUp, lvl = levelupCheck(userRow)
            if levelUp:
                print(message.author, "가 레벨업 했습니다")
                print("")
                embed = discord.Embed(title = "레벨업", description = None, color = 0x00A260)
                embed.set_footer(text = message.author.name + "이 " + str(lvl) + "레벨 달성!")
                await channel.send(embed=embed)
            else:
                modifyExp(userRow, 1)
                print("------------------------------\n")

        await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("명령어를 찾지 못했습니다. !도움을 입력하여 명령어를 확인하세요.")

bot.run('your bot token')
