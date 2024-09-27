
import os
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer

LOG_FILE_PATH = 'logfile.log'
MAX_LINES = 10

class LogConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        last_lines = await self.get_last_n_lines(MAX_LINES)
        await self.send(last_lines)
        self.monitor_task = asyncio.create_task(self.monitor_log_file())

    async def disconnect(self, close_code):
        if hasattr(self, 'monitor_task'):
            self.monitor_task.cancel()

    async def monitor_log_file(self):
        last_position = os.path.getsize(LOG_FILE_PATH)
        while True:
            current_size = os.path.getsize(LOG_FILE_PATH)

            if current_size != last_position:
                last_lines = await self.get_last_n_lines(MAX_LINES)
                await self.send(last_lines)
                last_position = current_size

            await asyncio.sleep(0.1)

    async def get_last_n_lines(self, n):
        with open(LOG_FILE_PATH, 'r') as log_file:
            lines = log_file.readlines()
        if len(lines) < n:
            return ''.join(lines)
        return ''.join(lines[-n:])
