import logging


class MaterialsContainersDispenser:
    def __init__(self, capacity):
        self.capacity = capacity
        self.current_volume = capacity
        logging.debug(f"MaterialsContainersDispenser=> initialized with capacity: {capacity}")
    
    def refill(self):
        self.current_volume = self.capacity
        logging.debug("===MaterialsContainersDispenser.refill=>  refilled")
    
    def use(self, amount):
        logging.debug(
            f"===MaterialsContainersDispenser.use=> Attempting to use {amount} from {self.current_volume} available")
        if self.current_volume >= amount:
            self.current_volume -= amount
            logging.debug(
                f"===MaterialsContainersDispenser.use=> Volume after use: {self.current_volume}")
            return True
        logging.debug(
            f"===MaterialsContainersDispenser.use=>  {self.current_volume} < for amount {amount}")
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
    def __init__(
            self,
            materials_capacity,
            coin_values,
            menu,
            drink_price,
            vending_machine_states,
            vending_machine_current_state
    ):
        self.dispenser = {material: MaterialsContainersDispenser(capacity) for material, capacity in
                          materials_capacity.items()}
        self.coin_dispenser = AcceptedCoinsDispenser(coin_values)
        self.menu = DrinksMenu(menu)
        self.drink_price = drink_price
        self.possible_states = vending_machine_states
        self.current_state = vending_machine_current_state
    
    def get_state(self):
        return self.current_state
    
    def check_availability(self, drink):
        if self.current_state == "in_maintenance":
            return False
        ingredients = self.menu.get_ingredients(drink)
        available = all(self.dispenser[material].get_volume() >= amount for material, amount in
                        ingredients.items())
        return available
    
    def check_maintenance(self):
        for drink in self.menu.get_drinks():
            if self.check_availability(drink):
                self.current_state = "in_operation"
                return False  # At least one drink is available
        self.current_state = "in_maintenance"
        return True  # No drinks available, enter maintenance mode
    
    def make_drink(self, drink):
        if not self.check_availability(drink):
            return False
        
        logging.debug(f'===VendingMachine.make_drink=> starting making drink: {drink}')
        
        ingredients = self.menu.get_ingredients(drink)
        for material, amount in ingredients.items():
            logging.debug(
                f'===VendingMachine.make_drink=> {drink} / {material} call use({amount}) ')
            self.dispenser[material].use(amount)
        
        logging.debug(f'===VendingMachine.make_drink=> finished making drink: {drink}')
        return True
    
    def refill(self):
        for dispenser in self.dispenser.values():
            dispenser.refill()
        self.current_state = "in_operation"
    
    def process_payment(self, drink, payment):
        if drink not in self.drink_price:
            return None
        
        price = self.drink_price[drink]
        change = self.coin_dispenser.validate_payment(payment, price)
        if change is not None:
            return change
        return None
