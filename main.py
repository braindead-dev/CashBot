# config
prefix = "$"
token = "YOUR_DISCORD_TOKEN"

# imports
import discord
from discord.ext import commands
from messages import *
import asyncio
import re
from datetime import datetime, timezone

bot = discord.Client()

# mod imports
import os
from time import sleep
from login import *
import random
import string

# defines bot
bot = commands.Bot(command_prefix=prefix)
bot.remove_command("help")

# function when bot is loaded
@bot.event
async def on_ready():
    print("Successfully logged in.")

# help
@bot.command()
async def help(ctx):
    reply = await ctx.reply(content="", embed=help_message, mention_author=False)
    await reply.add_reaction("✅")

    def check_reply(reaction, user):
        return user == ctx.message.author

    try:
        reaction, user = await bot.wait_for("reaction_add", check=check_reply)
    except asyncio.TimeoutError:
        await reply.delete()
        await ctx.message.delete()
    else:
        if str(reaction.emoji) == "✅":
            await reply.delete()
            await ctx.message.delete()

# change status of bot (secret owner only command)
@bot.command()
async def setstatus(ctx):
    cmd_access = False
    with open("admin/adminlist.txt") as f:
        if str(ctx.message.author.id) in f.read():
            cmd_access = True
    
    if cmd_access == True:
        await ctx.message.delete()
        try:
            sender_message = ctx.message
            objects = sender_message.content.split(" ")
            want_status = objects[1]
            try:
                statusparse = re.findall(r'"([^"]*)"', sender_message.content)
                var2 = statusparse[0]
                try:
                    var3 = statusparse[1]
                except:
                    pass
            except:
                pass

            try:
                if want_status == "game":
                    await bot.change_presence(activity=discord.Game(name=var2))
                if want_status == "streaming":
                    await bot.change_presence(
                        activity=discord.Streaming(
                            name=var2, url="https://twitch.tv/" + var3
                        )
                    )
                if want_status == "listening":
                    await bot.change_presence(
                        activity=discord.Activity(
                            type=discord.ActivityType.listening, name=var2
                        )
                    )
                if want_status == "watching":
                    await bot.change_presence(
                        activity=discord.Activity(
                            type=discord.ActivityType.watching, name=var2
                        )
                    )
                if want_status == "none":
                    try:
                        await bot.change_presence(activity=None)
                    except:
                        pass

                try:
                    reply = await ctx.reply(content="",embed=generic_success_message, mention_author=False)
                    print("generr_1")
                    sleep(5.0)
                    await reply.delete()
                    await ctx.message.delete()

                except:
                    reply = await ctx.reply(content="",embed=generic_error_message, mention_author=False)
                    print("generr_2")
                    sleep(5.0)
                    await reply.delete()
                    await ctx.message.delete()
            

            except:
                pass
        
        except:
            pass

# get basic account info
@bot.command()
async def info(ctx):
    cookie="[null]"
    proceed = False
    try:
        with open("credentials/"+str(ctx.message.author.id)+".txt", mode = "r") as userfile:
            cookie = userfile.read()
            result_json = get_info(cookie)
            proceed = True

    except:
        #this exception usually means no account has been linked
        reply = await ctx.reply(content="",embed=no_linked_account, mention_author=False)
        sleep(5.0)
        await reply.delete()
        await ctx.message.delete()

    if proceed == True:
        try:
            full_name = result_json["profile"]["full_name"]
            photo_url = result_json["profile"]["photo_url"]

            #try:
            #    email = result_json["profile"]["aliases"][0]["alias"]["canonical_text"]
            #except:
            #    email = "[NULL]"
            #try:
            #    sms = result_json["profile"]["aliases"][0]["alias"]["canonical_text"]
            #except:
            #    sms = "[NULL]"
            #if email == "[NULL]":
            #    try:
            #        email = result_json["profile"]["aliases"][1]["alias"]["canonical_text"]
            #    except:
            #        email = "[NULL]"
            #if sms == "[NULL]":
            #    try:
            #        sms = result_json["profile"]["aliases"][1]["alias"]["canonical_text"]
            #    except:
            #        sms = "[NULL]"
            
            cashtag = result_json["profile"]["cashtag_with_currency_symbol"]
            cashtag_qr_image_url = result_json["profile"]["cashtag_qr_image_url"]

            #address_line_1 = result_json["profile"]["postal_address"]["address_line_1"]
            #city = result_json["profile"]["postal_address"]["locality"]
            #state = result_json["profile"]["postal_address"]["administrative_district_level_1"]
            #country_code = result_json["profile"]["postal_address"]["country_code"]

            embed = embed=discord.Embed(title="User Info", description="**"+full_name+"**\nCashtag: `"+cashtag+"`", color=0x00d632)
            embed.set_thumbnail(url=photo_url)
            embed.set_image(url=cashtag_qr_image_url)
            #embed.add_field(name=full_name, value="\n\nEmail: `"+email+"`\nSMS: `"+sms+"`\nCashtag: `"+cashtag+"`\nAddress: `" + address_line_1 + ", " + city + " " + state + ", " + country_code + "`", inline=False)

            reply = await ctx.reply(content="", embed = embed, mention_author=False)

        except:
            reply = await ctx.reply(content="", embed=generic_error_message, mention_author=False)
            print("generr_3")
            sleep(5.0)
            await reply.delete()
            await ctx.message.delete()

    sleep(10)
    await reply.delete()
    await ctx.message.delete()

