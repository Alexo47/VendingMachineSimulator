# drink_distribution_business package - version 202401301 v06


from datetime import datetime


def date_stamp():
	"""
	=> Returns date_stamp for prints
	:return: date_time
	"""
	now = datetime.now()
	date_time = now.strftime("%Y/%m/%d, %H:%M")
	return date_time

# ###################################################################################
# ## ===drink_distribution_business=> MaterialsContainersDispenser
# ###################################################################################

class MaterialsContainersDispenser:
	"""
	=> attributes:
		materials_containers dictionary with the following structure:
		{'material name string':  {'capacity': value , 'volume': value}}
	
	=> methods:
		def add_material_container(self, material_container, capacity)
		def material_container_status(self,material)
		def refill_material_container(self, material, volume)
	
	"""
	
	def __init__(self):
		# Initialize the Materials dictionary
		self.materials_containers = {}
		
	def add_material_container(self, material_container, capacity):
		"""
		=> This method adds a new container to the dispenser
		It checks if the material container does not already exist
		If not it will add the new container with the capacity indicated and sets volume to 0
		:param material_container:
		:param capacity:
		:return: True if container added - False if the material already has a container
		"""
		# Check if the material_container already exists
		if material_container in self.materials_containers:
			print(
				f"\n===MaterialsContainersDispenser/add_material_container=> {date_stamp()}"
				f"{material_container} already configured in the ContainerDispenser"
			)
			return False
		else:
			# Add the material_container with the specified maximum quantity
			self.materials_containers[material_container] = {'capacity': capacity, 'volume': 0}
			# self.materials_containers[material_container]['capacity'] = capacity
			# self.materials_containers[material_container]['volume'] = 0
			print(
				f"\n===MaterialsContainersDispenser/add_material_container=> {date_stamp()}"
				f"{material_container} added to ContainerDispenser capacity:{capacity} & volume = 0"
			)
			return True
	
	
	def material_container_status(self, materials_containers, material):
		
		"""
		=> This method returns capacity & current volume of the container of a material
		:param materials_containers:
		:param material:
		:return: container_volume
		"""

		
		if material in materials_containers:
			container_capacity = self.materials_containers[material]['capacity']
			container_volume = self.materials_containers[material]['volume']
			print(
				f"\n===MaterialsContainersDispenser/container_status=> {date_stamp()}"
				f"{material} dispenser capacity: <{container_capacity}>"
				f" the container currently filled with volume: {container_volume}"
			)
		else:
			container_capacity = 0
			container_volume = 0
			print(
				f"\n===MaterialsContainersDispenser/container_status=> {date_stamp()}"
				f" There is no such {material} container available at dispenser"
				f" Therefore returned status capacity, volume = 0 "
			)
		return container_capacity, container_volume

	
	def refill_material_container(self, materials_containers, material):
		"""
		=> This method fills the container for a specified material (~ingredient)
		It does not manage any ingredient refill packs therefore the action is limited
		to set volume = capacity
		:param materials_containers:
		:param material:
		:return:
		"""
		
		"""
		=> This method fills the container for a specified material (~ingredient)
		It does not manage any ingredient refill packs therefore the action is limited
		to set volume = capacity
		:param material: indicates what material (ingredient) is to be filled
		:return: volume = container capacity if container exist otherwise volume = 0
		"""
		if material not in materials_containers:
			volume = 0
			print(
				f"\n===MaterialsContainersDispenser/refill_material_container=> {date_stamp()}"
				f" {material} does not have an associated container"
				f" Refill failed! - Volume = 0"
			)

		else:
			# the container exist so we set volume = capacity
			volume = materials_containers[material]['capacity']
			materials_containers[material]['volume'] = volume
			print(
				f"\n===MaterialsContainersDispenser/refill_material_container=> {date_stamp()}"
				f" {material} refilled to full capacity, namely: {volume}"
			)

		return volume

# ###################################################################################
# ## ===drink_distribution_business=> Accepted Coins Dispenser
# ###################################################################################

class AcceptedCoinsDispenser:
	"""
	=> This class is related to the payment of drinks with coins (no credit cards in this version)
	
	=> attributes:
		accepted coins with following structure:
		{coin_name string: coin_value float}
	
	=> Methods
		def add_accepted_coin(self, coin, value):
	
	"""
	
	def __init__(self):
		# Initialize coins dictionary
		self.accepted_coins = {}
	
	def add_accepted_coin(self, coin, value):
		# Check if the coin already exists
		if coin in self.accepted_coins:
			return False
		else:
			# Add the coin with the specified value
			self.accepted_coins[coin] = value
			return True


