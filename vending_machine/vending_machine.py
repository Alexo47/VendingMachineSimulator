# vending_machine.py

class MaterialsContainersDispenser:
    def __init__(self, capacity):
        self.capacity = capacity
        self.current_volume = capacity

    def refill(self):
        self.current_volume = self.capacity

    def use(self, amount):
        if self.current_volume >= amount:
            self.current_volume -= amount
            return True
        return False

    def get_volume(self):
        return self.current_volume


class AcceptedCoinsDispenser:
    def __init__(self, coin_values):
        self.coin_values = coin_values

    def validate_payment(self, payment, price):
        total = sum(payment[coin] * self.coin_values[coin] for coin in payment)  # Use list comprehension for shorter code
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
    
    def get_ingredients(self, drink):  # This method is no longer needed in this case
        return self.menu[drink]  # Return the entire drink definition (water, milk, coffee)
    
   

class VendingMachine:
    def __init__(self, materials_capacity, coin_values, menu, drink_price):
        self.dispenser = {material: MaterialsContainersDispenser(capacity) for material, capacity in materials_capacity.items()}
        self.coin_dispenser = AcceptedCoinsDispenser(coin_values)
        self.menu = DrinksMenu(menu)
        self.drink_price = drink_price  # Store drink_price in the object

    def check_availability(self, drink):
        ingredients = self.menu.get_ingredients(drink)  # Use get_ingredients for consistency
        return all(self.dispenser[material].get_volume() >= amount for material, amount in ingredients.items())

    def make_drink(self, drink):
        if self.check_availability(drink):
            ingredients = self.menu.get_ingredients(drink)
            for material, amount in ingredients.items():
                self.dispenser[material].use(amount)
            return True
        return False

    def refill(self):
        for material in self.dispenser.values():
            material.refill()

    def process_payment(self, drink, payment):
        if drink not in self.drink_price:  # Check if drink exists in drink_price
            return None  # Handle invalid drink selection (optional)

        price = self.drink_price[drink]
        change = self.coin_dispenser.validate_payment(payment, price)
        if change is not None:
            return change
        return None

