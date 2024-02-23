# !/usr/bin/env python
# coding: utf-8

"""
# u100d_coffee-machine - Object-Oriented Programming - 20240126-v1
> This program interacts with the user to undertake single database management tasks
> Tasks maybe:
1) create/delete a relation between nodes ( such as Company <=> Security
2) delete a single node record (Company, Security, or GICS)
3) Rename a single node record cia_name
4) remove expired securities
"""


# ###################################################################################
# ## ===u100d_coffee-machine=> Import Modules
# ###################################################################################
from Modules.modgen_timestamp import date_stamp
from vending_machine_simulator import MaterialsContainersDispenser
from vending_machine_simulator import AcceptedCoinsDispenser
from vending_machine_simulator import DrinksMenu
from vending_machine_simulator import DrinksBom
from vending_machine_simulator import VendingMachineOperations
from vending_machine_simulator import DrinksBusinessMaintenance
import time
import os
import sys



# ###################################################################################
# ## ===u100d_coffee-machine=> Local Variables
# ###################################################################################

ITD2_DRINKS = ["expresso", "latte", "cappuccino"]
ITD2_INGREDIENTS = ["water", "milk", "coffee"]
ITD2_MATERIALS_DISPENSER_CAPACITY = {"water": 300, "milk": 200, "coffee": 100}
ITD2_ACCEPTED_COINS = {'Penny': 0.01, 'Nickel': 0.05, 'Dime': 0.10, 'Quarter': 0.25}
ITD2_ADMIN_COMMANDS = {
	'/?': 'print container operations',
	'/r': 'containers refill',
	'/s': 'shut down ordered_drink dispenser'
}

ERROR_CODES = {
	"dispenser shut down ordered": 0,
	"material_container_refill_failure": 10,
	"operations_status not recognizable - program failure": 90,
	"admin_commands inconsistency - addition failed": 91,
	"make ordered_drink failed - unable to update materials_dispenser volumes": 92
}

# ###################################################################################
# ## ===u100d_coffee-machine=> Vending Machine Operations Local Routines
# ###################################################################################
"""
	This "section'" manages customer orders, payment checkout, making the drink takeout ingredients
	
	attributes:
	
	methods:
		def check_drink_availability(self, drink):
		def ask_user_drink(self):
		def drink_checkout(self, ordered_drink):
		def make_drink(self, ordered_drink):
		
	external methods activated:
		drinks_menu.exist_drink
		drinks_menu.get_drink_price
		drinks_menu.get_drink_bom
		materials_dispenser.exist_material_container
		materials_dispenser.get_volume_material_container
		accepted_coins.get_all_coins
		accepted_coins.get_coin_value

"""

def check_drink_availability(ordered_drink: str) -> bool:
	"""
	Checks if all ingredients are available to make the ordered_drink
	:param ordered_drink:
	:return: True if the ordered_drink can be made False otherwise

	external methods activated:
		drinks_menu.exist_drink
		drinks_menu.get_drink_bom
		materials_dispenser.exist_material_container
		materials_dispenser.get_volume_material_container

	"""
	count_ok = 0
	
	if drinks_menu.exist_drink(ordered_drink):
		drink_bom = drinks_menu.get_drink_bom(ordered_drink)
		for ingr in drink_bom:
			vol_required = drink_bom[ingr]
			if self.materials_dispenser.exist_material_container(ingr):
				# The ingredient has a container in the dispenser - check volume
				
				vol_available = self.materials_dispenser.get_volume_material_container(ingr)
				if vol_available >= vol_required:
					count_ok += 1
		
		if count_ok == len(drink_bom):
			return True
	return False


