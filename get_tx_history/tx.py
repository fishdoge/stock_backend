# !pip install finmind
from FinMind.data import DataLoader
# import FinMind
# print(FinMind)
api = DataLoader()
api.login_by_token(api_token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRlIjoiMjAyMy0wNy0xMiAxMTowNzo1NiIsInVzZXJfaWQiOiJ3ZXNsaXV0dyIsImlwIjoiMTIzLjI0MC4yMzIuOTMifQ.EnPZsW9V9NkQq3iZ4TtmQnu-6EwRoJ8cRF-LBrDmH0s')
# api.login(user_id='user_id',password='password')
df = api.taiwan_futures_tick(
    futures_id='MTX',
    date='2020-04-01'
)
df