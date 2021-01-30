import sys
sys.path.append('..')
from main import *
@tasks.loop(seconds=60)
async def loopGVW():
    for i in await listallservers():
        d = await Dados(i)
        d['gv']