def ask_user_drink(self):
	"""
	Scans the Drinks Menu - If drink can be made displays menu choice: price & command
	:return:

	external methods activated:
		drinks_menu.get_all_drinks
		drinks_menu.exist_drink
		drinks_menu.get_drink_price
		drinks_menu.get_drink_command
		materials_dispenser.exist_material_container
		materials_dispenser.get_volume_material_container
	"""
	
	drinks_in_menu = self.drinks_menu.get_all_drinks()
	for drink in drinks_in_menu:
		if self.check_drink_availability(drink):
			drink_price = self.drinks_menu.get_drink_price(drink)
			drink_command = self.drinks_menu.get_drink_command(drink)
			print(
				f"Want {drink} for {drink_price} US$?"
				f"then type: {drink_command}"
			)
	user_choice = input("So what is your choice? =?> ")
	print(f"\n===vending_machine_simulator=> You ordered {user_choice}")
	for drink in drinks_in_menu:
		drink_command = self.drinks_menu.get_drink_command(drink)
		if user_choice == drink_command:
			return drink
	# user choice unrecognizable
	drink = '#'
	return drink


def drink_checkout(self, ordered_drink):
	"""

	:param ordered_drink:
	:return:

	external methods activated:
		drinks_menu.get_drink_price
		accepted_coins.get_all_coins
		accepted_coins.get_coin_value

	"""
	
	drink_price = self.drinks_menu.get_drink_price(ordered_drink)
	current_payment = 0
	coins_accepted = self.accepted_coins.get_all_coins()
	for coin in coins_accepted:
		number_coins = int(input(f" <{coin}> : How many?"))
		coin_value = self.accepted_coins.get_coin_value(coin)
		current_payment += coin_value * number_coins
		if drink_price <= current_payment:
			change = current_payment - drink_price
			print(f" You are all set for your <{ordered_drink}> and your change is <{change}>")
			return True
	
	# at this level the user introduced an insufficient amount to pay for his ordered_drink
	change = current_payment
	print(
		f" {current_payment} is insufficient for your"
		f"<{ordered_drink}> that costs: <{drink_price}"
		f" Here is your change: {change}"
	)
	return False


def make_drink(self, ordered_drink):
	"""
	Drink consumption requires ingredients, this method reduces volume accordingly to drink_bom
	:param ordered_drink:
	:return:

	external methods activated:
		drinks_menu.exist_drink
		drinks_menu.get_drink_price
		drinks_menu.get_drink_bom
		materials_dispenser.exist_material_container
		materials_dispenser.takeout_material_container
	"""
	if self.drinks_menu.exist_drink(ordered_drink):
		drink_bom = self.drinks_menu.get_drink_bom(ordered_drink)
		for ingr in drink_bom:
			vol_required = drink_bom[ingr]
			if self.materials_dispenser.exist_material_container(ingr):
				# The ingredient has a container in the dispenser - check volume
				new_volume = self.materials_dispenser.takeout_material_container(
					ingr, vol_required
				)
				if new_volume < 0:  # program error make_drink should not have been activated
					return False
		return True
	return False


# ###################################################################################
# ## ===vending_machine_simulator=> Drinks Business Maintenance Local Routines
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
		self.materials_dispenser.materials_containers = materials_dispenser.materials_containers
	
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


# ###################################################################################
# ## ===u100d_coffee-machine=> Initialize Objects
# ###################################################################################


# ########## Instantiate Materials Dispenser ##########



itd2_materials_dispenser = MaterialsContainersDispenser()
for material in ITD2_MATERIALS_DISPENSER_CAPACITY:
	dispenser_capacity = ITD2_MATERIALS_DISPENSER_CAPACITY[material]
	mat_flag = itd2_materials_dispenser.allocate_material_container(
		material,
		dispenser_capacity
	)
	if not mat_flag:
		print(
			f"\n======u100d_coffee-machine/materials_dispenser/instantiate=> {date_stamp()}"
			f" : Addition of {material} container failed"
		)
	else:
		print(
			f"\n======u100d_coffee-machine/materials_dispenser/instantiate> {date_stamp()}"
			f" : {material} container capacity of {ITD2_MATERIALS_DISPENSER_CAPACITY[material]}"
			f" ADDED successfully"
		)

# ########## Instantiate Cash Dispenser ##########

