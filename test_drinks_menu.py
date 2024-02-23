import unittest
from vending_machine_simulator import DrinksMenu
# Define global variables for testing
drink1 = 'cappuccino'
price1 = 3.0
bom1 = {"water": 250, "milk": 100, "coffee": 24}
command1 = '/c'
drink2 = 'macchiatto'


class TestDrinksMenu(unittest.TestCase):

    def setUp(self) -> None:
        self.drinks_menu = DrinksMenu()

    
    def test_existence(self):
        self.assertFalse(self.drinks_menu.exist_drink(drink1))
        self.assertTrue(self.drinks_menu.add_drink(drink1, price1, bom1, command1))
        self.assertTrue(self.drinks_menu.exist_drink(drink1))
        
    # Test case for adding a new ordered_drink
    def test_add_drink(self):
        # Test adding a new ordered_drink
        self.assertFalse(self.drinks_menu.exist_drink(drink1))
        self.assertTrue(self.drinks_menu.add_drink(drink1, price1, bom1, command1))

        # Test adding an existing ordered_drink
        self.assertFalse(self.drinks_menu.add_drink(drink1, price1, bom1, command1))

    # Test case for getting the price of a ordered_drink
    def test_get_drink_price(self):
        # No ordered_drink in the menu
        self.assertFalse(self.drinks_menu.exist_drink(drink1))  # drinks_menu is empty
        # Add a ordered_drink to the drinks_menu
        self.drinks_menu.add_drink(drink1, price1, bom1, command1)

        # Test getting the price of an existing ordered_drink
        self.assertEqual(self.drinks_menu.get_drink_price(drink1), price1)

        # Test getting the price of a non-existing ordered_drink
        self.assertEqual(self.drinks_menu.get_drink_price(drink2), -1)

    # Test case for getting the BOM of a ordered_drink
    def test_get_drink_bom(self):
        # No ordered_drink in the menu
        self.assertFalse(self.drinks_menu.exist_drink(drink1))  # drinks_menu is empty
        # Add a ordered_drink to the drinks_menu
        self.drinks_menu.add_drink(drink1, price1, bom1, command1)

        # Test getting the BOM of an existing ordered_drink
        self.assertDictEqual(self.drinks_menu.get_drink_bom(drink1), bom1)

        # Test getting the BOM of a non-existing ordered_drink
        self.assertDictEqual(self.drinks_menu.get_drink_bom(drink2), {})

    # Test case for getting the command of a ordered_drink
    def test_get_drink_command(self):
        # No ordered_drink in the menu
        self.assertFalse(self.drinks_menu.exist_drink(drink1))  # drinks_menu is empty

        # Add a ordered_drink to the drinks_menu
        self.drinks_menu.add_drink(drink1, price1, bom1, command1)

        # Test getting the command of an existing ordered_drink
        self.assertEqual(self.drinks_menu.get_drink_command(drink1), command1)

        # Test getting the command of a non-existing ordered_drink
        self.assertEqual(self.drinks_menu.get_drink_command(drink2), '#')


if __name__ == '__main__':
    unittest.main()
