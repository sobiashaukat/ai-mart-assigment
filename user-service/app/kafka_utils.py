# user-service/kafka_utils.py
import asyncio
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import json

KAFKA_BOOTSTRAP_SERVERS = "broker:19092"

producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)

async def produce_event(topic: str, event: dict):
    await producer.start()
    try:
        value = json.dumps(event).encode("utf-8")
        await producer.send_and_wait(topic, value)
    finally:
        await producer.stop()

consumer = AIOKafkaConsumer(
    "user-events",
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    group_id="user-group",
)

async def consume_events():
    await consumer.start()
    try:
        async for msg in consumer:
            print(f"Consumed message: {msg.value.decode('utf-8')}")
    finally:
        await consumer.stop()
