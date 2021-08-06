from __future__ import annotations
from typing import Union

# custom annotation to accept a float or an int
float_int = Union[float, int]


class Category:
    def __init__(self, name: str) -> None:
        self.name = name
        self.ledger = []
        self.balance = 0

    def deposit(self, amount: float_int, description: str = '') -> None:
        self._append_to_ledger(amount, description)
        self.balance += amount

    def withdraw(self, amount: float_int, description: str = '') -> bool:
        if self.check_funds(amount):
            self._append_to_ledger(-amount, description)
            self.balance -= amount
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
