from __future__ import annotations
from typing import Union

import math

# custom annotation to accept a float or an int
float_int = Union[float, int]


class Category:
    total_withdraws = 0

    def __init__(self, name: str) -> None:
        self.name = name
        self.ledger = []
        self.balance = 0
        self.category_withdraws_total = 0

    def deposit(self, amount: float_int, description: str = '') -> None:
        self._append_to_ledger(amount, description)
        self.balance += amount

    def withdraw(self, amount: float_int, description: str = '') -> bool:
        if self.check_funds(amount):
            self._append_to_ledger(-amount, description)
            self.balance -= amount
            self.category_withdraws_total += math.floor((amount))
            Category.total_withdraws += math.floor((amount))
            return True
        return False

    def get_balance(self) -> float_int:
        return self.balance

    def transfer(self, amount: float_int, category: Category) -> bool:
        if self.check_funds(amount):
            description = f"Transfer to {category.name}"
            self.withdraw(amount, description)

            other_description = f"Transfer from {self.name}"
            category.deposit(amount, other_description)
            return True
        return False

    def check_funds(self, amount: float_int) -> bool:
        return amount <= self.balance

    def _append_to_ledger(self, *items) -> None:
        amount, description = items
        self.ledger.append({
            'amount': amount,
            'description': description,
        })

    def __str__(self) -> str:
        title = self._create_title_string()
        amount_and_description_strings = self._create_string_from_ledger()
        total = self._create_total_string()
        return f"{title}{amount_and_description_strings}{total}"

    def _create_string_from_ledger(self) -> str:
        strings = []
        for object in self.ledger:
            amount, description = object.values()
            description_max_23ch = description[:23]
            string = f"{description_max_23ch}" + f"{amount:.2f}".rjust(
                30 - len(description_max_23ch)) + "\n"
            strings.append(string)
        return ''.join(strings)

    def _create_title_string(self) -> str:
        return f"{self.name}".center(30, "*") + "\n"

    def _create_total_string(self) -> str:
        return f"Total: {self.balance}"

    def calculate_percentage(self):
        return (self.category_withdraws_total / Category.total_withdraws) * 100


def transform_percentages(percentage: int):
    string_percentage = str(percentage)
    if len(string_percentage) == 1:
        return 0
    elif len(string_percentage) == 2:
        return int(string_percentage[0] + '0')
    return 100


def create_spend_chart(categories: Category):
    result = []
    percentages = [math.floor(c.calculate_percentage()) for c in categories]

    percentages_transformed = list(map(transform_percentages, percentages))

    bar = ' o '
    space = "   "
    rule_map = {k: [] for k in range(100, -1, -10)}

    for v in rule_map.values():
        v.extend([space] * len(percentages_transformed))
        v.append(" ")

    temp = percentages_transformed.copy()

    while temp:
        percentage = temp.pop(0)
        index = percentages_transformed.index(percentage)
        while percentage >= 0:
            rule_map[percentage][index] = bar
            percentage -= 10

    result.append("Percentage spent by category\n")

    for p, bars in rule_map.items():
        percentage_str = f"{p}|".rjust(4)
        result.append(f"{percentage_str}{''.join(bars)}\n")

    result.append(" " * 4 + '-' * len(percentages_transformed)**2 + '-' + "\n")

    category_names = [c.name for c in categories]
    max_length = len((max(category_names, key=len)))

    for i in range(max_length):

        parts = ["    "]
        for name in category_names:
            if i < len(name):
                string = f" {name[i]}"

                parts.append(string + " ")
            else:

                parts.append("   ")
        if i != max_length - 1:

            parts.append(" \n")
        else:

            parts.append(" ")
        result.append(''.join(parts))

    return ''.join(result)
