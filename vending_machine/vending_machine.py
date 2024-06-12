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
        total = sum(self.coin_values[coin] * count for coin, count in payment.items())
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

    def get_bom(self, drink):
        return self.menu[drink]['bom']

    def get_command(self, drink):
        return self.menu[drink]['command']


class VendingMachine:
    def __init__(self, materials_capacity, coin_values, menu):
        self.dispenser = {material: MaterialsContainersDispenser(capacity) for material, capacity in materials_capacity.items()}
        self.coin_dispenser = AcceptedCoinsDispenser(coin_values)
        self.menu = DrinksMenu(menu)

    def check_availability(self, drink):
        bom = self.menu.get_bom(drink)
        return all(self.dispenser[material].get_volume() >= amount for material, amount in bom.items())

    def make_drink(self, drink):
        if self.check_availability(drink):
            bom = self.menu.get_bom(drink)
            for material, amount in bom.items():
                self.dispenser[material].use(amount)
            return True
        return False

    def refill(self):
        for material in self.dispenser.values():
            material.refill()

    def process_payment(self, drink, payment):
        price = self.menu.get_price(drink)
        change = self.coin_dispenser.validate_payment(payment, price)
        if change is not None:
            return change
        return None
