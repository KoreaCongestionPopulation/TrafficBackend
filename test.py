import asyncio
import websockets


async def receive_data():
    async with websockets.connect("ws://localhost:8084/ws/avg_age_topic") as websocket:
        while True:
            data = await websocket.recv()
            print(data)


asyncio.get_event_loop().run_until_complete(receive_data())
# from fastapi import FastAPI, WebSocket
# from sqlalchemy import create_engine, MetaData, Table
# from databases import Database

# import json, asyncio
# from datetime import datetime
# from decimal import Decimal

# DATABASE_URL = "mysql+mysqlconnector://root:123456789@traffic_sql:3306/peopletraffic"
# metadata = MetaData()
# database = Database(DATABASE_URL)
# engine = create_engine(DATABASE_URL)

# # 테이블 객체 정의
# congestion_age = Table("age_congestion", metadata, autoload=True, autoload_with=engine)
# congestion_pred_age = Table(
#     "age_congestion_pred", metadata, autoload=True, autoload_with=engine
# )
# congestion_gender = Table(
#     "gender_congestion", metadata, autoload=True, autoload_with=engine
# )
# congestion_gender_pred = Table(
#     "gender_congestion_pred", metadata, autoload=True, autoload_with=engine
# )
# # WebSocket 클라이언트를 추적하기 위한 set
# active_websockets = {
#     "congestion_age": set(),
#     "congestion_pred_age": set(),
#     "congestion_gender": set(),
#     "congestion_gender_pred": set(),
# }

# app = FastAPI()


# @app.on_event("startup")
# async def startup():
#     await database.connect()


# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()


# async def fetch_table_data(table):
#     query = table.select()
#     rows = await database.fetch_all(query)
#     data = [dict(row) for row in rows]  # 각 Row 객체를 딕셔너리로 변환
#     for row in data:
#         for key, value in row.items():
#             if isinstance(value, datetime):
#                 row[key] = value.isoformat()  # datetime 객체를 문자열로 변환
#             elif isinstance(value, Decimal):
#                 row[key] = str(value)  # Decimal 객체를 문자열로 변환
#     return data


# @app.websocket("/ws/congestion_age")
# async def congestion_age_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     while True:
#         data = await fetch_table_data(congestion_age)
#         json_trasn = json.dumps(data, indent=4, ensure_ascii=False)
#         await websocket.send_text(json_trasn)
#         await asyncio.sleep(2)  # 10초 간격으로 데이터 전송


# @app.websocket("/ws/congestion_pred_age")
# async def congestion_pred_age_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     data = await fetch_table_data(congestion_pred_age)
#     json_trasn = json.dumps(data, indent=4, ensure_ascii=False)
#     await websocket.send_text(json_trasn)  # 데이터 전송


# @app.websocket("/ws/congestion_gender")
# async def congestion_gender_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     data = await fetch_table_data(congestion_gender)
#     json_trasn = json.dumps(data, indent=4, ensure_ascii=False)
#     await websocket.send_text(json_trasn)  # 데이터 전송


# @app.websocket("/ws/congestion_gender_pred")
# async def congestion_gender_pred_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     data = await fetch_table_data(congestion_gender_pred)
#     json_trasn = json.dumps(data, indent=4, ensure_ascii=False)
#     await websocket.send_text(json_trasn)  # 데이터 전송
