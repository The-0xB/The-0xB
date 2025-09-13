# lock_manager.py
import discord

class LockManager:
    def __init__(self, bot, modified_channels_file='data/modified_channels.json'):
        self.bot = bot
        self.modified_channels_file = modified_channels_file
        self.modified_channels = self._load_modified_channels()

    def _load_modified_channels(self):
        import json
        import os
        if not os.path.exists(self.modified_channels_file):
            return {}
        with open(self.modified_channels_file, 'r') as f:
            return json.load(f)

    def _save_modified_channels(self):
        import json
        with open(self.modified_channels_file, 'w') as f:
            json.dump(self.modified_channels, f, indent=4)

    async def lock_channels(self, guild: discord.Guild):
        for channel_id in self.modified_channels.get("locked", []):
            channel = guild.get_channel(int(channel_id))
            if channel:
                await channel.set_permissions(guild.default_role, send_messages=False, connect=False)

    async def unlock_channels(self, guild: discord.Guild):
        for channel_id in self.modified_channels.get("locked", []):
            channel = guild.get_channel(int(channel_id))
            if channel:
                await channel.set_permissions(guild.default_role, send_messages=True, connect=True)

    async def hide_channels(self, guild: discord.Guild):
        for channel_id in self.modified_channels.get("hidden", []):
            channel = guild.get_channel(int(channel_id))
            if channel:
                await channel.set_permissions(guild.default_role, view_channel=False)

    async def show_channels(self, guild: discord.Guild):
        for channel_id in self.modified_channels.get("hidden", []):
            channel = guild.get_channel(int(channel_id))
            if channel:
                await channel.set_permissions(guild.default_role, view_channel=True)

    def add_locked_channel(self, channel_id):
        self.modified_channels.setdefault("locked", [])
        if channel_id not in self.modified_channels["locked"]:
            self.modified_channels["locked"].append(channel_id)
            self._save_modified_channels()

    def remove_locked_channel(self, channel_id):
        if "locked" in self.modified_channels and channel_id in self.modified_channels["locked"]:
            self.modified_channels["locked"].remove(channel_id)
            self._save_modified_channels()

    def add_hidden_channel(self, channel_id):
        self.modified_channels.setdefault("hidden", [])
        if channel_id not in self.modified_channels["hidden"]:
            self.modified_channels["hidden"].append(channel_id)
            self._save_modified_channels()

    def remove_hidden_channel(self, channel_id):
        if "hidden" in self.modified_channels and channel_id in self.modified_channels["hidden"]:
            self.modified_channels["hidden"].remove(channel_id)
            self._save_modified_channels()
