import asyncio
from time import time
from wizwalker import XYZ
from wizwalker.constants import Keycode
from wizwalker.extensions.wizsprinter import SprintyCombat, CombatConfigProvider, WizSprinter
from utils import decide_heal

async def main(sprinter):
# majority of this code is tangents
#flowerboy was here to fix potions :3
    
    # Register clients
    sprinter.get_new_clients()
    clients = sprinter.get_ordered_clients()
    p1, p2, p3 = [*clients, None, None, None][:3]
    for i, p in enumerate(clients, 1):
        p.title = "p" + str(i)

    # Hook activation
    for p in clients: 
        print(f"[{p.title}] Activating Hooks")
        await p.activate_hooks()
        await p.mouse_handler.activate_mouseless()
        await p.send_key(Keycode.PAGE_DOWN, 0.1)

    Total_Count = 0
    total = time()
    while True:
        start = time()

        await p1.tp_to_closest_mob()
        await asyncio.sleep(0.4)
        p1pos = await p1.body.position()
        await p2.teleport(p1pos)
        await p2.send_key(Keycode.W, 0.1)
        await asyncio.sleep(0.3)

        combat_handlers = []
        print("Initiating combat")
        combat_handlers.append(SprintyCombat(p1, CombatConfigProvider('bane_configs/p1spellconfig.txt', cast_time=1)))
        combat_handlers.append(SprintyCombat(p2, CombatConfigProvider('bane_configs/p2spellconfig.txt', cast_time=1)))
        await asyncio.gather(*[h.wait_for_combat() for h in combat_handlers]) 
        print("Combat ended")

        await asyncio.sleep(1)
        await p1.send_key(Keycode.A, 0.1)
        await p2.send_key(Keycode.A, 0.1)
        await asyncio.sleep(1)

        for p in clients:
            await p.send_key(Keycode.SPACEBAR, 0.1)
            await asyncio.sleep(1)
          
        await p3.goto(-2650.177978515625, 71.61460876464844)
        await asyncio.sleep(3)
        await p3.goto(3050.296630859375, 17.513824462890625)
        await asyncio.sleep(3)

        for p in clients:
          await p.use_potion_if_needed(health_percent=10, mana_percent=10)
          await asyncio.sleep(1)
        await asyncio.gather(*[decide_heal(p) for p in clients])
        await asyncio.sleep(3.5)

        Total_Count += 1
        print("The Total Amount of Runs: ", Total_Count)
        print("Time Taken for run: ", round((time() - start) / 60, 2), "minutes")
        print("Total time elapsed: ", round((time() - total) / 60, 2), "minutes")
        print("Average time per run: ", round(((time() - total) / 60) / Total_Count, 2), "minutes")



async def run():
  sprinter = WizSprinter()

  try:
    await main(sprinter)
  except:
    import traceback

    traceback.print_exc()

  await sprinter.close()


# Start
if __name__ == "__main__":
    asyncio.run(run())
