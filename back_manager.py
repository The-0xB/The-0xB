# backup_manager.py
import json
import discord

class BackupManager:
    def __init__(self, bot, backup_file='data/backup_data.json'):
        self.bot = bot
        self.backup_file = backup_file

    async def create_backup(self, guild: discord.Guild):
        backup_data = {
            "channels": [],
            "roles": []
        }

        # Backup roles
        for role in guild.roles:
            if role.is_default():
                continue  # Skip @everyone role
            backup_data["roles"].append({
                "name": role.name,
                "permissions": role.permissions.value,
                "color": role.color.value,
                "hoist": role.hoist,
                "mentionable": role.mentionable,
                "position": role.position
            })

        # Backup channels
        for channel in guild.channels:
            channel_data = {
                "name": channel.name,
                "type": str(channel.type),
                "position": channel.position,
                "category": channel.category.name if channel.category else None,
                "overwrites": {}
            }
            # Save permission overwrites
            for target, overwrite in channel.overwrites.items():
                channel_data["overwrites"][str(target.id)] = {
                    "allow": overwrite.pair()[0].value,
                    "deny": overwrite.pair()[1].value,
                    "type": "role" if isinstance(target, discord.Role) else "member"
                }
            backup_data["channels"].append(channel_data)

        # Save to file
        with open(self.backup_file, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, ensure_ascii=False, indent=4)

    async def restore_backup(self, guild: discord.Guild):
        with open(self.backup_file, 'r', encoding='utf-8') as f:
            backup_data = json.load(f)

        # Delete existing channels and roles except @everyone
        for channel in guild.channels:
            await channel.delete()
        for role in guild.roles:
            if not role.is_default():
                await role.delete()

        # Recreate roles
        roles = []
        for role_data in backup_data["roles"]:
            role = await guild.create_role(
                name=role_data["name"],
                permissions=discord.Permissions(role_data["permissions"]),
                color=discord.Color(role_data["color"]),
                hoist=role_data["hoist"],
                mentionable=role_data["mentionable"]
            )
            roles.append(role)

        # Recreate channels
        categories = {}
        for channel_data in backup_data["channels"]:
            if channel_data["type"] == "ChannelType.category":
                category = await guild.create_category(channel_data["name"], position=channel_data["position"])
                categories[channel_data["name"]] = category

        for channel_data in backup_data["channels"]:
            if channel_data["type"] != "ChannelType.category":
                category = categories.get(channel_data["category"])
                if channel_data["type"] == "ChannelType.text":
                    channel = await guild.create_text_channel(channel_data["name"], category=category, position=channel_data["position"])
                elif channel_data["type"] == "ChannelType.voice":
                    channel = await guild.create_voice_channel(channel_data["name"], category=category, position=channel_data["position"])
                else:
                    continue

                # Set permission overwrites
                overwrites = {}
                for target_id, overwrite_data in channel_data["overwrites"].items():
                    target = guild.get_role(int(target_id)) if overwrite_data["type"] == "role" else guild.get_member(int(target_id))
                    if target:
                        overwrites[target] = discord.PermissionOverwrite(
                            allow=discord.Permissions(overwrite_data["allow"]),
                            deny=discord.Permissions(overwrite_data["deny"])
                        )
                await channel.edit(overwrites=overwrites)

