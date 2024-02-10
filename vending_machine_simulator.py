"""
Vending Machine Simulator - version 20240210 v09
=> This Module handles all classes/methods/attributes related to drink vending machines operations

It consists of the following elements:

### class MaterialsContainersDispenser:
	=> This class handles the coins_dispenser of containers where each container is associated to a
	specific material (~ingredient such as coffee, water, milk, ...)
	
	## attributes:
		materials_containers dictionary with the following structure:
		{'material name string':  {'capacity': value , 'volume': value}}
	
	## methods:
		def exist_material_container(self, material):
		def allocate_material_container(self, material, capacity)
		def get_capacity_material_container(self, material):
		def get_volume_material_container(self, material):
		def refill_material_container(self, material):

### class AcceptedCoinsDispenser:
	=> This class is related to the payment of drinks with coins (no credit cards in this version)
	
	## attributes:
		accepted coins with following structure:
		{coin_name string: coin_value float}
	
	## Methods
		def add_accepted_coin(self, coin, value):
		
### Class Drinks Menu
	=> This class deals with the drink coins_dispenser OFFER that clients can purchase
	
	## attributes:
		drinks_menu is a dictionary with the following structure:
		{drink string: {'price': cost of the drink in float, 'command': keystrokes to order string}}
	
	## method:
		def add_drink(self, drink, price, command):
		
### class DrinksBom:
	=> This class manages the making of a particular drink, it relies on:
	the materials_containers (available ingredients)
	the drinks_menu : drinks to make
	
	## attributes:
		bom is a dictionary with following structure
		{drink name (str): {material name (str): required volume (float), ....}}
		
	## methods:
		def add_drink_bom(self, drink, materials):
		
### class DrinksBusinessOperations:
	=> This class manages customer orders, payments...cumulated revenue
	
	## attributes:
		uses objects defined in other classes namely:
		materials_dispenser, drinks_bom, drinks_menu, coins_accepted, business_cumulated_revenue
		
	=> methods:
		def check_availability(self, drink):
		def update_drink_volume(self, drink):
		def reset_revenue(self):
		def add_revenue(self, amount):
		def drink_checkout(self, drink):
		def ask_user_drink(self):
		def make_drink(self, drink):
		
### class DrinksBusinessMaintenance:
	=> This class manages all maintenance operations
	it uses materials_dispenser from MaterialsContainersDispensers
	
	=> attributes:
		admin_maintenance_commands is a dictionary with the following structure
			{keystrokes (string): command message (string)}
			
	=> methods:
		def add_admin_command(self, control_command):
		def report_containers_levels(self):
		def refill_all_containers(self):
		
	
	
"""

from datetime import datetime
from typing import Dict, Union


def date_stamp():
	"""
	=> Returns date_stamp for prints
	:return: date_time
	"""
	now = datetime.now()
	date_time = now.strftime("%Y/%m/%d, %H:%M")
	return date_time

# ###################################################################################
# ## ===vending_machine_simulator=> MaterialsContainersDispenser
# ###################################################################################