# get detailed account info
@bot.command()
async def moreinfo(ctx):
    reply = await ctx.reply(content="This function is still in development.", mention_author=False)
    sleep(7.5)
    await reply.delete()
    await ctx.message.delete()

# set up bot for a server
@bot.command()
async def servermode(ctx):
    # step by step proccess; wait for continue/back/cancel command(s) to go through the steps.
    sender_message = ctx.message
    try:
        objects = sender_message.content.split(" ")
        on_or_off = objects[1]
    except:
        reply = await ctx.reply(content="",embed=invalid_input, mention_author=False)
        sleep(5.0)
        await reply.delete()
        await ctx.message.delete()
        
    command_server_id = ctx.message.guild.id

    if on_or_off.upper() == "ON":

        reply = await ctx.reply(content="", embed=server_setup_1, mention_author=False)
        await reply.add_reaction("✅")
        await reply.add_reaction("❌")

        def check_reply(reaction, user):
            return user == ctx.message.author 

        try:
            reaction, user = await bot.wait_for("reaction_add", check=check_reply)
        except asyncio.TimeoutError:
            await reply.delete()
        else:
            await reply.delete()
            
            if str(reaction.emoji) == "❌":
                reply = await ctx.reply(content="",embed=canceled_setup, mention_author=False)
                sleep(5.0)
                await reply.delete()
                await ctx.message.delete()

            if str(reaction.emoji) == "✅":
                # verify admin perms and linked account
                if ctx.message.author.guild_permissions.administrator:

                    proceed = False
                    try:
                        with open("credentials/"+str(ctx.message.author.id)+".txt", mode = "r") as userfile:
                            proceed = True

                    except:
                        #this exception usually means no account has been linked
                        reply = await ctx.reply(content="",embed=no_linked_account, mention_author=False)
                        sleep(5.0)
                        await reply.delete()
                        await ctx.message.delete()

                    if proceed == True:

                        proceed = False
                        try:
                            with open("servers/"+str(command_server_id)+".txt", mode = "r") as userfile:
                                reply = await ctx.reply(content="",embed=already_on_error, mention_author=False)
                                sleep(5.0)
                                await reply.delete()
                                await ctx.message.delete()
                                proceed = False
                        except:
                            proceed = True

                        if proceed == True:
                            # enable server mode ; record  guild/server id and mark as enabled, as well as default servwide settings; 
                            def turn_on_servermode(command_server_id):
                                with open("servers/"+str(command_server_id)+".txt", mode = "w") as userfile:
                                    userfile.write(str(command_server_id) + "\n[TEST_SETTING]=True")

                            turn_on_servermode(command_server_id)
                            reply = await ctx.reply(content="", embed=server_setup_2, mention_author=False)
                            sleep(5.0)
                            await reply.delete()
                            await ctx.message.delete()

                else:
                    reply = await ctx.reply(content="",embed=no_admin_perms, mention_author=False)
                    sleep(5.0)
                    await reply.delete()
                    await ctx.message.delete()

    elif on_or_off.upper() == "OFF":

        reply = await ctx.reply(content="", embed=unlink_message, mention_author=False)
        await reply.add_reaction("✅")
        await reply.add_reaction("❌")

        def check_reply(reaction, user):
            return user == ctx.message.author

        try:
            reaction, user = await bot.wait_for("reaction_add", check=check_reply)
        except asyncio.TimeoutError:
            await reply.delete()
        else:
            await reply.delete()

            if str(reaction.emoji) == "❌":
                    reply = await ctx.reply(content="",embed=canceled_setup, mention_author=False)
                    sleep(5.0)
                    await reply.delete()
                    await ctx.message.delete()
            
            if str(reaction.emoji) == "✅":
                proceed = False
                try:
                    with open("servers/"+str(command_server_id)+".txt", mode = "r") as userfile:
                        proceed = True
                except:
                    reply = await ctx.reply(content="",embed=already_off_error, mention_author=False)
                    sleep(5.0)
                    await reply.delete()
                    await ctx.message.delete()
                    proceed = True

                if proceed == True:
                    try:
                        os.remove("servers/"+str(command_server_id)+".txt") 
                        reply = await ctx.reply(content="",embed=generic_success_message, mention_author=False)
                        print("generr_4")
                        sleep(5.0)
                        await reply.delete()
                        await ctx.message.delete()
                    except:
                        reply = await ctx.reply(content="",embed=generic_error_message, mention_author=False)
                        print("generr_5")
                        sleep(5.0)
                        await reply.delete()
                        await ctx.message.delete()