itd2_accepted_coins = AcceptedCoinsDispenser()
for coin in ITD2_ACCEPTED_COINS:
	coin_value = ITD2_ACCEPTED_COINS[coin]
	coin_flag = itd2_accepted_coins.add_accepted_coin(
		coin,
		coin_value
	)
	if not coin_flag:
		print(
			f"\n======u100d_coffee-machine/coins_dispenser/instantiate=> {date_stamp()}"
			f" : Addition of {coin} container failed"
		)
	else:
		print(
			f"\n======u100d_coffee-machine/coins_dispenser/instantiate=> {date_stamp()}"
			f" : {coin} container for {ITD2_ACCEPTED_COINS[coin]} US$ Coins "
			f" ADDED successfully"
		)

# ########## Instantiate Drink Menu ##########

ITD2_DRINKS_MENU = {
	'expresso': {'price': 1.5, 'command': '/e'},
	'latte': {'price': 2.5, 'command': '/l'},
	'cappuccino': {'price': 3.0, 'command': '/c'}
}


itd2_drinks_menu = DrinksMenu()
for drink in ITD2_DRINKS_MENU:
	drink_price = ITD2_DRINKS_MENU[drink]['price']
	drink_command = ITD2_DRINKS_MENU[drink]['command']
	drink_flag = itd2_drinks_menu.add_drink(
		drink,
		drink_price,
		drink_command
	)
	if not drink_flag:
		print(
			f"\n======u100d_coffee-machine/DrinkMenu/instantiate=> {date_stamp()}"
			f" : Addition of {drink} container failed"
		)
	else:
		print(
			f"\n======u100d_coffee-machine/DrinkMenu/instantiate=> {date_stamp()}"
			f" : {drink} Menu with price {drink_price} US$ amd command {drink_command}"
			f" ADDED successfully"
		)

	
# ########## Instantiate ITD2_DRINKS_BOM ##########

ITD2_DRINKS_BOM = {
	"expresso": {"water": 50, "milk": 0, "coffee": 18},
	"latte": {"water": 200, "milk": 150, "coffee": 24},
	"cappuccino": {"water": 250, "milk": 100, "coffee": 24}
}

itd2_drinks_bom = DrinksBom(
	itd2_materials_dispenser.materials_containers,
	itd2_drinks_menu.drinks_menu
)
for drink in ITD2_DRINKS_BOM:
	drink_bom = ITD2_DRINKS_BOM[drink]
	bom_flag = itd2_drinks_bom.add_drink_bom(
		drink,
		drink_bom
	)
	if not bom_flag:
		print(
			f"\n======u100d_coffee-machine/DrinksBom/instantiate=> {date_stamp()}"
			f" : Addition of {drink_bom} Bill of Materials failed"
		)
	else:
		print(
			f"\n======u100d_coffee-machine/DrinksBom/instantiate=> {date_stamp()}"
			f" : {drink} with the following BOM ingredients {drink_bom} "
			f" ADDED successfully"
		)

# ########## Instantiate ITD2_DRINKS_BUSINESS Operations ##########

itd2_accumulated_revenue = 0

itd2_drink_dispenser_business = VendingMachineOperations(
	itd2_materials_dispenser,
	itd2_drinks_bom,
	itd2_drinks_menu,
	itd2_accepted_coins,
	itd2_accumulated_revenue
)

# ########## Instantiate Drink ITD2_DRINKS_BUSINESS Maintenance ##########

itd2_admin_commands = DrinksBusinessMaintenance(itd2_materials_dispenser.materials_containers)
new_command = {}
for admin_command in ITD2_ADMIN_COMMANDS:
	new_command = {}
	new_command[admin_command] = ITD2_ADMIN_COMMANDS[admin_command]
	
	admin_command_flag = itd2_admin_commands.add_admin_command(
		new_command
	)
	
	if not admin_command_flag:
		error_message = 'admin_commands inconsistency - addition failed'
		error_code = ERROR_CODES[error_message]
		print(
			f"\n======u100d_coffee-machine/MaintenanceOperations/instantiate=> {date_stamp()}"
			f"\n Addition of {admin_command} command failed"
			f"\n This is another programming inconsistency"
			f" Program exit {error_message} raised {error_code} "
		)


# ###################################################################################
# ## ===u100d_coffee-machine=> Local Routines
# ###################################################################################



