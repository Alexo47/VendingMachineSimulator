# vending_machine.py
import logging

class MaterialsContainersDispenser:
    def __init__(self, capacity):
        self.capacity = capacity
        self.current_volume = capacity
        logging.debug(f"MaterialsContainersDispenser initialized with capacity: {capacity}")

    def refill(self):
        self.current_volume = self.capacity
        logging.debug("MaterialsContainersDispenser refilled")

    def use(self, amount):
        logging.debug(f"Attempting to use {amount} from {self.current_volume} available")
        if self.current_volume >= amount:
            self.current_volume -= amount
            logging.debug(f"New volume after use: {self.current_volume}")
            return True
        logging.debug("Not enough volume to use the requested amount")
        return False

    def get_volume(self):
        return self.current_volume


class AcceptedCoinsDispenser:
    def __init__(self, coin_values):
        self.coin_values = coin_values

    def validate_payment(self, payment, price):
        total = sum(payment[coin] * self.coin_values[coin] for coin in payment)
        if total >= price:
            return total - price
        return None


class DrinksMenu:
    def __init__(self, menu):
        self.menu = menu

    def get_drinks(self):
        return self.menu.keys()

    def get_price(self, drink):
        return self.menu[drink]['price']

    def get_ingredients(self, drink):
        return self.menu[drink]  # Return the entire drink definition (water, milk, coffee)


class VendingMachine:
    def __init__(self, materials_capacity, coin_values, menu, drink_price):
        self.dispenser = {material: MaterialsContainersDispenser(capacity) for material, capacity in materials_capacity.items()}
        self.coin_dispenser = AcceptedCoinsDispenser(coin_values)
        self.menu = DrinksMenu(menu)
        self.drink_price = drink_price
        self.is_shutdown = False  # To track if the machine is shutdown

    def check_availability(self, drink):
        ingredients = self.menu.get_ingredients(drink)
        available = all(self.dispenser[material].get_volume() >= amount for material, amount in ingredients.items())
        logging.debug(f"Check availability for {drink}: {available}")
        return available
    
    def check_maintenance(self):
        for drink in self.menu.get_drinks():
            if self.check_availability(drink):
                return False  # At least one drink is available
        self.is_shutdown = True
        return True  # No drinks available, enter maintenance mode

    def make_drink(self, drink):
        if not self.check_availability(drink):
            return False
        ingredients = self.menu.get_ingredients(drink)
        for material, amount in ingredients.items():
            self.dispenser[material].use(amount)
        return True

    def refill(self):
        for dispenser in self.dispenser.values():
            dispenser.refill()
        self.is_shutdown = False
        logging.debug("Machine refilled and restarted")

    def process_payment(self, drink, payment):
        if drink not in self.drink_price:
            return None

        price = self.drink_price[drink]
        change = self.coin_dispenser.validate_payment(payment, price)
        if change is not None:
            return change
        return None
