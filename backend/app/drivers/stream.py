import asyncio
import redis
import redis.asyncio.client
import redis.client


from app.redis_client import _redis_client


DRIVER_WEBSOCKET_TOPIC = "driver/location/{driver_id}"


class RedisStream:

    def __init__(self, driver_id: str) -> None:
        self.driver_id = driver_id

    async def publish_driver_location_to_topic(self, data):
        topic = DRIVER_WEBSOCKET_TOPIC.format(driver_id=self.driver_id)
        await _redis_client.publish(topic, data)

    async def get_published_messages(
        self, topic: str, _redis: redis.asyncio.client.Redis
    ):
        # Create a PubSub object
        pubsub: redis.asyncio.client.PubSub = _redis.pubsub()

        # Subscribe to the topic (await since it's an async operation)
        await pubsub.subscribe(topic)

        # Process messages in an infinite loop
        try:
            while True:
                message = await pubsub.get_message(ignore_subscribe_messages=True)
                if message and message["type"] == "message":
                    yield {message["data"].decode("utf-8")}
                await asyncio.sleep(0.1)  # Small delay to prevent busy-waiting
        except asyncio.CancelledError:
            # Handle task cancellation if necessary
            print("Listener task was cancelled.")
        finally:
            # Unsubscribe and close PubSub
            await pubsub.unsubscribe(topic)
            await pubsub.close()
