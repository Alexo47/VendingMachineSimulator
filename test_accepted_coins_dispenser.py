import unittest
from vending_machine_simulator import AcceptedCoinsDispenser

# Global variables for coins and their values
coin1 = 'quarter'
coin1_value = 0.25
coin2 = 'dime'
coin2_value = 0.10
invalid_value = -1

class TestAcceptedCoinsDispenser(unittest.TestCase):
    def setUp(self):
        # Instantiate a new AcceptedCoinsDispenser object before each test
        self.coins_dispenser = AcceptedCoinsDispenser()

    def test_exist_accepted_coins(self):
        # Test case for exist_accepted_coins method
        self.assertFalse(self.coins_dispenser.exist_accepted_coins(coin1))
        self.assertTrue(self.coins_dispenser.add_accepted_coins(coin1, coin1_value))
        self.assertTrue(self.coins_dispenser.exist_accepted_coins(coin1))

    def test_add_accepted_coins(self):
        # Test case for add_accepted_coins method
        self.assertTrue(self.coins_dispenser.add_accepted_coins(coin2, coin2_value))
        self.assertTrue(self.coins_dispenser.exist_accepted_coins(coin2))
        self.assertFalse(self.coins_dispenser.add_accepted_coins(coin2, coin2_value))

    def test_get_accepted_coins_value(self):
        # Test case for get_coin_value method
        self.assertTrue(self.coins_dispenser.get_coin_value(coin1), invalid_value)
        self.assertTrue(self.coins_dispenser.add_accepted_coins(coin1, coin1_value))
        self.assertAlmostEqual(self.coins_dispenser.get_coin_value(coin1), coin1_value)

if __name__ == '__main__':
    unittest.main()