# ###################################################################################
# ## ===drink_distribution_business=> Drinks Menu
# ###################################################################################


class DrinksMenu:
	"""
	=> This class deals with the drink dispenser OFFER that clients can purchase
	
	=> attributes:
		drinks_menu is a dictionary with the following structure:
		{drink string: {'price': cost of the drink in float, 'command': keystrokes to order string}}
	
	=> method:
		def add_drink(self, drink, price, command):
	
	"""
	
	def __init__(self):
		# Initialize Drinks Menu
		self.drinks_menu = {}
	
	def add_drink(self, drink, price, command):
		"""
		=> This method adds a new drink to the drinks_menu (a new drink offer for the customer)
		
		:param drink:
		:param price:
		:param command:
		:return: True if drink added - False if drink already exists
		"""
		
		# Check if the drink already exists

		if drink in self.drinks_menu:
			return False
		
		else:
			
			# Add the drink with the specified price
			
			self.drinks_menu[drink] = {'price': price, 'command': command}
			return True

# ###################################################################################
# ## ===drink_distribution_business=> Drinks BOM - Drink composition
# ###################################################################################

class DrinksBom:
	"""
	=> This class manages the making of a particular drink, it relies on:
	the materials_containers (available ingredients)
	the drinks_menu : drinks to make
	
	=> attributes:
		bom is a dictionary with following structure
		{drink name (str): {material name (str): required volume (float), ....}}
		
	=> method:
		
		def add_drink_bom(self, drink, materials):
	
	"""
	
	def __init__(self, materials_containers, drinks_menu):
		self.bom = {}
		
		# Pass instances of MaterialsContainersDispenser and DrinksMenu
		self.materials_containers = materials_containers
		self.drinks_menu = drinks_menu

		
	def get_bom(self):
		"""
		=This method is just to grab the bom dictionary
		:return: bom : the bom dictionary
		"""
		return self.bom
	
	def add_drink_bom(self, drink, materials):
		"""
		=> This method enters the composition (ingredients and volumes) of a drink
		:param drink:  # must be a registered key of drinks_menu
		:param materials:
			# is a dictionary with ingredient as key and required volume as value
			# {"water": 200, "milk": 150, "coffee": 24}  is an example for latte
		:return: True if operation ok - False if operation failed
		"""
		# Check if the drink exists in the menu
		if drink not in self.drinks_menu:
			print(f"{drink} is not available in the drinks menu.")
			return False
		
		# Check if materials are compatible with materials_containers
		for material in materials:
			if material not in self.materials_containers:
				print(f"{material} is not available in the materials containers.")
				return False
		self.bom[drink] = materials
		return True
	


# ###################################################################################
# ## ===drink_distribution_business=> Drinks Business Operations
# ###################################################################################

class DrinksBusinessOperations:
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
		current_bom = self.drinks_bom.bom[drink]
		count_ok = 0
		for ingredient in self.drinks_bom.bom[drink]:
			availability = self.materials_dispenser.materials_containers[ingredient]['volume']
			required = self.drinks_bom.bom[drink][ingredient]
			if availability >= required:
				count_ok += 1
		if count_ok == len(current_bom):
			return True
		else:
			return False

	def update_drink_volume(self, drink):
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
					f" This should be considered as a dispenser program inconsistency"
				)
		if material_count == len(current_bom):
			return True
		else:
			return False

	
	def reset_revenue(self):
		self.business_cumulated_revenue = 0
		
	
	def add_revenue(self, amount):
		self.business_cumulated_revenue += amount
	

	
	def drink_checkout(self, drink):
		
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
			print(f" !!! Your selection is not recognized by the dispenser - Try again")
			user_drink = ''
		return user_drink
	
	def make_drink(self, drink):
		
		# we need now to remove the ingredients consumption of the drink
		return self.update_drink_volume(drink)

# ###################################################################################
# ## ===drink_distribution_business=> Drinks Business Maintenance
# ###################################################################################


class DrinksBusinessMaintenance:
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
		# 	f"\n variable control_command_keystroke: <{control_command_keystroke} "
		# )

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
		materials_volume = {}
		for material in self.materials_dispenser.materials_containers:
			volume = self.materials_dispenser.refill_material_container(material)
			materials_volume[material] = volume
		return materials_volume
		
		

print(f"\n===drink_distribution_business=> Classes/Methods Package <20240131-v06> @ {date_stamp()}")
