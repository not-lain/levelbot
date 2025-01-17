import discord
import os
import threading
from discord.ext import commands
import json
import datetime
import requests
import os.path
import random
import gspread
import re
from PIL import Image, ImageDraw ,ImageFont,ImageOps
import requests
from io import BytesIO


import gradio_client
import gradio as gr
from gradio_client import Client
from huggingface_hub import HfApi, list_models, list_liked_repos, list_metrics

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN", None)
intents = discord.Intents.all() 
bot = commands.Bot(command_prefix='!', intents=intents)


""""""
XP_PER_MESSAGE = 10 # 100k messages = 1M exp = lvl 100
""""""
service_account = json.loads(os.environ.get('KEY'))
file_path = 'service_account.json'
with open(file_path, 'w') as json_file:
    json.dump(service_account, json_file)
gspread_bot = gspread.service_account(filename='service_account.json')
worksheet = gspread_bot.open("levelbot").sheet1
worksheet2 = gspread_bot.open("hf_discord_verified_users_test").sheet1
""""""
bot_ids = [1136614989411655780, 1166392942387265536, 1158038249835610123, 1130774761031610388, 1155489509518098565, 1155169841276260546, 1152238037355474964, 1154395078735953930]
""""""
api = HfApi()
""""""


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print(f"XP_PER_MESSAGE: {XP_PER_MESSAGE}")

    
def calculate_level(xp):
    return int(xp ** (1.0 / 3.0))


def calculate_xp(level):
    return (int(level ** 3))


# use a command
# check xp record presence (done in add_exp)
# check discord_user_id is verified
# do add_exp for hub?
@bot.command(name='add_exp_hub')
async def add_exp_hub(ctx):
    try:
        column_values_7 = worksheet2.col_values(7)
        column_values_3 = worksheet2.col_values(3)
        
        for i, value in enumerate(column_values_7):
            if not value:
                print(f"cell empty, updating with likes")
                hf_user_name = column_values_3[i]
                print(f"hf_user_name = {hf_user_name}")
                try:
                    likes = list_liked_repos(f"{hf_user_name}")
                    hf_likes_new = likes.total
                    print(f"hf_likes_new = {hf_likes_new}")
                    worksheet2.update(f'G{i+1}', f'{hf_likes_new}')
                except Exception as e:
                    print(f"list_liked_repos Error: {e}")  
                        
    except Exception as e:
        print(f"add_exp_hub Error: {e}")  


@bot.command(name='api_test')
async def api_test(ctx):
    # take nate 
    column_values_3 = worksheet2.col_values(3)
    column_values_8 = worksheet2.col_values(8)
    #row_values_2 = worksheet2.row_values(2)

    for i, user in enumerate(column_values_3):
        if not column_values_8[i]:
            url = f"https://huggingface.co/api/users/{user}/overview"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
        
                likes = data["numLikes"]
                models = data["numModels"]
                datasets = data["numDatasets"]
                spaces = data["numSpaces"]
                discussions = data["numDiscussions"]
                papers = data["numPapers"]
                upvotes = data["numUpvotes"]
            
                worksheet2.update(values=[[likes, models, datasets, spaces, discussions, papers, upvotes]], range_name=f'G{i+1}:M{i+1}')
            else:
                print(f"Failed to retrieve data. Status code: {response.status_code}")  


@bot.command(name='get_cell_value')
async def get_cell_value(ctx, row, col):
    cell = worksheet2.cell(row, col)
    print(cell.value)


@bot.command(name='check')
async def check(ctx):
    try:
        column_values_7 = worksheet2.col_values(7)
        column_values_3 = worksheet2.col_values(3)
        
        for i, value in enumerate(column_values_7):
            print(i)
            print(value)
                        
    except Exception as e:
        print(f"add_exp_hub Error: {e}")  
        

async def add_exp(member_id):
    try:
        guild = bot.get_guild(879548962464493619)
        member = guild.get_member(member_id)
        lvl1 = guild.get_role(1171861537699397733)
        lvl2 = guild.get_role(1171861595115245699)
        lvl3 = guild.get_role(1171861626715115591)
        lvl4 = guild.get_role(1171861657975259206)
        lvl5 = guild.get_role(1171861686580412497)
        lvl6 = guild.get_role(1171861900301172736)
        lvl7 = guild.get_role(1171861936258941018)
        lvl8 = guild.get_role(1171861968597024868)
        lvl9 = guild.get_role(1171862009982242836)
        lvl10 = guild.get_role(1164188093713223721)
        lvl11 = guild.get_role(1171524944354607104)
        lvl12 = guild.get_role(1171524990257082458)
        lvl13 = guild.get_role(1171525021928263791)
        lvl14 = guild.get_role(1171525062201966724)
        lvl15 = guild.get_role(1171525098465918996)
        lvl16 = guild.get_role(1176826165546201099)
        lvl17 = guild.get_role(1176826221301092392)
        lvl18 = guild.get_role(1176826260643659776)
        lvl19 = guild.get_role(1176826288816791693)
        lvl20 = guild.get_role(1176826319447801896)
        lvls = {
            1: lvl1, 2: lvl2, 3: lvl3, 4: lvl4, 5: lvl5, 6: lvl6, 7: lvl7, 8: lvl8, 9: lvl9, 10: lvl10,
            11: lvl11, 12: lvl12, 13: lvl13, 14: lvl14, 15: lvl15, 16: lvl16, 17: lvl17, 18: lvl18, 19: lvl19, 20: lvl20,
        }        
        #if member.id == 811235357663297546:
        # does a record already exist?
        cell = worksheet.find(str(member.id))
        length = len(worksheet.col_values(1))
        if cell is None:
            print(f"creating new record for {member}")            
            # if not, create new record
            string_member_id = str(member.id)
            xp = 10
            current_level = calculate_level(xp)
            member_name = member.name
            worksheet.update(values=[[string_member_id, member_name, xp, current_level]], range_name=f'A{length+1}:D{length+1}')
            # initial role assignment
            if current_level == 1:
                if lvl1 not in member.roles:
                    await member.add_roles(lvl1)
                    print(f"Gave {member} {lvl1}")
        else:
            if cell:
                # if so, update that row...
                xp = worksheet.cell(cell.row, cell.col+2).value
                xp = int(xp) + XP_PER_MESSAGE
                current_level = calculate_level(xp)
                print(f"updating record for {member}: {xp} xp")
                # write with added xp
                worksheet.update(values=[[xp, current_level]], range_name=f'C{cell.row}:D{cell.row}')   
                # level up
                if current_level >= 2 and current_level <=20:
                    current_role = lvls[current_level]
                    if current_role not in member.roles:
                        await member.add_roles(current_role)
                        print(f"Gave {member} {current_role}")
                        await member.remove_roles(lvls[current_level-1])
                        print(f"Removed {lvls[current_level-1]} from {member}")  
                        #print(f"{member} Level up! {current_level-1} -> {current_level}!")
                        await member.send(f"Level up! {current_level-1} -> {current_level}!")
                        
    except Exception as e:
        print(f"add_exp Error: {e}")   


