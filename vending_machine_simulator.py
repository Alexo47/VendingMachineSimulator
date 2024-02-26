"""
Vending Machine Simulator - version 20240223 v11
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
=> This class deals with the vending machine DRINKS OFFER that clients can purchase
	
	=> attributes:
		drinks_menu is a dictionary with the following structure:
		{drink string:
		{'price': cost of the drink in float,
		'bom': {material name (str): required volume (float), material_name (str): ....}}
		'command': keystrokes to order string}
	
	=> methods:
		def exist_drink(self, drink: str) -> bool:
		def add_drink(self, drink: str, price: float, bom: Dict[str, int], command: str) -> bool:
		def get_drink_price(self, drink: str) -> float:
		def get_drink_bom(self, drink: str) -> Dict[str, int]:
		def get_drink_command(self, drink: str) -> str:
		
### class VendingMachineFinancials:
=>  Manages revenues and financial statistics
	=> attributes:
		vending_machine_revenue  # float value of cumulated payments of drinks ordered
	=> methods:
		def reset_revenue(self):
		def add_revenue(self, amount: float):
		def get_current_revenue(self) -> float:
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
	This class manages the materials (drink ingredients) containers of the vending machine
	Each container has a defined 'capacity' and is filled at 'volume' ranging [0:'capacity']
	
	acronym: 'mcd'  # will be used externally to reach it´s class methods
	
	attributes:
		materials_containers dictionary with the following structure:
		{'material name string':  {'capacity': value , 'volume': value}}
		materials_containers is encapsulated by getters methods described below
	
	methods:
		def exist_material_container(self, material):
		def allocate_material_container(self, material, capacity)
		def get_all_materials(self) -> list:
		def get_capacity_material_container(self, material):
		def get_volume_material_container(self, material):
		def refill_material_container(self, material):
		def takeout_material_container(self,material, volume):
		
	external methods: None
	
	"""
	
	def __init__(self) -> None:
		# Initialize the Materials dictionary
		self.materials_containers: Dict[str, Dict[str, Union[int, float]]] = {}
		
	
	
	def exist_material_container(self, material: str) -> bool:
		"""
		This method checks if there is a coins_dispenser allocated for a specific material.
		
		:param material: The name of the material to check.
		:return: True if a material_dispenser exists for the material, False otherwise.
		
		external calls:
			self.exist_material_container
		"""
		
		return material in self.materials_containers
	
	def allocate_material_container(self, material: str, capacity: int) -> bool:
		"""
		=> This method adds a new material container to the coins_dispenser
		It checks if the material container does not already exist
		If not it will add the new container with the capacity indicated and sets volume to 0
		
		:param material:  # kind of ingredient
		:param capacity:  # maximum volume container can be filled
		:return: True if container added - False if the material already has a container
		
		external calls:
			self.exist_material_container
		"""
		
		# Check if the material already exists
		if self.exist_material_container(material):
			return False
		# Add the material with the specified maximum quantity
		self.materials_containers[material] = {'capacity': capacity, 'volume': 0}
		return True
	
	def get_all_materials(self) -> list:
		"""
		Methods returns all the materials names (str) in a list structure
		:return: list of available materials
		"""
		material_list = []
		for material in self.materials_containers:
			material_list.append(material)
		return material_list
	
	def get_capacity_material_container(self, material: str) -> int:
		"""
		=> Get the capacity of the container allocated for a specific material.

		:param material:  # The name of the material to get the capacity of its container.
		:return capacity: # The capacity of the coins_dispenser allocated for the material.
		If the material container does not exist, returns a negative (-1) capacity value.
		
		external calls:
			self.exist_material_container
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
		
		external calls:
			self.exist_material_container
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
		:return volume: True if refill operation achieved False otherwise
		
		external calls:
			self.exist_material_container
			self.get_capacity_material_container
		"""
		
		if self.exist_material_container(material):
			
			# the container exist so we set volume = capacity
			self.materials_containers[material]['volume'] = (
				self.get_capacity_material_container(material)
			)
			return True
		
		return False
	
	def takeout_material_container(self, material, draw_volume):
		"""
		Drink order consume materials - This method reduce the volume of a particular material
		:param material:
		:param draw_volume:
		:return: True if withdrawal possible False otherwise
		
		external calls:
			self.exist_material_container
			self.get_volume_material_container
		"""
		if self.exist_material_container(material):
			current_volume = self.get_volume_material_container(material)
			reduced_volume = current_volume - draw_volume
			if reduced_volume < 0:
				return False
			self.materials_containers[material]['volume'] = reduced_volume
			return True
		return False

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
		def get_all_coins(self) -> list:
		def get_coin_value(self, coin: str) -> float:
	
	"""
	
	def __init__(self):
		# Initialize coins dictionary
		self.accepted_coins: Dict[str, float] = {}
	
	def exist_accepted_coins(self, coin: str) -> bool:
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
		
		external calls:
			self.exist_accepted_coins:
		"""
		
		# Check if the coin already exists
		if self.exist_accepted_coins(coin):
			return False
		
		# Add the coin with the specified value
		self.accepted_coins[coin] = value
		return True

	def get_all_coins(self) -> list:
		"""
		Methods returns all the coins names (str) in a list structure
		:return coins_list
		"""
		coin_list = []
		for coin in self.accepted_coins:
			coin_list.append(coin)
		return coin_list


	def get_coin_value(self, coin: str) -> float:
		"""
		Returns value of a coin if the coin is registered otherwise returns -1
		:param coin:  # name of the coin
		:return:  # the value of coin if registered otherwise returns -1
		
		external calls:
			self.exist_accepted_coins:
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
	=> This class deals with the drinks that clients can purchase through the vending machine
	
	=> attributes:
		drinks_menu is a dictionary with the following structure:
		{drink string:
		{'price': cost of the drink in float,
		'bom': {material name (str): required volume (float), material_name (str): ....}}
		'command': keystrokes to order string}
	
	=> methods:
		def exist_drink(self, drink: str) -> bool:
		def add_drink(
			self,
			drink: str,
			price: float,
			bom: Dict[str, int], command: str
		) -> bool:
		def get_all_drinks(self) -> list:
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
		Checks if a drink' figures in the drinks_menu

		:param drink: # The name of the drink to check in drinks_menu
		:return: True if 'drink' exists, False otherwise.
		"""
		
		return drink in self.drinks_menu
	
	
	def add_drink(self, drink: str, price: float, bom: Dict[str, int], command: str) -> bool:
		"""
		=> Adds a drink to the drinks_menu (a new drink offer for the customer)
		
		:param drink:  # name of the drink
		:param price: # cost of the drink
		:param bom:  # ingredients composition of the drink
		:param command: keystrokes to order the drink
		:return: True if drink added - False if drink already exists
		
		external calls:
			self.exist_drink:
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
	
	def get_all_drinks(self) -> list:
		"""
		Methods returns all the drinks names (str) in a list structure
		:return: list of available drinks
		"""
		drink_list = []
		for drink in self.drinks_menu:
			drink_list.append(drink)
		return drink_list
	
	def get_drink_price(self, drink: str) -> float:
		"""
		This method returns the price value (float) of a specified drink.
		If drink not in drinks_menu returns -1
		:param drink:
		:return price:  # Price of the drink or -1 if drink not registered
		
		external calls:
			self.exist_drink:
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

		external calls:
			self.exist_drink:
		
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
		:return command:  # keystrokes to command the drink or "#" if drink not registered
		
		external calls:
			self.exist_drink:
		"""
		
		if self.exist_drink(drink):
			command = self.drinks_menu[drink]['command']
		else:
			command = '#'
		return command

	
	# ###################################################################################
	# ## ===vending_machine_simulator=> Vending Machines Financials
	# ###################################################################################
	
class VendingMachineFinancials:
	"""
	Manages revenues and financial statistics
	attributes:
		vending_machine_revenue  # float value of cumulated payments of drinks ordered
	methods:
		def reset_revenue(self):
		def add_revenue(self, amount: float):
		def get_current_revenue(self) -> float:
	"""
	
	def __init__(self):
		self.vending_machine_revenue: float = 0.0
	
	
	def reset_revenue(self):
		"""
		Starts Vending Machine new business cycle
		"""
		self.vending_machine_revenue: float = 0.0
		return self.vending_machine_revenue
	
	def add_revenue(self, amount: float):
		"""
		User consumed a drink - the payment is added to the vending_machine_revenue
		:param amount:  # it corresponds to the drink price the user order
		"""
		self.vending_machine_revenue += amount
		
	def get_current_revenue(self) -> float:
		return self.vending_machine_revenue
	
print(f"\n===vending_machine_simulator=> Class/Methods/Attributes <20240223-v11> @ {date_stamp()}")
