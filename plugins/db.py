import datetime
import os
import motor.motor_asyncio

# MongoDB Database URL and Name
DB_URL = os.environ.get("DB_URL", "mongodb+srv://KarthikMovies:KarthikUK007@cluster0.4l5byki.mongodb.net/?retryWrites=true&w=majority")
DB_NAME = os.environ.get("DB_NAME", "Cluster0")

class Database:
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.users = self.db.UsersData
        self.channels = self.db.ChannelsData  # Collection for source and destination channels
        self.messages = self.db.Messages  # Collection for storing messages
        self.replacement_data = self.db.ReplacementData  # Collection for replacement logs
        self.channels_tb = self.db.ChannelsData_tb  # Collection for source and destination channels
        self.messages_tb = self.db.Messages_tb  # Collection for storing messages
        self.replacement_data_tb = self.db.ReplacementData_tb

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

    async def replace_text(self, source_channel, old_text, new_text):
        """
        Replaces specific text in messages from a source channel.
        :param source_channel: ID of the source channel
        :param old_text: Text to replace
        :param new_text: Replacement text
        :return: Count of updated messages
        """
        updated_count = 0

        # Find matching messages in the collection
        async for message_doc in self.messages.find({"source_channel": source_channel}):
            if old_text in message_doc.get("message", ""):
                # Replace the specified text in the message
                updated_message = message_doc["message"].replace(old_text, new_text)

                # Update the document in the database
                await self.messages.update_one(
                    {"_id": message_doc["_id"]},
                    {"$set": {"message": updated_message}}
                )
                updated_count += 1

        # Log the replacement operation
        replacement_data = {
            "source_channel": source_channel,
            "original_text": old_text,
            "new_text": new_text,
            "replaced_count": updated_count,
            "timestamp": datetime.datetime.now()
        }
        await self.replacement_data.insert_one(replacement_data)

        return updated_count

    # second source 
    async def add_channel_tb(self, source_channel, destination_channel):
        # Add source and destination channels to the database
        channel_data = {
            "source_channel": source_channel,
            "destination_channel": destination_channel,
            "added_on": datetime.datetime.now()
        }
        await self.channels_tb.insert_one(channel_data)

    async def get_all_channels_tb(self):
        # Retrieve all source and destination channels from the database
        channels = []
        async for channel in self.channels_tb.find():
            channels.append(channel)
        return channels

    async def delete_channel_tb(self, source_channel):
        # Delete a source and its corresponding destination channel
        result = await self.channels_tb.delete_one({"source_channel": source_channel})
        return result.deleted_count > 0

    async def replace_text_tb(self, source_channel, old_text, new_text):
        """
        Replaces specific text in messages from a source channel.
        :param source_channel: ID of the source channel
        :param old_text: Text to replace
        :param new_text: Replacement text
        :return: Count of updated messages
        """
        updated_count = 0

        # Find matching messages in the collection
        async for message_doc in self.messages_tb.find({"source_channel": source_channel}):
            if old_text in message_doc.get("message", ""):
                # Replace the specified text in the message
                updated_message = message_doc["message"].replace(old_text, new_text)

                # Update the document in the database
                await self.messages_tb.update_one(
                    {"_id": message_doc["_id"]},
                    {"$set": {"message": updated_message}}
                )
                updated_count += 1

        # Log the replacement operation
        replacement_data_tb = {
            "source_channel": source_channel,
            "original_text": old_text,
            "new_text": new_text,
            "replaced_count": updated_count,
            "timestamp": datetime.datetime.now()
        }
        await self.replacement_data_tb.insert_one(replacement_data)
        return updated_count

u_db = Database(DB_URL, DB_NAME)