class MaterialsContainersDispenser:
	"""
	=> attributes:
		materials_containers dictionary with the following structure:
		{'material name string':  {'capacity': value , 'volume': value}}
		materials_containers is encapsulated by getters methods described below
	
	=> methods:
		def exist_material_container(self, material):
		def allocate_material_container(self, material, capacity)
		def get_capacity_material_container(self, material):
		def get_volume_material_container(self, material):
		def refill_material_container(self, material):
	
	"""
	
	def __init__(self) -> None:
		# Initialize the Materials dictionary
		self.materials_containers: Dict[str, Dict[str, Union[int, float]]] = {}
		
	
	
	def exist_material_container(self, material: str) -> bool:
		"""
		=> This method checks if there is a coins_dispenser allocated for a specific material.
		
		:param material: The name of the material to check.
		
		:return: True if a coins_dispenser exists for the material, False otherwise.
		"""
		
		return material in self.materials_containers
	
	def allocate_material_container(self, material: str, capacity: int) -> bool:
		"""
		=> This method adds a new material container to the coins_dispenser
		It checks if the material container does not already exist
		If not it will add the new container with the capacity indicated and sets volume to 0
		
		:param material:
		:param capacity:
		
		:return: True if container added - False if the material already has a container
		"""
		
		# Check if the material already exists
		if self.exist_material_container(material):
			return False
		# Add the material with the specified maximum quantity
		self.materials_containers[material] = {'capacity': capacity, 'volume': 0}
		return True
	
	def get_capacity_material_container(self, material: str) -> int:
		"""
		=> Get the capacity of the container allocated for a specific material.

		:param material: The name of the material to get the capacity of its container.
			
		:return capacity: The capacity of the coins_dispenser allocated for the material.
		If the material container does not exist, returns a negative (-1) capacity value.
		"""
		
		if self.exist_material_container(material):
			capacity = self.materials_containers[material]['capacity']
		else:
			capacity = -1
		return capacity
	
	def get_volume_material_container(self, material: str) -> int:
		"""
		=> This method returns the volume of the container allocated for a specific material.
		
		:param material:
		
		:return volume: The volume of material available on it´s coins_dispenser - If the material does
		not have a coins_dispenser the volume returned is negative number -1
		"""
		
		if self.exist_material_container(material):
			volume = self.materials_containers[material]['volume']
		else:
			volume = -1
		return volume
	
	def refill_material_container(self, material: str) -> int:
		
		"""
		=> This method fills the container for a specified material (~ingredient)
		It does not manage any ingredient refill packs therefore the action is limited
		to set volume = capacity
		
		:param material: indicates what material (ingredient) is to be filled
		
		:return volume: container capacity if container exist otherwise volume = -1
		"""
		
		if self.exist_material_container(material):
			
			# the container exist so we set volume = capacity
			volume = MaterialsContainersDispenser.get_capacity_material_container(self, material)
			self.materials_containers[material]['volume'] = volume
		
		else:
			volume = -1
		
		return volume


# ###################################################################################
# ## ===vending_machine_simulator=> Accepted Coins Dispenser
# ###################################################################################

class AcceptedCoinsDispenser:
	"""
	=> This class is related to the payment of drinks with coins (no credit cards in this version)
	
	## attributes:
		accepted coins with following structure:
		{coin_name string: coin_value float}
	
	## Methods
		def exist_accepted_coin(self,coin: str) -> bool:
		def add_accepted_coin(self, coin: str, value: float) -> bool:
		def get_accepted_coins_value(self, coin: str) -> float:
	
	"""
	
	def __init__(self):
		# Initialize coins dictionary
		self.accepted_coins: Dict[str, float] = {}
	
	def exist_accepted_coins(self,coin: str) -> bool:
		"""
		Checks if a 'coin' is registered at the coins_dispenser
		:param coin:
		:return: True if coin is registered otherwise False
		"""
		return coin in self.accepted_coins
	
	def add_accepted_coins(self, coin: str, value: float) -> bool:
		"""
		=> This method adds a new accepted coin if the coin is not yet already accepted
		
		:param coin: name of the coin
		:param value: value in dollar/cents
		
		:return: True if coin is a new type False if coin already accepted by the coins_dispenser
		"""
		
		# Check if the coin already exists
		if self.exist_accepted_coins(coin):
			return False
		
		# Add the coin with the specified value
		self.accepted_coins[coin] = value
		return True

	def get_accepted_coins_value(self, coin: str) -> float:
		"""
		Returns value of a coin if the coin is registered otherwise returns -1
		:param coin:  # name of the coin
		:return:  # the value of coin if registered otherwise returns -1
		"""
		if self.exist_accepted_coins(coin):
			value = self.accepted_coins[coin]
		else:
			value = -1.
		return value
		
		
# ###################################################################################
# ## ===vending_machine_simulator=> Drinks Menu
# ###################################################################################


