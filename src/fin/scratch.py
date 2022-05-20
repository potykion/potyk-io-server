import datetime as dt
import dataclasses
from typing import List, Any

from src.fin.cases import SplitDepositByRatio, FinGoalProgress, SplitDepositByRatioWithTodayMonthFirst, SplitParams
from src.fin.data import deposit, goals, deposit_days, cur_date





if __name__ == '__main__':
    params = SplitParams(deposit, deposit_days, goals, cur_date)
    SplitDepositByRatio.run_until_complete(params)
    print()
    SplitDepositByRatioWithTodayMonthFirst.run_until_complete(params)
    print()