def clear_terminal():
	print(f" Finishing execution of last order")
	time.sleep(5)
	os.system('cls')
	
def set_timer(seconds):
	print(f"Timer set for {seconds} seconds.")
	time.sleep(seconds)
	print("Timer expired!")


# ###################################################################################
# ## ===u100d_coffee-machine=> Business Launch Initialization
# ###################################################################################

# ########## Refill the Materials Dispenser Containers ##########

for material in itd2_materials_dispenser.materials_containers:
	material_container_capacity = itd2_materials_dispenser.refill_material_container(
		itd2_materials_dispenser.materials_containers,
		material
	)
	
	if material_container_capacity == 0:
		error_message = 'material_container_refill_failure'
		error_code = ERROR_CODES[error_message]
		
		print(
			f"\n======u100d_coffee-machine/BusinessLaunch/SetupOperations=> {date_stamp()}"
			f" : {material} refill was unsuccessful - Launch Operations Aborted"
			f"{error_message} - raising error code <{error_code}>"
			f" Dispenser needs Maintenance Intervention"
		)

		sys.exit(error_code)
	else:
		print(
			f"\n======u100d_coffee-machine/BusinessLaunch/SetupOperations=> {date_stamp()}"
			f"\n{material} successful refill to capacity, volume = {material_container_capacity}"
		)
		
# we need now to initiate accounting operations

itd2_drink_dispenser_business.reset_revenue()

# Initially the dispenser is full so there is at least one ordered_drink to offer
one_drink = True
operations = 'running'



# ###################################################################################
# ## ===u100d_coffee-machine=> Loop Engine
# ###################################################################################