# get a list of recent transactions
@bot.command()
async def transactions(ctx):
    reply = await ctx.reply(content="This function is still in development.", mention_author=False)
    sleep(7.5)
    await reply.delete()
    await ctx.message.delete()

# update your credentials
@bot.command()
async def update(ctx):

    def save_userinfo(user_cookies):
        with open("credentials/"+str(ctx.message.author.id)+".txt", mode = "w") as userfile:
            userfile.write(user_cookies)
                
    reply = await ctx.reply(content="", embed=update_message, mention_author=False)

    message = await bot.wait_for("message")
    await reply.delete()

    if len(message.content) == 632:
        reply = await ctx.reply(content="",embed=setup_message5, mention_author=False)
        user_cookies = message.content
        await message.delete()
        try:
            save_userinfo(user_cookies)
        except:
            pass
        sleep(5.0)
        await reply.delete()
        await ctx.message.delete()

    elif message.content == "❌":
        reply = await ctx.reply(content="",embed=canceled_setup, mention_author=False)
        sleep(5.0)
        await reply.delete()
        await message.delete()
        await ctx.message.delete()

    else:
        reply = await ctx.reply(content="",embed=invalid_input, mention_author=False)
        sleep(5.0)
        await reply.delete()
        await message.delete()
        await ctx.message.delete()

