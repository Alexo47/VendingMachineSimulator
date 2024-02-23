import unittest
from vending_machine_simulator import VendingMachineFinancials

initial_revenue: float = 0.0
new_sale: float = 2.5


class TestVendingMachineFinancials(unittest.TestCase):
    def setUp(self):
        # Instantiate a new AcceptedCoinsDispenser object before each test
        self.machine_revenue = VendingMachineFinancials()

    def test_reset_revenue(self):
        self.assertTrue(self.machine_revenue, initial_revenue)
        self.machine_revenue.add_revenue(new_sale)
        self.assertTrue(self.machine_revenue, new_sale)
        self.assertAlmostEqual(self.machine_revenue.reset_revenue(), initial_revenue)


    def test_add_revenue(self):
        
        self.assertTrue(self.machine_revenue, initial_revenue)
        self.machine_revenue.add_revenue(new_sale)
        self.machine_revenue.add_revenue(new_sale)
        self.machine_revenue.add_revenue(new_sale)
        self.machine_revenue.add_revenue(new_sale)
        self.assertTrue(self.machine_revenue, 4 * new_sale)
        self.assertAlmostEqual(self.machine_revenue.reset_revenue(), initial_revenue)
    
    def test_get_current_revenue(self):
        self.assertTrue(self.machine_revenue, initial_revenue)
        self.machine_revenue.add_revenue(new_sale)
        self.machine_revenue.add_revenue(new_sale)
        self.machine_revenue.add_revenue(new_sale)
        self.machine_revenue.add_revenue(new_sale)
        # self.assertTrue(self.machine_revenue.get_current_revenue(), 4 * new_sale)
        self.assertAlmostEqual(self.machine_revenue.reset_revenue(), initial_revenue)

if __name__ == '__main__':
    unittest.main()