class DrinksMenu:

	"""
	=> This class deals with the drink coins_dispenser OFFER that clients can purchase
	
	=> attributes:
		drinks_menu is a dictionary with the following structure:
		{drink string:
		{'price': cost of the drink in float,
		'bom': {material name (str): required volume (float), material_name (str): ....}}
		'command': keystrokes to order string}}
	
	=> methods:
		def exist_drink(self, drink: str) -> bool:
		def add_drink(self, drink: str, price: float, bom: Dict[str, int], command: str) -> bool:
		def get_drink_price(self, drink: str) -> float:
		def get_drink_bom(self, drink: str) -> Dict[str, int]:
		def get_drink_command(self, drink: str) -> str:
		
	"""
	
	def __init__(self) -> None:
		"""
		Initializes the drinks drinks_menu with an empty dictionary.
		"""
		self.drinks_menu: Dict[str, Dict[str, Union[float, str, Dict[str, int]]]] = {}
	
	
	def exist_drink(self, drink: str) -> bool:
		"""
		=> This method checks if a 'drink' figures in the drinks_menu

		:param drink: The name of the drink to check in drinks)drinks_menu

		:return: True if 'drink' exists, False otherwise.
		"""
		
		return drink in self.drinks_menu
	
	
	def add_drink(self, drink: str, price: float, bom: Dict[str, int], command: str) -> bool:
		"""
		=> This method adds a new drink to the drinks_menu (a new drink offer for the customer)
		
		:param drink:  # name of the drink
		:param price: # cost of the drink
		:param bom:  # ingredients composition of the drink
		:param command: keystrokes to order the drink
		:return: True if drink added - False if drink already exists
		"""
		
		# Check if the drink already exists
		
		if self.exist_drink(drink):
			return False
		
		# Add the drink with the specified price, bom and command
		
		self.drinks_menu[drink] = {
			'price': price,
			'bom': bom,
			'command': command
		}
		return True
	
	def get_drink_price(self, drink: str) -> float:
		"""
		This method returns the price value (float) of a specified drink.
		If drink not in drinks_menu returns -1
		:param drink:
		:return price:  # Price of the drink or -1 if drink not registered
		"""
		
		if self.exist_drink(drink):
			price = self.drinks_menu[drink]['price']
		else:
			price = -1.
		return price
		
	def get_drink_bom(self, drink: str) -> Dict[str, int]:
		"""
		This method returns the bom {ingredient: volume}  of a specified drink.
		If drink not in drinks_menu returns empty dictionary {}
		:param drink:
		:return bom:  # BOM of the drink or {} if drink not registered
		"""
		
		if self.exist_drink(drink):
			bom = self.drinks_menu[drink]['bom']
		else:
			bom = {}
		return bom
	
	def get_drink_command(self, drink: str) -> str:
		"""
		This method returns the command keystrokes (string) to launch the order
		If drink not in drinks_menu returns -1
		:param drink:
		:return command:  # commnd of the drink or "#" if drink not registered
		"""
		
		if self.exist_drink(drink):
			command = self.drinks_menu[drink]['command']
		else:
			command = '#'
		return command



# ###################################################################################
# ## ===vending_machine_simulator=> Drinks Business Operations
# ###################################################################################

class DrinksBusinessOperations:
	# TODO Fully encapsulate DrinksBusinessOperations Class
	"""
	=> This class manages customer orders, payments...cumulated revenue
	
	=> attributes:
		uses objects defined in other classes namely:
		materials_dispenser, drinks_bom, drinks_menu, coins_accepted, business_cumulated_revenue
		
	=> methods:
		def check_availability(self, drink):
		def update_drink_volume(self, drink):
		def reset_revenue(self):
		def add_revenue(self, amount):
		def drink_checkout(self, drink):
		def ask_user_drink(self):
		def make_drink(self, drink):
		
	"""
	
	def __init__(
			self,
			materials_dispenser,
			drinks_bom,
			drinks_menu,
			coins_accepted,
			business_cumulated_revenue
	):
		# Initialize the Materials dictionary
		self.business_cumulated_revenue = business_cumulated_revenue
		self.materials_dispenser = materials_dispenser
		self.drinks_bom = drinks_bom
		self.drinks_menu = drinks_menu
		self.coins_accepted = coins_accepted
	
	def check_availability(self, drink):
		"""
		
		:param drink:
		:return:
		"""
		current_bom = self.drinks_bom.bom[drink]
		count_ok = 0
		for ingredient in self.drinks_bom.bom[drink]:
			availability = self.materials_dispenser.materials_containers[ingredient]['volume']
			required = self.drinks_bom.bom[drink][ingredient]
			if availability >= required:
				count_ok += 1
		if count_ok == len(current_bom):
			return True
		
		return False
	
	def update_drink_volume(self, drink):
		"""
		
		:param drink:
		:return:
		"""
		current_bom = self.drinks_bom.bom[drink]
		material_count = 0
		for material in current_bom:
			current_fill = self.materials_dispenser.materials_containers[material]['volume']
			drink_required_fill = current_bom[material]
			if current_fill >= drink_required_fill:
				current_fill -= drink_required_fill
				self.materials_dispenser.materials_containers[material]['volume'] = current_fill
				material_count += 1
			else:
				print(
					f"\n===DrinksBusinessOperations/update_drink_volume=> {date_stamp()}"
					f" {drink} update failed - last drink served not enough {material}"
					f" This should be considered as a coins_dispenser program inconsistency"
				)
		if material_count == len(current_bom):
			return True
		return False
	
	def reset_revenue(self):
		"""
		
		:return:
		"""
		self.business_cumulated_revenue = 0
	
	def add_revenue(self, amount):
		"""
		
		:param amount:
		:return:
		"""
		self.business_cumulated_revenue += amount
	
	def drink_checkout(self, drink):
		"""
		
		:param drink:
		:return:
		"""
		
		drink_cost = self.drinks_menu.drinks_menu[drink]['price']
		current_payment = 0
		
		for coin in self.coins_accepted.accepted_coins:
			number_coins = int(input(f" <{coin}> : How many?"))
			current_payment += self.coins_accepted.accepted_coins[coin] * number_coins
			if drink_cost <= current_payment:
				change = current_payment - drink_cost
				print(f" You are all set for your <{drink}> and your change is <{change}>")
				return True, change
		
		# at this level the user introduced an insufficient amount to pay for his drink
		change = current_payment
		print(
			f" {current_payment} is insufficient for your <{drink}> that costs: <{drink_cost}"
			f" Here is your change: {change}"
		)
		return False, change
	
	def ask_user_drink(self):
		"""
		
		:return:
		"""
		
		for drink in self.drinks_menu:
			if DrinksBusinessOperations.check_availability(self, drink):
				print(
					f"Want {drink} for {self.drinks_menu[drink]['price']} US$?"
					f"then type: {self.drinks_menu[drink]['command']}"
				)
		user_choice = input("So what is your choice? =?> ")
		print(f"\n===u100d_coffee-machine=> You ordered {user_choice}")
		if user_choice in self.drinks_menu:
			user_drink = self.drinks_menu[user_choice]
		else:
			print(f" !!! Your selection is not recognized by the coins_dispenser - Try again")
			user_drink = ''
		return user_drink
	
	def make_drink(self, drink):
		"""
		
		:param drink:
		:return:
		"""
		
		# we need now to remove the ingredients consumption of the drink
		return self.update_drink_volume(drink)


