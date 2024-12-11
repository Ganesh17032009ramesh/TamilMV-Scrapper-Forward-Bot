import datetime
import os
import motor.motor_asyncio

# MongoDB Database URL and Name
DB_URL = os.environ.get("DB_URL", "mongodb+srv://KarthikMovies:KarthikUK007@cluster0.4l5byki.mongodb.net/?retryWrites=true&w=majority")
DB_NAME = os.environ.get("DB_NAME", "Cluster0")

# Initialize Database Class
class Database:
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.users = self.db.UsersData
        self.channels = self.db.ChannelsData  # Collection for source and destination channels

    async def add_channel(self, source_channel, destination_channel):
        # Add source and destination channels to the database
        channel_data = {
            "source_channel": source_channel,
            "destination_channel": destination_channel,
            "added_on": datetime.datetime.now()
        }
        await self.channels.insert_one(channel_data)

    async def get_all_channels(self):
        # Retrieve all source and destination channels from the database
        channels = []
        async for channel in self.channels.find():
            channels.append(channel)
        return channels

    async def delete_channel(self, source_channel):
        # Delete a source and its corresponding destination channel
        result = await self.channels.delete_one({"source_channel": source_channel})
        return result.deleted_count > 0

# MongoDB instance
u_db = Database(DB_URL, DB_NAME)
