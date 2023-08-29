from fastapi import FastAPI, WebSocket, status, WebSocketDisconnect
from aiokafka import AIOKafkaConsumer
import asyncio
import json

app = FastAPI()

# Active WebSocket connections
connections = {}


# Initialize Kafka consumer
async def consume_kafka():
    consumer = AIOKafkaConsumer(
        "avg_age_topic",
        "avg_gender_topic",
        "avg_n_age_topic",
        "avg_n_gender_topic",
        bootstrap_servers="kafka1:19092, kafka2:29092, kafka3:39092",
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    )
    await consumer.start()
    try:
        async for msg in consumer:
            topic = msg.topic
            value = msg.value
            if topic in connections:
                for websocket in connections[topic]:
                    json_trans = json.dumps(value, indent=4, ensure_ascii=False)
                    await websocket.send_text(json_trans)
    except Exception as error:
        print(error)
    finally:
        await consumer.stop()


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(consume_kafka())


@app.on_event("shutdown")
async def shutdown_event():
    for conns in connections.values():
        for websocket in conns:
            await websocket.close()


@app.websocket("/ws/{topic}")
async def websocket_endpoint(websocket: WebSocket, topic: str):
    await websocket.accept()
    if topic not in connections:
        connections[topic] = []
    connections[topic].append(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(data)
            # You can add more logic here
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for topic: {topic}")
    finally:
        connections[topic].remove(websocket)
        await websocket.close(code=status.WS_1000_NORMAL_CLOSURE)
