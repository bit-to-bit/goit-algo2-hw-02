from typing import List, Dict


def rod_cutting_memo(length: int, prices: List[int]) -> Dict:
    """
    Знаходить оптимальний спосіб розрізання через мемоізацію

    Args:
        length: довжина стрижня
        prices: список цін, де prices[i] — ціна стрижня довжини i+1

    Returns:
        Dict з максимальним прибутком та списком розрізів
    """

    memo = [{"max_profit": 0, "cuts": [], "number_of_cuts": 0}]

    for i in range(1, length + 1):

        max_profit = prices[i - 1]
        best_cuts = [i]

        for j in range(1, i):

            profit = memo[i - j].get("max_profit")
            cuts = memo[i - j].get("cuts")
            new_profit = memo[j].get("max_profit") + profit

            if new_profit > max_profit:
                max_profit = new_profit
                best_cuts = cuts + memo[j].get("cuts")

        memo.append(
            {
                "max_profit": max_profit,
                "cuts": best_cuts,
                "number_of_cuts": len(best_cuts) - 1,
            }
        )

    return memo[length]


def rod_cutting_table(length: int, prices: List[int]) -> Dict:
    """
    Знаходить оптимальний спосіб розрізання через табуляцію

    Args:
        length: довжина стрижня
        prices: список цін, де prices[i] — ціна стрижня довжини i+1

    Returns:
        Dict з максимальним прибутком та списком розрізів
    """
    dp = [0] * (length + 1)
    table = [[] for _ in range(length + 1)]

    for i in range(1, length + 1):
        max_profit = float("-inf")
        for j in range(1, i + 1):
            if j <= len(prices):
                current_profit = prices[j - 1] + dp[i - j]
                if current_profit > max_profit:
                    max_profit = current_profit
                    table[i] = table[i - j] + [j]
        dp[i] = max_profit

    return {
        "max_profit": dp[length],
        "cuts": table[length],
        "number_of_cuts": len(table[length]) - 1,
    }