@bot.event
async def on_message(message):
    try:
        if message.author.id not in bot_ids:
            await add_exp(message.author.id)
        await bot.process_commands(message)
    except Exception as e:
        print(f"on_message Error: {e}")

        
@bot.event
async def on_reaction_add(reaction, user):
    try:
        if user.id not in bot_ids:
            await add_exp(user.id)
    except Exception as e:
        print(f"on_reaction_add Error: {e}")


def create_progress_bar(w = 800,h = 100 ,progress_percentage=0.25):
    progress = Image.new("RGB", (w,h)) 
    draw = ImageDraw.Draw(progress)
    draw_progress(20, h*0.5, w-20*3, 25, progress_percentage,draw)
    return progress
def draw_progress(x, y, width, height, progress_percentage,draw, fg="#FFD21E", fg2="#6B7280"):
    # Draw the background
    draw.rectangle((x+(height/2), y, x+width+(height/2), y+height), fill=fg2, width=10)
    draw.ellipse((x+width, y, x+height+width, y+height), fill=fg2)
    draw.ellipse((x, y, x+height, y+height), fill=fg2)
    width = int(width*progress_percentage)
    # Draw the part of the progress bar that is actually filled
    draw.rectangle((x+(height/2), y, x+width+(height/2), y+height), fill=fg, width=10)
    draw.ellipse((x+width, y, x+height+width, y+height), fill=fg)
    draw.ellipse((x, y, x+height, y+height), fill=fg)

def create_base(w=800,h = 300,username = "username",current_xp=25,next_lvl_xp=100):
    base = Image.new("RGB",(w,h))
    draw = ImageDraw.Draw(base)
    # requires a newer version of pillow
    font = ImageFont.load_default(size=50) # big text
    draw.text((20, 20),username,(255,255,255),font=font)
    font = ImageFont.load_default(size=30)
    xp_msg = f"{current_xp}/{next_lvl_xp} XP"
    pad = font.getlength(xp_msg)
    draw.text((w-30-pad, h-50),xp_msg,(255,255,255),font=font)
    return base


async def process_avatar(url,hugg = True):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    # resize image to a square
    img = ImageOps.fit(img, (189, 189))

    # create circular mask
    mask = Image.new('L', (189, 189), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, 189, 189), fill=255)
    # apply mask to image
    img.putalpha(mask)
    if hugg :
      img2 = Image.open("./assets/hugg.png")
      img.paste(img2,(0,0),img2)
    return img


# AI prediction command
@bot.hybrid_command(
    name="lvl",
    description="get the level of a user",
)
async def lvl(ctx):
    username=ctx.author.name
    url = ctx.author.display_avatar.url
    # TODO : 
    # get the level of a user
    # get next lvl xp
    current_xp = 25 
    next_lvl_xp = 100
    progress_percentage = current_xp/next_lvl_xp
    base = create_base(username=username,current_xp=current_xp,next_lvl_xp=next_lvl_xp)
    progress = create_progress_bar(progress_percentage=progress_percentage)
    avatar = await process_avatar(url)
    final = Image.new("RGB",(base.size[0],base.size[1]+progress.size[1]))
    final.paste(base,(0,0))
    final.paste(progress,(0,base.size[1]))
    x_begin = final.size[0]-189-20
    final.paste(avatar,(x_begin,20,x_begin+189,20+189),avatar)
    with BytesIO() as image_binary:
                    final.save(image_binary, 'PNG')
                    image_binary.seek(0)
                    await ctx.send(file=discord.File(fp=image_binary, filename=f'{username}.png'))




""""""
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN", None)
def run_bot():
    bot.run(DISCORD_TOKEN)
threading.Thread(target=run_bot).start()
def greet(name):
    return "Hello " + name + "!"
demo = gr.Interface(fn=greet, inputs="text", outputs="text")
demo.launch()    
