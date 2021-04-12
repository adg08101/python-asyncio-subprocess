import asyncio
import multiprocessing

async def run(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    print(f'[{cmd!r} exited with {proc.returncode}]')
    if stdout:
        print(f'[stdout]\n{stdout.decode()}')
    if stderr:
        print(f'[stderr]\n{stderr.decode()}')

def call(p, c):
    for i in range(c):
        asyncio.run(run(p))

def call_defined(p):
    asyncio.run(run(p))

def get_process(p, c):
    l = [
        multiprocessing.Process(
            target=call_defined,
            args=[p]
        )
        for i in range(c)
    ]

    return l

if __name__ == '__main__':
    proc1 = multiprocessing.Process(
        target=call,
        args=['notepad', 1]
    )

    proc2 = multiprocessing.Process(
        target=call,
        args=['mspaint', 1]
    )

    l = get_process('notepad', 15)

    proc1.start()
    proc2.start()

    for p in l:
        p.start()

    for p in l:
        p.join()

    proc1.join()
    proc2.join()
