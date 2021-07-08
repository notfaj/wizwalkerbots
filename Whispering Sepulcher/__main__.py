import asyncio
from time import time
from wizwalker import XYZ
from wizwalker.constants import Keycode
from wizwalker.extensions.wizsprinter import SprintyCombat, CombatConfigProvider, WizSprinter

from utils import decide_heal, logout_and_in, go_through_dialog , check_death, death_true

# Dungeon
L_Whispering1 = XYZ(x=-43.25860595703125, y=1592.595947265625, z=58.073028564453125)
L_Whispering5 = XYZ(x=3692.925048828125, y=10892.2333984375, z=330.5667419433594)
L_Whispering10 = XYZ(x=-5377.4970703125, y=9799.5234375, z=-220.61044311523438)

async def main(sprinter):
    # Register clients
    sprinter.get_new_clients()
    clients = sprinter.get_ordered_clients()
    p1, p2, p3, p4 = [*clients, None, None, None, None][:4]
    for i, p in enumerate(clients, 1):
        p.title = "p" + str(i)

    # Hook activation
    for p in clients: 
        print(f"[{p.title}] Activating Hooks")
        await p.activate_hooks()
        await p.mouse_handler.activate_mouseless()
        await p.send_key(Keycode.PAGE_DOWN, 0.1)

    combat_handlers = []
    Total_Count = 0
    total = time()
    while True:
        start = time()
        combat_handlers = []
        # Entering Dungeon
        await asyncio.gather(*[p.send_key(Keycode.X, 0.1) for p in clients])
        await asyncio.sleep(11)
        await asyncio.gather(*[p.wait_for_zone_change() for p in clients])
        await asyncio.sleep(1)
        await asyncio.gather(*[p.teleport(L_Whispering1) for p in clients]) # teleports to talk to
        await asyncio.gather(*[p.send_key(Keycode.W, 3) for p in clients])
        await asyncio.gather(*[go_through_dialog(p) for p in clients])

        # Teleporting to Battle 
        await p1.tp_to_closest_mob()
        await p1.send_key(Keycode.W, 0.1)
        await asyncio.sleep(0.4)
        for p in clients[1:]:
            p1pos = await p1.body.position()
            await p.teleport(p1pos)
            await p.send_key(Keycode.W, 0.1)
            await asyncio.sleep(0.2)
        await asyncio.sleep(1)

        # Battle:
        print("Initiating 1st mob battle")
        for p in clients: # Setting up the parsed configs to combat_handlers
            combat_handlers.append(SprintyCombat(p, CombatConfigProvider(f'configs/{p.title}spellconfig.txt', cast_time=1))) #UniversalWanderingBot/
        await asyncio.gather(*[h.wait_for_combat() for h in combat_handlers]) # .wait_for_combat() to wait for combat to then go through the battles
        print("Combat ended")
        
        #check death mob
        if await check_death(p1) == True:
            await asyncio.gather(*[death_true(p) for p in clients])
            await asyncio.sleep(0.4)
            await p1.tp_to_closest_mob()
            await p1.send_key(Keycode.W, 0.1)
            await asyncio.sleep(0.4)
            #redo's battle
            for p in clients[1:]:
                p1pos = await p1.body.position()
                await p.teleport(p1pos)
                await p.send_key(Keycode.W, 0.1)
                await asyncio.sleep(0.2)
            for p in clients: # Setting up the parsed configs to combat_handlers
                    combat_handlers.append(SprintyCombat(p, CombatConfigProvider(f'configs/{p.title}spellconfig.txt', cast_time=1))) #UniversalWanderingBot/
            await asyncio.gather(*[h.wait_for_combat() for h in combat_handlers]) # .wait_for_combat() to wait for combat to then go through the battles
            print("Combat ended")
            
        # Health check
        await asyncio.gather(*[p.use_potion_if_needed(health_percent=65, mana_percent=5) for p in clients])

        
        # Teleporting to Battle
        await asyncio.gather(*[go_through_dialog(p) for p in clients]) # Finishes talking at end of 1st battle
        await asyncio.gather(*[p.teleport(L_Whispering5) for p in clients]) # teleports to talk to
        await asyncio.gather(*[go_through_dialog(p) for p in clients])
        await asyncio.sleep(4)
        await p1.tp_to_closest_mob()
        await p1.send_key(Keycode.W, 0.1)
        await asyncio.sleep(1)
        await p1.send_key(Keycode.S, 0.3)
        for p in clients[1:]:
            p1pos = await p1.body.position()
            await p.teleport(p1pos)
            await p.send_key(Keycode.W, 0.1)
            await asyncio.sleep(0.2)
        await asyncio.sleep(2)

        # Battle:
        combat_handlers = []
        print("Initiating 2nd mob battle")
        for p in clients: # Setting up the parsed configs to combat_handlers
            combat_handlers.append(SprintyCombat(p, CombatConfigProvider(f'configs/{p.title}spellconfig.txt', cast_time=1))) #UniversalWanderingBot/
        await asyncio.gather(*[h.wait_for_combat() for h in combat_handlers]) # .wait_for_combat() to wait for combat to then go through the battles
        print("Combat ended")


        #check death mob
        if await check_death(p1) == True:
            await asyncio.gather(*[death_true(p) for p in clients])
            await asyncio.sleep(0.4)
            await p1.tp_to_closest_mob()
            await p1.send_key(Keycode.W, 0.1)
            await asyncio.sleep(0.4)
            for p in clients[1:]:
                p1pos = await p1.body.position()
                await p.teleport(p1pos)
                await p.send_key(Keycode.W, 0.1)
                await asyncio.sleep(0.2)
            #redo's battle
            for p in clients: # Setting up the parsed configs to combat_handlers
                    combat_handlers.append(SprintyCombat(p, CombatConfigProvider(f'configs/{p.title}spellconfig.txt', cast_time=1))) #UniversalWanderingBot/
            await asyncio.gather(*[h.wait_for_combat() for h in combat_handlers]) # .wait_for_combat() to wait for combat to then go through the battles
            print("Combat ended")


        # Health check
        await asyncio.gather(*[p.use_potion_if_needed(health_percent=65, mana_percent=5) for p in clients])

        # Teleporting to Battle
        await asyncio.gather(*[p.teleport(L_Whispering10) for p in clients]) # teleports to talk to
        await asyncio.gather(*[go_through_dialog(p) for p in clients])
        await p1.tp_to_closest_mob()
        await p1.send_key(Keycode.W, 0.1)
        await asyncio.sleep(4)
        await p1.send_key(Keycode.S, 0.2)
        await asyncio.sleep(0.4)
        for p in clients[1:]:
            p1pos = await p1.body.position()
            await p.teleport(p1pos)
            await p.send_key(Keycode.W, 0.1)
            await asyncio.sleep(0.2)
        await asyncio.sleep(1)

        # Battle:
        combat_handlers = []
        print("Initiating boss battle")
        for p in clients: # Setting up the parsed configs to combat_handlers
            combat_handlers.append(SprintyCombat(p, CombatConfigProvider(f'configs/{p.title}bossspellconfig.txt', cast_time=1.5))) #UniversalWanderingBot/
        await asyncio.gather(*[h.wait_for_combat() for h in combat_handlers]) # .wait_for_combat() to wait for combat to then go through the battles
        print("Combat ended")



        #check death mob
        if await check_death(p1) == True:
            await asyncio.gather(*[death_true(p) for p in clients])
            await asyncio.sleep(0.4)
            await p1.tp_to_closest_mob()
            await p1.send_key(Keycode.W, 0.1)
            await asyncio.sleep(0.4)
            for p in clients[1:]:
                p1pos = await p1.body.position()
                await p.teleport(p1pos)
                await p.send_key(Keycode.W, 0.1)
                await asyncio.sleep(0.2)
            #redo's battle
            for p in clients: # Setting up the parsed configs to combat_handlers
                    combat_handlers.append(SprintyCombat(p, CombatConfigProvider(f'configs/{p.title}bossspellconfig.txt', cast_time=1))) #UniversalWanderingBot/
            await asyncio.gather(*[h.wait_for_combat() for h in combat_handlers]) # .wait_for_combat() to wait for combat to then go through the battles
            print("Combat ended")






        # Reseting
        await asyncio.sleep(1)
        await asyncio.gather(*[logout_and_in(p) for p in clients])
        
        # Healing
        await asyncio.sleep(2)
        await asyncio.gather(*[p.use_potion_if_needed(health_percent=65, mana_percent=5) for p in clients])
        await asyncio.gather(*[decide_heal(p) for p in clients])
        await asyncio.sleep(3.5)

        # Time
        Total_Count += 1
        print("The Total Amount of Runs: ", Total_Count)
        print("Time Taken for run: ", round((time() - start) / 60, 2), "minutes")
        print("Total time elapsed: ", round((time() - total) / 60, 2), "minutes")
        print("Average time per run: ", round(((time() - total) / 60) / Total_Count, 2), "minutes")



# Error Handling
async def run():
  sprinter = WizSprinter() # Define thingys

  try:
    await main(sprinter)
  except:
    import traceback

    traceback.print_exc()

  await sprinter.close()


# Start
if __name__ == "__main__":
    asyncio.run(run())