# setup
@bot.command()
async def link(ctx):

    # step by step proccess; wait for continue/back/cancel command(s) to go through the steps. Paste cookies
    reply = await ctx.reply(content="", embed=setup_message, mention_author=False)
    await reply.add_reaction("✅")
    await reply.add_reaction("❌")

    def check_reply(reaction, user):
        return user == ctx.message.author 

    command_user_id = ctx.message.author.id

    try:
        reaction, user = await bot.wait_for("reaction_add", check=check_reply)
    except asyncio.TimeoutError:
        await reply.delete()
    else:
        await reply.delete()

        if str(reaction.emoji) == "❌":
                reply = await ctx.reply(content="",embed=canceled_setup, mention_author=False)
                sleep(5.0)
                await reply.delete()
                await ctx.message.delete()
        
        if str(reaction.emoji) == "✅":
            # step 2 (login to cashapp on the web)
            reply = await ctx.reply(content="", embed=setup_message2, mention_author=False)
            await reply.add_reaction("✅")
            await reply.add_reaction("❌")

            try:
                reaction, user = await bot.wait_for("reaction_add", check=check_reply)

            except asyncio.TimeoutError:
                await reply.delete()
            else:
                await reply.delete()

                if str(reaction.emoji) == "❌":
                    reply = await ctx.reply(content="",embed=canceled_setup, mention_author=False)
                    sleep(5.0)
                    await reply.delete()
                    await message.delete()
                    await ctx.message.delete()

                if str(reaction.emoji) == "✅":
                    reply = await ctx.reply(content="",embed=setup_message3, mention_author=False)
                    await reply.add_reaction("✅")
                    await reply.add_reaction("❌")

                    
                    try:
                        reaction, user = await bot.wait_for("reaction_add", check=check_reply)

                    except asyncio.TimeoutError:
                        await reply.delete()
                    else:
                        await reply.delete()

                        if str(reaction.emoji) == "❌":
                            reply = await ctx.reply(content="",embed=canceled_setup, mention_author=False)
                            sleep(5.0)
                            await reply.delete()
                            await message.delete()
                            await ctx.message.delete()


                        if str(reaction.emoji) == "✅":

                            reply = await ctx.reply(content="",embed=setup_message4, mention_author=False)

                            message = await bot.wait_for("message")
                            await reply.delete()

                            def save_userinfo(user_cookies):
                                with open("credentials/"+str(command_user_id)+".txt", mode = "w") as userfile:
                                    userfile.write(user_cookies)

                            if ctx.message.author.id == command_user_id:
                                try:

                                    if len(message.content) == 632:
                                        reply = await ctx.reply(content="",embed=setup_message5, mention_author=False)
                                        user_cookies = message.content
                                        await message.delete()
                                        try:
                                            save_userinfo(user_cookies)
                                        except:
                                            pass
                                        sleep(5.0)
                                        await reply.delete()
                                        await ctx.message.delete()

                                    elif message.content == "❌":
                                        reply = await ctx.reply(content="",embed=canceled_setup, mention_author=False)
                                        sleep(5.0)
                                        await reply.delete()
                                        await message.delete()
                                        await ctx.message.delete()
                                        
                                    else:
                                        reply = await ctx.reply(content="",embed=invalid_input, mention_author=False)
                                        sleep(5.0)
                                        await reply.delete()
                                        await message.delete()
                                        await ctx.message.delete()
                                except:
                                    reply = await ctx.reply(content="",embed=invalid_input, mention_author=False)
                                    sleep(5.0)
                                    await reply.delete()
                                    await message.delete()
                                    await ctx.message.delete()

# unlink account delete file
@bot.command()
async def unlink(ctx):
    command_user_id = ctx.message.author.id

    reply = await ctx.reply(content="", embed=unlink_message, mention_author=False)
    await reply.add_reaction("✅")
    await reply.add_reaction("❌")

    def check_reply(reaction, user):
        return user == ctx.message.author

    try:
        reaction, user = await bot.wait_for("reaction_add", check=check_reply)
    except asyncio.TimeoutError:
        await reply.delete()
    else:
        await reply.delete()

        if str(reaction.emoji) == "❌":
                reply = await ctx.reply(content="",embed=canceled_setup, mention_author=False)
                sleep(5.0)
                await reply.delete()
                await ctx.message.delete()
        
        if str(reaction.emoji) == "✅":
            proceed = False
            try:
                with open("credentials/"+str(command_user_id)+".txt", mode = "r") as userfile:
                    reply = await ctx.reply(content="",embed=already_off_error, mention_author=False)
                    sleep(5.0)
                    await reply.delete()
                    await ctx.message.delete()
                    proceed = False
            except:
                proceed = True

            if proceed == True:
                try:
                    os.remove("credentials/"+str(command_user_id)+".txt") 
                    reply = await ctx.reply(content="",embed=generic_success_message, mention_author=False)
                    print("generr_6")
                    sleep(5.0)
                    await reply.delete()
                    await ctx.message.delete()
                except:
                    reply = await ctx.reply(content="",embed=generic_error_message, mention_author=False)
                    print("generr_7")
                    sleep(5.0)
                    await reply.delete()
                    await ctx.message.delete()

