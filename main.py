import requests
from bs4 import BeautifulSoup
import discord
from datetime import datetime, time, timedelta, date
import asyncio

today = date.today()
now = datetime.now()
d3 = today.strftime("%m/%d/%y")

current_time = now.strftime("%H:%M:%S")

url = 'http://103.247.238.92/webportal/pages/covid19.php'
reqs = requests.get(url)
soup = BeautifulSoup(reqs.text, 'lxml')
info_list = soup.find_all("span", class_="info-box-number")

total_lab_tests = info_list[0].text
total_confirmed = info_list[1].text
total_isolated = info_list[2].text
total_recovered = info_list[3].text
total_deaths = info_list[4].text
second_dose_administrated = info_list[5].text
today_lab_tests = info_list[6].text
today_confirmed = info_list[7].text
today_isolated = info_list[8].text
today_recovered = info_list[9].text
today_deaths = info_list[10].text

client = discord.Client()


WHEN = time(20, 12, 30)
channel_id = 837606361373081670  # Put your channel id here


@client.event
async def on_ready():
    print('I have logged in as {0.user}'.format(client))


async def called_once_a_day():  # Fired every day
    await client.wait_until_ready()  # Make sure your guild cache is ready so the channel can be found via get_channel
    channel = client.get_channel(
        channel_id)
    embed = discord.Embed(title="Corona Update", color=0xff0000)
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/avatars/837600602513997864/cc765ea6da31e08c822aa6e1395e1f6c.webp?size=128")
    embed.add_field(name="All Time", value="-----------", inline=False)
    embed.add_field(name="🧪Lab Tests", value=total_lab_tests, inline=True)
    embed.add_field(name="✅Confirmed", value=total_confirmed, inline=True)
    embed.add_field(name="😷Isolated", value=total_isolated, inline=True)
    embed.add_field(name="👪Recovered", value=total_recovered, inline=True)
    embed.add_field(name="💀Deaths", value=total_deaths, inline=True)
    embed.add_field(name="💉2nd Dose Administrated", value=second_dose_administrated, inline=True)
    embed.add_field(name="-------------------------------------------------------------------------------",
                    value="|", inline=True)
    embed.add_field(name="Today", value="--------", inline=False)
    embed.add_field(name="🧪Lab Tests", value=today_lab_tests, inline=False)
    embed.add_field(name="✅Confirmed", value=today_confirmed, inline=False)
    embed.add_field(name="😷Isolated", value=today_isolated, inline=False)
    embed.add_field(name="👪Recovered", value=today_recovered, inline=False)
    embed.add_field(name="💀Deaths", value=today_deaths, inline=False)
    embed.set_footer(text="Last updated: " + current_time + " " + d3)

    await channel.send(embed=embed)


async def background_task():
    now = datetime.now()
    if now.time() > WHEN:
        tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
        seconds = (tomorrow - now).total_seconds()  # Seconds until tomorrow (midnight)
        await asyncio.sleep(seconds)  # Sleep until tomorrow and then the loop will start
    while True:
        now = datetime.now()
        target_time = datetime.combine(now.date(), WHEN)
        seconds_until_target = (target_time - now).total_seconds()
        await asyncio.sleep(seconds_until_target)  # Sleep until we hit the target time
        await called_once_a_day()  # Call the helper function that sends the message
        tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
        seconds = (tomorrow - now).total_seconds()  # Seconds until tomorrow (midnight)
        await asyncio.sleep(seconds)  # Sleep until tomorrow and then the loop will start a new iteration


if __name__ == "__main__":
    client.loop.create_task(background_task())
    client.run("ODM3NjAwNjAyNTEzOTk3ODY0.YIu6WQ.oISPzjp8QmnTYegBPjKUGAsDsLE")
