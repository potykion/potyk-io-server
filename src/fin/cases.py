import dataclasses
import datetime as dt
from abc import ABC
from dataclasses import dataclass, field
from decimal import Decimal
from itertools import repeat
from typing import List, Protocol, Dict

from src.fin.utils import split_filter

FinGoalId = int


@dataclass()
class FinGoal:
    """
    Финансовая цель, напр. 100к на отпуск до сентября
    """
    id: FinGoalId
    name: str
    price: Decimal
    deadline_date: dt.date
    weight: float = 1

    def as_progress(self, **kwargs):
        return FinGoalProgress(
            goal=self,
            **kwargs
        )


@dataclass()
class FinGoalProgress:
    goal: FinGoal
    cur_price: Decimal = Decimal(0)
    cur_date: dt.date = field(default_factory=dt.date.today)

    @property
    def price_diff(self) -> Decimal:
        return self.goal.price - self.cur_price

    @property
    def dt_diff(self) -> int:
        return (self.goal.deadline_date - self.cur_date).days or 1

    @property
    def done(self):
        return self.cur_price >= self.goal.price


@dataclass()
class SplitParams:
    deposit: Decimal
    deposit_days: int
    goals: List[FinGoalProgress]
    cur_date: dt.date


class SplitDeposit(Protocol):
    """
    Делит депозит на части

    То есть у нас есть 10 финансовых целей, и 40к которые мы вкидываем каждый месяц
    Вот эти 40к надо как-то распределить, напр. 10к на 1 цель, 20к на другую и тд
    """

    @classmethod
    def from_params(cls, params: SplitParams) -> 'SplitDeposit':
        ...

    def __call__(self) -> Dict[FinGoalId, Decimal]:
        ...

    @classmethod
    def run_until_complete(cls, params: SplitParams):
        def iteration(params: SplitParams) -> SplitParams:
            split = cls.from_params(params)()
            return dataclasses.replace(
                params,
                goals=[
                    dataclasses.replace(
                        progress,
                        cur_price=progress.cur_price + split[progress.goal.id],
                        cur_date=progress.cur_date + dt.timedelta(days=params.deposit_days),
                    )
                    for progress in params.goals
                ],
                cur_date=params.cur_date + dt.timedelta(days=params.deposit_days),
            )

        print(f'## {cls.__name__}')
        print()

        completed_goals: list[FinGoalProgress] = []
        while params.goals:
            params = iteration(params)
            completed_goals += [goal for goal in params.goals if goal.done]
            params = dataclasses.replace(params, goals=[goal for goal in params.goals if not goal.done])

        completed_goals = sorted(completed_goals, key=lambda prog: prog.goal.deadline_date)
        for progress in completed_goals:
            date_diff = (progress.goal.deadline_date - progress.cur_date).days
            print(
                f'Цель: {progress.goal.name}',
                f'Дедлайн: {progress.goal.deadline_date}',
                f'Дата погашения: {progress.cur_date}',
                f'Быстрее на {date_diff}' if date_diff > 0 else f'Просрочка на {abs(date_diff)}',
                sep=' | '
            )

        max_deadline = completed_goals[-1].goal.deadline_date
        max_cur_date = max(g.cur_date for g in completed_goals)
        date_diff = (max_deadline - max_cur_date).days

        print(
            f'Последний дедлайн: {max_deadline}',
            f'Последнее погашение: {max_cur_date}',
            f'Быстрее на {date_diff}' if date_diff > 0 else f'Просрочка на {abs(date_diff)}',
            sep=' | '
        )

        return date_diff


@dataclass()
class SplitDepositByRatio(SplitDeposit):
    deposit: Decimal
    goals: List[FinGoalProgress]

    @classmethod
    def from_params(cls, params):
        return cls(
            deposit=params.deposit,
            goals=params.goals,
        )

    def __call__(self) -> Dict[FinGoalId, Decimal]:
        def progress_weight(progress):
            return progress.price_diff / progress.dt_diff * Decimal(progress.goal.weight)

        total_weight = sum(map(progress_weight, self.goals))

        def deposit_split(progress):
            split_ = (
                round(self.deposit * progress_weight(progress) / total_weight / 1000) * 1000
            )
            split_ = min(split_, progress.price_diff)
            return split_

        return {
            progress.goal.id: deposit_split(progress)
            for progress in self.goals
        }


@dataclass()
class SplitDepositByRatioWithTodayMonthFirst(SplitDeposit):
    deposit: Decimal
    goals: List[FinGoalProgress]
    cur_date: dt.date

    @classmethod
    def from_params(cls, params):
        return cls(
            deposit=params.deposit,
            goals=params.goals,
            cur_date=params.cur_date,
        )

    def __call__(self) -> Dict[FinGoalId, Decimal]:
        split_ = {}

        today_month_goals, goals = split_filter(
            self.goals,
            lambda prog: prog.goal.deadline_date.month == self.cur_date.month
        )

        for progress in today_month_goals:
            split_[progress.goal.id] = min(progress.price_diff, self.deposit)
            self.deposit -= min(progress.price_diff, self.deposit)

        split_.update(SplitDepositByRatio(self.deposit, goals)())
        return split_
