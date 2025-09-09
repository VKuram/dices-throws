from collections import defaultdict
from decimal import Decimal, getcontext
from fractions import Fraction
from math import floor, log10


getcontext().prec = 10000  # Точность для Decimal


class Probability():
    def __init__(self):
        print("=== Расчёт вероятности выпадения суммы при бросках костей ===\n")
        try:
            self.dices_amount = int(input("Введите количество костей: "))
            self.dice_sides = int(input("Введите количество граней на кости: "))
            self.rolls_amount = int(input("Введите количество бросков: "))
            self.target_number = int(input("Введите целевую сумму: "))

            print("\n")

            if self.dices_amount <= 0 or self.dice_sides <= 0 or self.rolls_amount <= 0:
                print("Все числа должны быть положительными.")
                return

            if self.target_number < self.dices_amount * self.rolls_amount:
                print(f"Число не может быть меньше {self.dices_amount * self.rolls_amount}.")
                return

        except ValueError:
            print("Введите целое число.")

    def _get_single_roll_distribution(self):
        """
        Получение словаря: сумма -> количество способов получить её при одном броске `dices_amount` костей.
        """
        if self.dices_amount == 0:
            return {0: 1}

        dp = defaultdict(int)
        dp[0] = 1

        for _ in range(self.dices_amount):
            new_dp = defaultdict(int)
            for current_sum, count in dp.items():
                for face in range(1, self.dice_sides + 1):
                    new_dp[current_sum + face] += count
            dp = new_dp

        return dp

    def _calculate_probability(self):
        """
        Рассчитать вероятность получения `target_number` при `rolls_amount` бросках `dices_amount` костей с `dice_sides`
        гранями.
        """
        total_outcomes = (self.dice_sides ** self.dices_amount) ** self.rolls_amount

        dp = defaultdict(int)
        dp[0] = 1

        for _ in range(self.rolls_amount):
            new_dp = defaultdict(int)

            for current_sum, count in dp.items():
                single_roll_dist = self._get_single_roll_distribution()

                for roll_sum, ways in single_roll_dist.items():
                    new_dp[current_sum + roll_sum] += count * ways

            dp = new_dp

        target_outcomes = dp.get(self.target_number, 0)

        return target_outcomes, total_outcomes

    def _small_number_to_decimal_str(self, small_number: int | Decimal, precision: int = 4):
        """
        Преобразовать очень маленькое число (например, 8.2e-294) в строку вида "0.000...00082" с указанием количества
        нулей.
        """
        if small_number == 0:
            return "0.0"
        if small_number >= 1e-5:
            return f"{small_number:.{precision+5}f}".rstrip('0').rstrip('.') or "0.0"

        exponent = floor(log10(abs(small_number)))
        leading_zeros = -exponent - 1

        significand = small_number / Decimal(10 ** exponent)
        rounded_significand = round(significand, precision - 1)
        
        if rounded_significand >= 10:
            rounded_significand /= 10
            leading_zeros -= 1

        significand_str = f"{rounded_significand:.{precision}f}".rstrip('0').rstrip('.')
        if '.' in significand_str:
            significand_str = significand_str.replace('.', '')

        integer_part = "0"
        decimal_part = "0" * leading_zeros + significand_str

        if len(decimal_part) > 12:
            shown = decimal_part[:2] + "..." + decimal_part[-(precision + 2):]
            return f"{integer_part}.{shown}  (всего {leading_zeros} нулей до значащих цифр)"
        else:
            return f"{integer_part}.{decimal_part}"

    def main(self):
        try:
            target_outcomes, total_outcomes = self._calculate_probability()

            fraction = Fraction(target_outcomes, total_outcomes)
            fraction_probability = (f"{fraction.numerator}/{fraction.denominator}")

            if len(str(target_outcomes)) > 1:
                chance_numerator = Decimal(target_outcomes) // (10 ** (len(str(target_outcomes))-1))
                chance_denominator = Decimal(total_outcomes) // (10 ** (len(str(target_outcomes))-1))
                abt_probability = f"~{1}/{chance_denominator // chance_numerator}"
            else:
                abt_probability = f"{target_outcomes}/{total_outcomes}"

            percent_probability = Decimal(target_outcomes) / Decimal(total_outcomes) * 100
            percent_probability = self._small_number_to_decimal_str(percent_probability)

            print(f"\nРезультаты:")
            print(f"Целевая сумма: {self.target_number}")
            print(f"Количество благоприятных исходов: {target_outcomes}")
            print(f"Общее количество исходов: {total_outcomes}")
            print(
                f"Вероятность: " + 
                (
                    f"{abt_probability}" if
                    fraction_probability != abt_probability else
                    f"{fraction_probability}"
                ) +
                f", или ~{percent_probability}%"
            )

        except Exception as e:
            print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    probability = Probability()
    probability.main()