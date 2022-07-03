import sys
import asyncio

from os import chdir, path

chdir(path.dirname(path.abspath(__file__)))

from GUI.application import App
from init import command_line_options
from processor.grapher import grapher

async def main():

    if len(sys.argv) > 1:
        await grapher(options=command_line_options.on_start())
    else:
        app = App(command_line_options.default_dict())
        app.mainloop()
        await grapher(options=app.get_options())

if __name__ == '__main__':
    asyncio.run(main())
