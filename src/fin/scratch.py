from src.fin.cases import SplitDepositByRatio, SplitDepositByRatioWithTodayMonthFirst, SplitParams
from src.fin.data import deposit, goals, deposit_days, cur_date


def compare_algos(params):
    print(f'# {deposit=}, {deposit_days=}')
    print()
    SplitDepositByRatio.run_until_complete(params)
    print()
    SplitDepositByRatioWithTodayMonthFirst.run_until_complete(params)
    print()


def apply_algo(algo, params):
    split = algo.from_params(params)()
    for progress in params.goals:
        print(progress.goal.name, split[progress.goal.id])


if __name__ == '__main__':
    params = SplitParams(deposit, deposit_days, goals, cur_date)

    # compare_algos(params)

    apply_algo(SplitDepositByRatio, params)