# ###################################################################################
# ## ===vending_machine_simulator=> Drinks Business Maintenance
# ###################################################################################


class DrinksBusinessMaintenance:
	# TODO Fully encapsulate DrinksBusinessMaintenance Class
	"""
	=> This class manages all maintenance operations
	it uses materials_dispenser from MaterialsContainersDispensers
	
	=> attributes:
		admin_maintenance_commands is a dictionary with the following structure
			{keystrokes (string): command message (string)}
			
	=> methods:
		def add_admin_command(self, control_command):
		def report_containers_levels(self):
		def refill_all_containers(self):
			
	"""
	
	def __init__(
			self,
			materials_dispenser
	):
		self.admin_maintenance_commands = {}
		self.materials_dispenser = materials_dispenser
	
	def add_admin_command(self, control_command):
		"""
		
		:param control_command:
		:return:
		"""
		control_command_keystroke, control_command_message = list(control_command.items())[0]
		# print(
		# 	f"\n===DrinksBusinessMaintenance/add_admin_command=> @ {date_stamp()}"
		# 	f"\n parameter control_command: <{control_command}>"
		# 	f"\n variable control_command_keystroke: <{control_command_keystroke} ")

		
		for command in self.admin_maintenance_commands:
			if command == control_command_keystroke:
				print(
					f"\n===DrinksBusinessMaintenance/add_admin_command=> {date_stamp()}"
					f"{control_command_keystroke} already configured in the ContainerDispenser"
				)
				return False
		self.admin_maintenance_commands[control_command_keystroke] = control_command_message
		return True
	
	def report_containers_levels(self):
		"""
		
		:return:
		"""
		time_stamp = date_stamp()
		print(
			f"At this point of time: {time_stamp}"
			f"The Containers are in the following status:"
		)
		for material in self.materials_dispenser:
			material_capacity = self.materials_dispenser[material]['capacity']
			material_volume = self.materials_dispenser[material]['volume']
			# material = materials_available.key()
			# filled = materials_available.value()
			print(
				f" Container of: <{material}> with total capacity of {material_capacity}"
				f" is currently filled at {material_volume} level"
			)
	
	def refill_all_containers(self):
		"""
		
		:return:
		"""
		materials_volume = {}
		for material in self.materials_dispenser.materials_containers:
			volume = self.materials_dispenser.refill_material_container(material)
			materials_volume[material] = volume
		return materials_volume


print(f"\n===vending_machine_simulator=> Class/Methods/Attributes <20240210-v09> @ {date_stamp()}")
