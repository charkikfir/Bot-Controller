import discord
from discord.ext import commands

import asyncio


class MyBot(commands.Bot):
    def __init__(self, token, con):
        super().__init__(command_prefix="!", loop=asyncio.new_event_loop())
        
        self.con = con
        self.token = token
        self.loop.create_task(self.check_con())

    async def check_con(self):
        await self.wait_until_ready()
        while not self.is_closed():
            if self.con.poll():
                m = self.con.recv()
                self.dispatch("pipe_message", m)
            await asyncio.sleep(1)

    async def on_pipe_message(self, m):
        if isinstance(m, list):
            command = m[0]
            args = m[1::]
            self.dispatch(command, *args)
        else:
            self.dispatch(m)

    async def on_change_pr(self, new_pr):  # Pipe command
        try:
            await self.change_presence(activity=discord.Game(new_pr))
            self.con.send("done")
        except Exception as e:
            self.con.send("error")
            raise e

    async def on_close(self):  # Pipe command
        for task in asyncio.all_tasks(loop=self.loop):
            task.cancel()
        await self.logout()

    async def on_give_guilds(self):  # Pipe command
        self.con.send([[g.name, g.id] for g in self.guilds])
        # self.con.send(self.guilds)
    
    async def on_give_channels(self, g_id):  # Pipe command
        guild = self.get_guild(g_id)
        chns = [[chn.name, chn.id] for chn in guild.text_channels]
        self.con.send(chns)

    async def on_ready(self):
        self.con.send("ready")
        self.con.send(self.user.name)
        print("I'm ready")

    def run(self): 
        super().run(self.token)
        self.con.send("LoginFailed") # If run doesn't.. run it will get to this line. This usually happens when token is invalid 


def start_bot(token, con):
    bot = MyBot(token, con)
    bot.run()
