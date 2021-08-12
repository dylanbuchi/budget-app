from budget import Category
from budget import create_spend_chart
from unittest import main
from pprint import pprint

food = Category("Food")
entertainment = Category("Entertainment")
business = Category("Business")

food.deposit(900, "deposit")
entertainment.deposit(900, "deposit")
business.deposit(900, "deposit")
food.withdraw(105.55)
entertainment.withdraw(33.40)
business.withdraw(10.99)

result = create_spend_chart([business, food, entertainment])

print(result)

# Run unit tests automatically
# main(module='test', exit=False)