# make invoice - add features priority
@bot.command()
async def invoice(ctx):
    sender_message = ctx.message

    try:
        objects = sender_message.content.split(" ")
        initial_int_amount = objects[1]
    except:
        reply = await ctx.reply(content="",embed=invalid_input, mention_author=False)
        sleep(5.0)
        await reply.delete()
        await ctx.message.delete()

    cookie="[null]"
    proceed = ""

    def create_txt_invoice(random_invoice_id, random_note, current_time, cashtag, int_amount, photo_url, cashtag_qr_image_url):
        current_time = str(current_time)
        with open("invoices/"+str(random_invoice_id)+".txt", mode = "w") as userfile:
            userfile.write("INVOICE_ID[" + random_invoice_id + "],NOTE[" + random_note + "],AMOUNT[" + int_amount + "],TIME[" + current_time + "],PURL[" + photo_url + "],CT_IMAGE[" + cashtag_qr_image_url + "], CT[" + cashtag + "]")

    try:
        with open("credentials/"+str(ctx.message.author.id)+".txt", mode = "r") as userfile:
            cookie = userfile.read()
            result_json = get_info(cookie)

    except:
        #this exception usually means no account has been linked
        reply = await ctx.reply(content="",embed=no_linked_account, mention_author=False)
        sleep(5.0)
        await reply.delete()
        await ctx.message.delete()
    
    try:
        whole_number_amount = initial_int_amount.split('.')[0]
        decimal_amount = initial_int_amount.split('.')[1]
        decimal_exists = True
    except:
        decimal_exists = False

    if decimal_exists == True:

        if len(decimal_amount) == 2:
            int_amount = whole_number_amount + "." + decimal_amount
            
        if len(decimal_amount) == 1:
            int_amount = whole_number_amount + "." + decimal_amount + "0"
        
        else:
            proceed = False
            reply = await ctx.reply(content="",embed=invalid_input, mention_author=False)
            sleep(5.0)
            await reply.delete()
            await ctx.message.delete()
            

    if decimal_exists == False:
        int_amount = initial_int_amount + ".00"

    if float(int_amount) > 7500:
        proceed = False
        reply = await ctx.reply(content="",embed=invalid_input, mention_author=False)
        sleep(5.0)
        await reply.delete()
        await ctx.message.delete()

    if proceed != False:
        try:
            random_invoice_id = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(12))
            random_note = ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(6))


            photo_url = result_json["profile"]["photo_url"]
            cashtag = result_json["profile"]["cashtag_with_currency_symbol"]
            cashtag_qr_image_url = result_json["profile"]["cashtag_qr_image_url"]
            current_time = datetime.now(timezone.utc)
            user_info = discord.Embed(title="Invoice Info", description="", color=0x00d632)
            payment_details_message = "Cashtag: `" + cashtag + "`\nAmount: `$" + int_amount + "`\n\n**Note:  " + random_note + "**\n*You MUST put this code in the notes section when paying*\n\n`🔄 to refresh the status`\n`🗑️ to delete this invoice`\n`❌ to remove this message`"
            user_info.add_field(name="Payment Details", value=payment_details_message, inline=False)
            user_info.set_thumbnail(url=photo_url)
            user_info.set_image(url=cashtag_qr_image_url)
            user_info.set_footer(text= "Invoice ID: " + random_invoice_id)
 
            create_txt_invoice(random_invoice_id, random_note, current_time, cashtag, int_amount, photo_url, cashtag_qr_image_url)

            reply = await ctx.reply(content="", embed = user_info, mention_author=False)

            await reply.add_reaction("🔄")
            await reply.add_reaction("🗑️")
            await reply.add_reaction("❌")

            def check_reply(reaction, user):
                return user == ctx.message.author 

            try:
                try:
                    reaction, user = await bot.wait_for("reaction_add", check=check_reply)
                except asyncio.TimeoutError:
                    await reply.delete()
                else:

                    if str(reaction.emoji) == "🗑️":

                        await reply.delete()

                        try:
                            os.remove("invoices/"+str(random_invoice_id)+".txt") 
                            reply = await ctx.reply(content="",embed=deleted_invoice, mention_author=False)
                            sleep(5.0)
                            await reply.delete()
                            await ctx.message.delete()
                        except:
                            reply = await ctx.reply(content="",embed=generic_error_message, mention_author=False)
                            print("gerr_8")
                            sleep(5.0)
                            await reply.delete()
                            await ctx.message.delete()

                    if str(reaction.emoji) == "❌":
                        await reply.delete()
                        message_delete_desc = "This message has been deleted. \n\nInvoice #" + random_invoice_id + "still exists and you can view/refresh the status by using: \n`$manage " + random_invoice_id + "`"
                        message_delete  = discord.Embed(title="Message Deleted", description=message_delete_desc, color=0x00d632)
                        message_delete.set_footer(text= "Invoice ID: " + random_invoice_id)

                        reply = await ctx.reply(content="",embed=message_delete, mention_author=False)
                        await reply.add_reaction("✅")
                        try:
                            reaction, user = await bot.wait_for("reaction_add", check=check_reply)
                        except asyncio.TimeoutError:
                            await reply.delete()
                        else:
                            if str(reaction.emoji) == "✅":
                                await reply.delete()
                                await ctx.message.delete()           
                    
                    if str(reaction.emoji) == "🔄":

                        try:
                            with open("credentials/"+str(ctx.message.author.id)+".txt", mode = "r") as userfile:
                                cookie = userfile.read()
                                updated_cash_status = update_cash_status(cookie, int_amount, random_note)

                                if updated_cash_status == "TRANSACTION CONFIRMED":
                                    await reply.delete()
                                    # move invoice to completed invoices folder

                                    try:
                                        os.rename("invoices/"+str(random_invoice_id), "completed_invoices/"+str(random_invoice_id))
                                    except:
                                        reply = await ctx.reply(content="",embed=generic_error_message, mention_author=False)
                                        print("generr_9")
                                        sleep(3.0)
                                        await reply.delete()
                                        
                                    transaction_confirmed  = discord.Embed(title="Transaction Confirmed", description='''This invoice has been fulfilled.''', color=0x00d632)
                                    transaction_confirmed.set_footer(text= "Invoice ID: " + random_invoice_id)
                                    reply = await ctx.reply(content="",embed=transaction_confirmed, mention_author=False)
                                    await reply.add_reaction("✅")

                                    try:
                                        reaction, user = await bot.wait_for("reaction_add", check=check_reply)
                                    except asyncio.TimeoutError:
                                        await reply.delete()
                                    else:
                                        if str(reaction.emoji) == "✅":
                                            await reply.delete()
                                            await ctx.message.delete()

                                if updated_cash_status == "TRANSACTION UNCONFIRMED":
                                    await reply.delete()
                                    transaction_unconfirmed  = discord.Embed(title="Transaction Unconfirmed", description='''This invoice has yet to be fulfilled.''', color=0x00d632)
                                    transaction_unconfirmed.set_footer(text= "Invoice ID: " + random_invoice_id)
                                    
                                    reply = await ctx.reply(content="",embed=transaction_unconfirmed, mention_author=False)
                                    sleep(3.0)
                                    await reply.delete()

                                else:
                                    await reply.delete()
                                    reply = await ctx.reply(content="",embed=generic_error_message, mention_author=False)
                                    print("gerr_10")
                                    sleep(5.0)
                                    await reply.delete()

                        except:
                            await reply.delete()
                            reply = await ctx.reply(content="",embed=generic_error_message, mention_author=False)
                            print("gerr_11")
                            sleep(5.0)
                            await reply.delete()
                            await ctx.message.delete()
            
            except:
                reply = await ctx.reply(content="",embed=generic_error_message, mention_author=False)
                print("gerr_12")
                sleep(5.0)
                await reply.delete()

        except:
            try:
                os.remove("invoices/"+str(random_invoice_id)+".txt") 
            except:
                pass
 
            reply = await ctx.reply(content="", embed=generic_error_message, mention_author=False)
            print("generr_13")
            sleep(5.0)
            await reply.delete()
            await ctx.message.delete()

