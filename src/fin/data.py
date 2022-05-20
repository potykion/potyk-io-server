from decimal import Decimal
from typing import List

from src.fin.cases import FinGoal, FinGoalProgress
from src.fin.utils import date_from_str

cur_date = date_from_str('2022/05/15')

goals: List[FinGoalProgress] = [
    FinGoal(id=1, name='хата', price=Decimal(75_000), deadline_date=date_from_str('2022/05/31')).as_progress(cur_price=Decimal(31_000), cur_date=cur_date),
    FinGoal(id=2, name='инвестиции', price=Decimal(50_000), deadline_date=date_from_str('2022/05/31'), weight=0.5).as_progress(cur_price=Decimal(11_000), cur_date=cur_date),
    FinGoal(id=3, name='колечко', price=Decimal(45_000), deadline_date=date_from_str('2022/10/31'), weight=3).as_progress(cur_price=Decimal(18_000), cur_date=cur_date),
    FinGoal(id=4, name='новая хата', price=Decimal(170_000), deadline_date=date_from_str('2022/10/31')).as_progress(cur_price=Decimal(31_000), cur_date=cur_date),
    FinGoal(id=5, name='отпуск', price=Decimal(100_000), deadline_date=date_from_str('2022/08/31')).as_progress(cur_price=Decimal(25_800), cur_date=cur_date),
    FinGoal(id=6, name='абик', price=Decimal(90_000), deadline_date=date_from_str('2023/03/31')).as_progress(cur_price=Decimal(13_000), cur_date=cur_date),
]

deposit = Decimal(80_000)
deposit_days = 15
