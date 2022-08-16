import discord
client = discord.Client()

@client.event
async def on_ready():
    print('{0.user} : Log in'.format(client))
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name='///'))
    print('{0.user} : Log in'.format(client))
    print('Ready to start')

from urllib.request import urlopen
import xmltodict
import os
'''
@bot.command(description="Input your Simbrief Username")
async def simbrief(ctx,
    user : Option(str, "Username")
):
    await brief(ctx, user)
'''
@client.event
async def on_message(message):
    if message.content.startswith("+fp "):
        await brief(message)
        return
    if message.content=="!test":
        await message.channel.send("Test")
        return
async def brief(message):
    msg = await.message.channel.send("``Loading...``")
    up = message.content.replace("+fp ","")
    user = up
    url = urlopen("https://www.simbrief.com/api/xml.fetcher.php?username={0}".format(user))
    file_url = "https://www.simbrief.com/ofp/flightplans/"
    img_url = "https://www.simbrief.com/ofp/uads/"
    data = url.read()
    data = xmltodict.parse(data)
    xml = data['OFP']
    xml_fetch = xml['fetch']
    xml_params = xml['params']
    xml_general = xml['general']
    xml_origin = xml['origin']
    xml_destination = xml['destination']
    xml_alternate = xml['alternate']
    xml_file = xml['files']
    xml_img = xml['images']
    xml_fuel = xml['fuel']
    xml_weights = xml['weights']
    xml_aircraft = xml['aircraft']
    pd = xml_file['pdf']
    pd1 = pd['link']
    img = xml_img['map']
    img = img[0]
    im = img['link']
    pdf = file_url + pd1
    img = img_url + im
    response_time = xml_fetch['time']
    aircraft = xml_aircraft['name']
    icao_airline = xml_general["icao_airline"]
    flight_number = xml_general["flight_number"]
    airac = xml_params['airac']
    units = xml_params['units']
    costindex = xml_general['costindex']
    route = xml_general['route']
    ori_icao = xml_origin['icao_code']
    ori_rwy = xml_origin['plan_rwy']
    ori_metar = xml_origin['metar']
    des_icao = xml_destination['icao_code']
    des_rwy = xml_destination['plan_rwy']
    des_metar = xml_destination['metar']
    alt_icao = xml_alternate['icao_code']
    alt_rwy = xml_alternate['plan_rwy']
    alt_metar = xml_alternate['metar'] 
    fuel_alt = xml_fuel['alternate_burn']
    fuel_res = xml_fuel['reserve']
    fuel_block = xml_fuel['plan_ramp']
    payload = xml_weights['payload']

    # await ctx.respond(f"{response_time}{aircraft}{airac}{units}{costindex}{route}{ori_icao}{ori_rwy}{ori_metar}{des_icao}{des_rwy}{des_metar}{alt_icao}{alt_rwy}{alt_metar}{fuel_alt}{fuel_res}{fuel_block}{payload}")
    # print(response_time,aircraft,airac,units,costindex,route,ori_icao,ori_rwy,ori_metar,des_icao,des_rwy,des_metar,alt_icao,alt_rwy,alt_metar,fuel_alt,fuel_res,fuel_block,payload)
    # await message.channel.send(f"{response_time}{aircraft}{airac}{units}{costindex}{route}{ori_icao}{ori_rwy}{ori_metar}{des_icao}{des_rwy}{des_metar}{alt_icao}{alt_rwy}{alt_metar}{fuel_alt}{fuel_res}{fuel_block}{payload}")
    brief_emb=discord.Embed(title="**Click to view full Plan (OFP)**", url=pdf, description=f"User : ``{user}``, Airac ver : ``{airac}``, Unit : ``{units}``\n Aircraft : ``{aircraft}``,  Airline : ``{icao_airline} (Num. {flight_number})``", color=0x2ec0ff)
    brief_emb.add_field(name="Origin", value=f"{ori_icao}/``{ori_rwy}``", inline=True)
    brief_emb.add_field(name="Destination", value=f"{des_icao}/``{des_rwy}``", inline=True)
    brief_emb.add_field(name="Alternate", value=f"{alt_icao}/``{alt_rwy}``", inline=True)
    brief_emb.add_field(name="Route", value=f"``{route}``", inline=True)
    brief_emb.add_field(name="Metar for Origin", value=f"{ori_metar}", inline=False)
    brief_emb.add_field(name="Metar for Destination", value=f"{des_metar}", inline=False)
    brief_emb.add_field(name="Block fuel ", value=f"{fuel_block}", inline=False)
    brief_emb.add_field(name="Payload", value=f"{payload}", inline=True)
    brief_emb.add_field(name="Other Things", value=f"FINRES fuel : {fuel_res}\nAlternate_burn fuel : {fuel_alt}\nCost Index : {costindex}", inline=False)
    brief_emb.set_image(url=img)
    brief_emb.set_footer(text=f"Source from : Simbrief | Response time {response_time}s")
    await msg.delete()
    await message.channel.send(embed = brief_emb)
    return
TOKEN = os.environ.get('TOKEN')
client.run(TOKEN)