# refresh/view invoice ; fix invoice popup with new parse of variables
@bot.command()
async def manage(ctx):
    sender_message = ctx.message

    try:
        objects = sender_message.content.split(" ")
        random_invoice_id = objects[1]
    except:
        reply = await ctx.reply(content="",embed=invalid_input, mention_author=False)
        sleep(5.0)
        await reply.delete()
        await ctx.message.delete()

    try:
        with open("invoices/"+str(random_invoice_id)+".txt", mode = "r") as invoicefile:
            invoice_txt_data = invoicefile.read()
            int_amount = find_between(invoice_txt_data, "AMOUNT[", "]" )
            random_note = find_between(invoice_txt_data, "NOTE[", "]" )
            photo_url = find_between(invoice_txt_data, "PURL[", "]" )
            cashtag_qr_image_url = find_between(invoice_txt_data, "CT_IMAGE[", "]" )
            cashtag = find_between(invoice_txt_data, "CT[", "]" )

    except:
        reply = await ctx.reply(content="",embed=invoice_doesnt_exist, mention_author=False)
        sleep(5.0)
        await reply.delete()
        await ctx.message.delete()

    # code to update transaction status. do this after user reacts with refresh emoji
    def check_reply(reaction, user):
        return user == ctx.message.author 

    try:
        with open("credentials/"+str(ctx.message.author.id)+".txt", mode = "r") as userfile:

            cookie = userfile.read()
            updated_cash_status = update_cash_status(cookie, int_amount, random_note)


            if updated_cash_status == "TRANSACTION CONFIRMED":
                await reply.delete()
                # move invoice to completed invoices folde

                try:
                    os.rename("invoices/"+str(random_invoice_id), "completed_invoices/"+str(random_invoice_id))
                except:
                    reply = await ctx.reply(content="",embed=generic_error_message, mention_author=False)
                    print("gerr_14")
                    sleep(5.0)
                    await reply.delete()
                    
                transaction_confirmed  = discord.Embed(title="Transaction Confirmed", description='''This invoice has been fulfilled.''', color=0x00d632)
                transaction_confirmed.set_footer(text= "Invoice ID: " + random_invoice_id)
                reply = await ctx.reply(content="",embed=transaction_confirmed, mention_author=False)
                await reply.add_reaction("✅")

                try:
                    reaction, user = await bot.wait_for("reaction_add", check=check_reply)
                except asyncio.TimeoutError:
                    await reply.delete()
                else:
                    if str(reaction.emoji) == "✅":
                        await reply.delete()
                        await ctx.message.delete()

            if updated_cash_status == "TRANSACTION UNCONFIRMED":
                
                try:
                    transaction_unconfirmed  = discord.Embed(title="Transaction Unconfirmed", description='''This invoice has yet to be fulfilled.''', color=0x00d632)
                    transaction_unconfirmed.set_footer(text= "Invoice ID: " + random_invoice_id)
                    reply = await ctx.reply(content="",embed=transaction_unconfirmed, mention_author=False)
                    sleep(5)
                    await reply.delete()

                except:
                    print("err_unable to send/delete")

                try:
                    user_info = discord.Embed(title="Invoice Info", description="", color=0x00d632)
                    payment_details_message = "Cashtag: `" + cashtag + "`\nAmount: `$" + int_amount + "`\n\n**Note:  " + random_note + "**\n*You MUST put this code in the notes section when paying*\n\n`🔄 to refresh the status`\n`🗑️ to delete this invoice`\n`❌ to remove this message`"
                    user_info.add_field(name="Payment Details", value=payment_details_message, inline=False)
                    user_info.set_thumbnail(url=photo_url)
                    user_info.set_image(url=cashtag_qr_image_url)
                    user_info.set_footer(text= "Invoice ID: " + random_invoice_id)

                    reply = await ctx.reply(content="", embed = user_info, mention_author=False)

                except:
                    print("err_unable to send/delete")
                
                try:
                    await reply.add_reaction("🔄")
                    await reply.add_reaction("🗑️")
                    await reply.add_reaction("❌")
                except:
                    print("err_unable to add reactions")

                def check_reply(reaction, user):
                    return user == ctx.message.author 

                try:
                    try:
                        reaction, user = await bot.wait_for("reaction_add", check=check_reply)
                    except asyncio.TimeoutError:
                        await reply.delete()
                    else:

                        if str(reaction.emoji) == "🗑️":

                            await reply.delete()

                            try:
                                os.remove("invoices/"+str(random_invoice_id)+".txt") 
                                reply = await ctx.reply(content="",embed=deleted_invoice, mention_author=False)
                                sleep(5.0)
                                await reply.delete()
                                await ctx.message.delete()
                            except:
                                reply = await ctx.reply(content="",embed=generic_error_message, mention_author=False)
                                print("gerr_15")
                                sleep(5.0)
                                await reply.delete()
                                await ctx.message.delete()

                        if str(reaction.emoji) == "❌":
                            await reply.delete()
                            message_delete_desc = "This message has been deleted. \n\nInvoice #" + random_invoice_id + "still exists and you can view/refresh the status by using: \n`$manage " + random_invoice_id + "`"
                            message_delete  = discord.Embed(title="Message Deleted", description=message_delete_desc, color=0x00d632)
                            message_delete.set_footer(text= "Invoice ID: " + random_invoice_id)

                            reply = await ctx.reply(content="",embed=message_delete, mention_author=False)
                            await reply.add_reaction("✅")
                            try:
                                reaction, user = await bot.wait_for("reaction_add", check=check_reply)
                            except asyncio.TimeoutError:
                                await reply.delete()
                            else:
                                if str(reaction.emoji) == "✅":
                                    await reply.delete()
                                    await ctx.message.delete()           
                        
                        if str(reaction.emoji) == "🔄":

                            try:
                                with open("credentials/"+str(ctx.message.author.id)+".txt", mode = "r") as userfile:
                                    cookie = userfile.read()
                                    updated_cash_status = update_cash_status(cookie, int_amount, random_note)

                                    if updated_cash_status == "TRANSACTION CONFIRMED":
                                        await reply.delete()
                                        # move invoice to completed invoices folder

                                        try:
                                            os.rename("invoices/"+str(random_invoice_id), "completed_invoices/"+str(random_invoice_id))
                                        except:
                                            reply = await ctx.reply(content="",embed=generic_error_message, mention_author=False)
                                            print("generr_16")
                                            sleep(3.0)
                                            await reply.delete()
                                            
                                        transaction_confirmed  = discord.Embed(title="Transaction Confirmed", description='''This invoice has been fulfilled.''', color=0x00d632)
                                        transaction_confirmed.set_footer(text= "Invoice ID: " + random_invoice_id)
                                        reply = await ctx.reply(content="",embed=transaction_confirmed, mention_author=False)
                                        await reply.add_reaction("✅")

                                        try:
                                            reaction, user = await bot.wait_for("reaction_add", check=check_reply)
                                        except asyncio.TimeoutError:
                                            await reply.delete()
                                        else:
                                            if str(reaction.emoji) == "✅":
                                                await reply.delete()
                                                await ctx.message.delete()

                                    if updated_cash_status == "TRANSACTION UNCONFIRMED":
                                        await reply.delete()
                                        transaction_unconfirmed  = discord.Embed(title="Transaction Unconfirmed", description='''This invoice has yet to be fulfilled.''', color=0x00d632)
                                        transaction_unconfirmed.set_footer(text= "Invoice ID: " + random_invoice_id)
                                        
                                        reply = await ctx.reply(content="",embed=transaction_unconfirmed, mention_author=False)
                                        sleep(3.0)
                                        await reply.delete()

                                    else:
                                        await reply.delete()
                                        reply = await ctx.reply(content="",embed=generic_error_message, mention_author=False)
                                        print("gerr_17")
                                        sleep(5.0)
                                        await reply.delete()

                            except:
                                await reply.delete()
                                reply = await ctx.reply(content="",embed=generic_error_message, mention_author=False)
                                print("gerr_18")
                                sleep(5.0)
                                await reply.delete()
                                await ctx.message.delete()
                
                except:
                    reply = await ctx.reply(content="",embed=generic_error_message, mention_author=False)
                    print("gerr_19")
                    sleep(5.0)
                    await reply.delete()


    except:
        reply = await ctx.reply(content="",embed=generic_error_message, mention_author=False)
        print("gerr_20")
        sleep(5.0)
        await reply.delete()
        await ctx.message.delete()

bot.run(token)

