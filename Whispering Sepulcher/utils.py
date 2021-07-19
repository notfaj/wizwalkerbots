import asyncio
from wizwalker import XYZ
from wizwalker.constants import Keycode
from wizwalker.extensions.wizsprinter.sprinty_client import MemoryReadError

darkmoor_exit = XYZ(x=1.3152320384979248, y=-3449.333740234375, z=0.5194091796875)
potion_ui_buy = [
    "fillallpotions",
    "buyAction",
    "btnShopPotions",
    "centerButton",
    "fillonepotion",
    "buyAction",
    "exit"
]

async def logout_and_in(client):
    await client.send_key(Keycode.ESC, 0.1)
    await asyncio.sleep(0.25)
    await client.mouse_handler.click_window_with_name('QuitButton')
    await asyncio.sleep(0.25)
    if await client.root_window.get_windows_with_name('centerButton'):
        await asyncio.sleep(0.4)
        await client.mouse_handler.click_window_with_name('centerButton')
    await asyncio.sleep(6)
    await client.mouse_handler.click_window_with_name('btnPlay')
    await client.wait_for_zone_change()
    

    
async def exit_out(client):
    await client.teleport(darkmoor_exit)
    await client.send_key(Keycode.W, 0.2)
    await asyncio.sleep(0.5)
    if await client.root_window.get_windows_with_name('centerButton'):
        await asyncio.sleep(1)
        await client.mouse_handler.click_window_with_name('centerButton')
        
async def go_through_dialog(client):
    while not await client.is_in_dialog():
        await asyncio.sleep(0.1)
    while await client.is_in_dialog():
        await client.send_key(Keycode.SPACEBAR, 0.1)



async def auto_buy_potions(client):
    # Head to home world gate
    await asyncio.sleep(1)
    await client.send_key(Keycode.HOME, 0.1)
    await client.wait_for_zone_change()
    while not await client.is_in_npc_range():
        await client.send_key(Keycode.S, 0.1)
    await client.send_key(Keycode.X, 0.1)
    await asyncio.sleep(1.2)
    # Go to Wizard City
    await client.mouse_handler.click_window_with_name('wbtnWizardCity')
    await asyncio.sleep(0.15)
    await client.mouse_handler.click_window_with_name('teleportButton')
    await client.wait_for_zone_change()
    # Walk to potion vendor
    await client.goto(-0.5264079570770264, -3021.25244140625)
    await client.send_key(Keycode.W, 0.5)
    await client.wait_for_zone_change()
    await client.goto(11.836355209350586, -1816.455078125)
    await client.send_key(Keycode.W, 0.5)
    await client.wait_for_zone_change()
    await client.goto(-880.2447509765625, 747.2051391601562)
    await client.goto(-4272.06884765625, 1251.950927734375)
    await asyncio.sleep(.4)
    if not await client.is_in_npc_range():
        await client.teleport(-4442.06005859375, 1001.5532836914062)
    await client.send_key(Keycode.X, 0.1)
    await asyncio.sleep(0.2)
    # Buy potions
    for i in potion_ui_buy:
        await client.mouse_handler.click_window_with_name(i)
        await asyncio.sleep(0.1)
    # Return
    await asyncio.sleep(.4)
    await client.mouse_handler.click_window_with_name('ResumeInstanceButton')
    await client.wait_for_zone_change()
    


async def safe_tp_to_mana(client):
  try:
    await client.tp_to_closest_mana_wisp()
  except MemoryReadError:
    await safe_tp_to_mana(client)
async def safe_tp_to_health(client):
  try:
    await client.tp_to_closest_health_wisp()
  except MemoryReadError:
    await safe_tp_to_health(client)


async def actually_collecting_wisps(client):
    while await client.stats.current_hitpoints() < await client.stats.max_hitpoints():
        await safe_tp_to_health(client)
        await asyncio.sleep(0.4)

async def check_death(client):
    #Checks if your in wizard city
    zone = await client.zone_name()
    if zone == "WizardCity/WC_Hub":
        print("You have died")
        return True

async def death_true(client):
        # Walk to potion vendor
        await client.goto(-880.2447509765625, 747.2051391601562)
        await client.goto(-4272.06884765625, 1251.950927734375)
        await asyncio.sleep(0.8)
        if not await client.is_in_npc_range():
            await client.teleport(-4442.06005859375, 1001.5532836914062)
        # Buy potions
        await client.send_key(Keycode.X, 0.1)
        await asyncio.sleep(1)
        for i in potion_ui_buy:
            await client.mouse_handler.click_window_with_name(i)
            await asyncio.sleep(0.1)
        #Dungeon recall
        await client.mouse_handler.click_window_with_name('ResumeInstanceButton')
        await client.wait_for_zone_change()



async def collect_wisps(client):
    # Head to home world gate
    await client.send_key(Keycode.HOME, 0.1)
    await client.wait_for_zone_change()
    while not await client.is_in_npc_range():
        await client.send_key(Keycode.S, 0.1)
    await client.send_key(Keycode.X, 0.1)
    await asyncio.sleep(0.5)
    # Go to Mirage
    for i in range(3):
        await client.mouse_handler.click_window_with_name('rightButton')
    await asyncio.sleep(0.1)
    await client.mouse_handler.click_window_with_name('wbtnMirage')
    await asyncio.sleep(0.1)
    await client.mouse_handler.click_window_with_name('teleportButton')
    await client.wait_for_zone_change()
    # Collecting wisps
    while await client.stats.current_hitpoints() < await client.stats.max_hitpoints():
        await safe_tp_to_health(client)
        await asyncio.sleep(0.4)
    while await client.stats.current_mana() < await client.stats.max_mana():
        await safe_tp_to_mana(client)
        await asyncio.sleep(0.4)
    # Return
    await client.mouse_handler.click_window_with_name('ResumeInstanceButton')
    await client.wait_for_zone_change()
    

async def decide_heal(client):
    if await client.needs_potion(health_percent=65, mana_percent=25) and not await client.has_potion():
        print(f'[{client.title}] Needs potion, checking gold count')
        if await client.stats.current_gold() >= 25000: 
            print(f"[{client.title}] Enough gold, buying potions")
            await auto_buy_potions(client)
        else:
            print(f"[{client.title}] Low gold, collecting wisps")
            await collect_wisps(client)