while operations != 'shutdown':
	
	# ########## Initializing New Cycle - Local Variables Setup ##########
	
	clear_terminal()
	current_drink_availability = {}
	drinks_available_count = 0
	
	# ########## Check Drinks Availability - Check Dispensers Fills ##########
	
	
	for drink in itd2_drinks_menu.drinks_menu:

		drink_flag = itd2_drink_dispenser_business.check_drink_availability(
			drink
		)
		if drink_flag:
			drinks_available_count += 1
		current_drink_availability[drink] = drink_flag
	
	print(
		f"\n===u100d_coffee-machine=> Current drinks availability at {date_stamp()}"
		f" {current_drink_availability}"
		)
	
	# ########## Check if Maintenance Required ##########
	
	if drinks_available_count >= 1:
		one_drink = True
		operations = 'running'
	else:
		one_drink = False
		operations = 'maintenance'  # Maintenance Intervention Required


	# ########## Request User Selection ##########
	if operations == 'running':
		print(f"\n===u100d_coffee-machine=> Welcome to the ITD2 Drink Dispenser")
		print(f"\n Below the following drinks you can select at this time {date_stamp()} ")

		for drink in itd2_drinks_menu.drinks_menu:
			if current_drink_availability[drink]:
				print(
					f" Want {drink} for {itd2_drinks_menu.drinks_menu[drink]['price']} US$?"
					f" => type {itd2_drinks_menu.drinks_menu[drink]['command']}"
				)
		user_prompt = "So what is your choice? "
		user_choice = input(user_prompt)
		print(f"\n===u100d_coffee-machine=> You ordered {user_choice}")
		
		# ########## Process User Selection ##########
		user_selection = False  # flag used to validate user_choice
		
		for drink in itd2_drinks_menu.drinks_menu:
			if user_choice == itd2_drinks_menu.drinks_menu[drink]['command']:
				selected_drink = drink
				user_selection = True
				if current_drink_availability[selected_drink]:
					drink_price = itd2_drinks_menu.drinks_menu[selected_drink]['price']
					payment, change_back = itd2_drink_dispenser_business.drink_checkout(
						selected_drink
					)
					if payment:
						print(
							f"\n===u100d_coffee-machine/checkout-order SUCCESSFUL"
							f"\n Here is your ordered ordered_drink <{selected_drink}>"
							f"\n Here is your change: {change_back}"
							f" Enjoy your {drink} - Thanks for using our services - Till soon"
						)
					# ########## Process Coffee Making ##########
						if not itd2_drink_dispenser_business.make_drink(drink):
							error_message = (
								f"make ordered_drink failed - unable to update materials_dispenser volumes"
							)
							error_code = ERROR_CODES[error_message]
							print(
								f"\n===u100d_coffee-machine/make_order UNSUCCESSFUL"
								f"\n Something fishy occurred with your <{selected_drink}>"
								f"\n {error_message} with <{error_code}> "
								f"\n Program shutdown triggered!"
							)
							sys.exit(error_code)
						else:
							time.sleep(10)  # coffee being filled
						
					else:
						print(
							f"\n===u100d_coffee-machine/checkout-order UNSUCCESSFUL"
							f"\n Insufficient payment for your ordered ordered_drink <{selected_drink}>"
							f"\n Payed {change_back} but your ordered_drink costs {drink_price}"
							f"\n Here is your refund: {change_back} - Till soon!"
						)
				else:
					print(
						f"\n===u100d_coffee-machine/checkout-order UNSUCCESSFUL"
						f"\n Your <{user_choice}> is not available at this moment"
					)

		
		if not user_selection:
			print(
				f"\n===u100d_coffee-machine/user_selection=> ORDER NOT RECOGNIZED"
				f"\n Please select only the drinks available that are displayed on the screen"
			)

	elif operations == 'maintenance':
		print(f"\n===u100d_coffee-machine=> ITD2 Drink Dispenser NO DRINKS AVAILABLE")
		print(
			f"\n If you are a Drink Dispenser Admin put your id-key - after that you can: "
		)
		for admin_command in itd2_admin_commands.admin_maintenance_commands:
			admin_command_message = itd2_admin_commands.admin_maintenance_commands[admin_command]
			print(
				f"For {admin_command_message} type {admin_command}"
			)
		admin_prompt = f"\n So what kind of maintenance you want to do?"
		admin_choice = input(admin_prompt)
		print(f"\n===u100d_coffee-machine/MaintenanceOperation=> Your command {admin_choice}")
		
		# ########## Process Admin Selection ##########
		user_selection = False
		if admin_choice in itd2_admin_commands.admin_maintenance_commands:
			user_selection = True
			
			if admin_choice == '/?':  # Admin wants a Status Report
				itd2_admin_commands.report_containers_levels()
				
			elif admin_choice == '/r':  # Admin want to refill all containers
				
				materials_containers_volume = itd2_admin_commands.refill_all_containers()

				for material in materials_containers_volume:
					volume = materials_containers_volume[material]
					if volume == 0:
						# we are in trouble the dispenser lacks basic materials to refill
						print(
							f"\n===u100d_coffee-machine/Maintenance=> Refill UNSUCCESSFUL"
							f"\n Material Dispenser cannot be refilled for {material}"
							f"\n This invalidates Drink Business Operations"
							f"\n Shut Down Exit automatically triggered"
						)
						operations = 'shutdown'
						error_message = 'material_container_refill_failure'
						error_code = ERROR_CODES[error_message]
						sys.exit(error_code)
			else:
				# admin_choice = '/s' - Admin wants to shut down the ordered_drink dispenser
				operations = 'shutdown'
				
		else:
			# Admin Command not recognized by the system
			print(
				f"\n===u100d_coffee-machine/Maintenance/AdminCommand=> @ {date_stamp()}"
				f"\n Your command <{admin_choice}> was not recognized"
				f"\n Please select only the commands that are displayed on the screen"
			)
	
			
	elif operations == 'shut down':
		error_message = "dispenser shut down ordered"
		error_code = ERROR_CODES[error_message]
		sys.exit(error_code)
	
	else:
		error_message = 'operations status not recognizable - program failure'
		error_code = ERROR_CODES[error_message]
		print(f"\n===u100d_coffee-machine=> {operations} {error_message}")
		print(
			f"\n Program will shut down with error_code: {error_code}"
		)
		sys.exit(error_code)

		
print(f"\n===u100d_coffee-machine=> <20240126-v1> exec@: {date_stamp()}")
