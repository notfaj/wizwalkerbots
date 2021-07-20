import asyncio
from time import time

from wizwalker.constants import Keycode
from wizwalker.extensions.wizsprinter import SprintyCombat, CombatConfigProvider, WizSprinter

from utils import decide_heal, logout_and_in, exit_out, go_through_dialog, actually_collecting_wisps



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

        # Initial battle starter
        await p1.tp_to_closest_mob()
        await p1.send_key(Keycode.W, 0.1)
        await asyncio.sleep(0.4)
        for p in clients[1:]:
            p1pos = await p1.body.position()
            await p.teleport(p1pos)
            await p.send_key(Keycode.W, 0.1)
            await asyncio.sleep(0.2)

        # Battle:
        print("Initiating combat")
        for p in clients: # Setting up the parsed configs to combat_handlers
            combat_handlers.append(SprintyCombat(p, CombatConfigProvider(f'configs/{p.title}spellconfig.txt', cast_time=1.5))) 
        await asyncio.gather(*[h.wait_for_combat() for h in combat_handlers]) # .wait_for_combat() to wait for combat to then go through the battles
        print("Combat ended")

        # Reseting
        await asyncio.sleep(0.4)
        await asyncio.gather(*[p.goto(12.702668190002441,1612.439208984375) for p in clients])
        await asyncio.gather(*[p.wait_for_zone_change() for p in clients])
        await asyncio.gather(*[p.send_key(Keycode.S, 3) for p in clients])
        
        
        # Healing
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
