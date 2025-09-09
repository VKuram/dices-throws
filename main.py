from collections import defaultdict
from decimal import Decimal, getcontext
from fractions import Fraction


getcontext().prec = 10000 # Точность для Decimal


def calculate_probability(num_dice, faces, num_rolls, target_sum):
    """
    Рассчитывает вероятность получения target_sum при num_rolls бросках num_dice костей с faces гранями.
    """

    # Общее количество возможных исходов
    total_outcomes = (faces ** num_dice) ** num_rolls

    # DP: dp[бросок][сумма] = количество способов получить эту сумму после этого броска
    # Начинаем с 0-го броска: сумма 0 -> 1 способ
    dp = defaultdict(int)
    dp[0] = 1

    # Для каждого броска
    for roll in range(num_rolls):
        new_dp = defaultdict(int)
        # Для каждой суммы, достигнутой на предыдущем шаге
        for current_sum, count in dp.items():
            # Генерируем все возможные суммы для одного броска num_dice костей
            # Используем рекурсию / вложенные циклы для генерации сумм одного броска
            # Но для эффективности — предварительно посчитаем распределение сумм для одного броска
            # (можно вынести в отдельную функцию и кэшировать)

            # Распределение сумм для одного броска num_dice костей с faces гранями
            single_roll_dist = get_single_roll_distribution(num_dice, faces)

            # Для каждого возможного результата одного броска
            for roll_sum, ways in single_roll_dist.items():
                new_dp[current_sum + roll_sum] += count * ways

        dp = new_dp

    # Количество способов получить target_sum
    favorable_outcomes = dp.get(target_sum, 0)

    return favorable_outcomes, total_outcomes


def get_single_roll_distribution(num_dice, faces):
    """
    Возвращает словарь: сумма -> количество способов получить её при одном броске num_dice костей.
    """
    from collections import defaultdict

    if num_dice == 0:
        return {0: 1}

    # dp[i] = количество способов получить сумму i
    dp = defaultdict(int)
    dp[0] = 1

    # Добавляем по одной кости
    for _ in range(num_dice):
        new_dp = defaultdict(int)
        for current_sum, count in dp.items():
            for face in range(1, faces + 1):
                new_dp[current_sum + face] += count
        dp = new_dp

    return dp


def main():
    print("=== Расчёт вероятности выпадения суммы при бросках костей ===")
    try:
        num_dice = int(input("Введите количество костей: "))
        faces = int(input("Введите количество граней на кости: "))
        num_rolls = int(input("Введите количество бросков: "))
        target_sum = int(input("Введите целевую сумму: "))

        if num_dice <= 0 or faces <= 0 or num_rolls <= 0:
            print("Все числа должны быть положительными.")
            return

        if target_sum < num_dice * num_rolls:
            print(f"Число не может быть меньше {num_dice * num_rolls}.")
            return

        favorable, total = calculate_probability(num_dice, faces, num_rolls, target_sum)

        fraction = Fraction(favorable, total)
        fraction_probability = (f"{fraction.numerator}/{fraction.denominator}")

        if len(str(favorable)) > 1:
            chance_numerator = Decimal(favorable) // (10 ** (len(str(favorable))-1)) # Сокращаем до 1 знака вывод текстом, если значения слишком большие
            chance_denominator = Decimal(total) // (10 ** (len(str(favorable))-1))
            abt_probability = f"~{1}/{chance_denominator // chance_numerator}"
        else:
            abt_probability = f"{favorable}/{total}"




        print(f"\nРезультаты:")
        print(f"Целевая сумма: {target_sum}")
        print(f"Количество благоприятных исходов: {favorable}")
        print(f"Общее количество исходов: {total}")
        print(f"Вероятность: " + (
                f"{abt_probability}" if
                fraction_probability != abt_probability else
                f"{fraction_probability}"
            ))

        # Опционально: вывод распределения всех сумм
        show_all = input("\nПоказать полное распределение сумм? (y/n): ").strip().lower()
        if show_all == 'y':
            from collections import defaultdict
            dp = defaultdict(int)
            dp[0] = 1
            for _ in range(num_rolls):
                new_dp = defaultdict(int)
                single_roll_dist = get_single_roll_distribution(num_dice, faces)
                for current_sum, count in dp.items():
                    for roll_sum, ways in single_roll_dist.items():
                        new_dp[current_sum + roll_sum] += count * ways
                dp = new_dp

            print("\nРаспределение сумм:")
            for s in sorted(dp.keys()):
                print(f"{s}: {dp[s]}")

    except ValueError:
        print("1 числа.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()