# !/usr/bin/env python
# coding: utf-8

"""
# Vending_machine_simulator - Object-Oriented Programming - 20240225-v2

"""


# ###################################################################################
# ## ===vending_machine_simulator=> Import Modules
# ###################################################################################
import time
import os
import sys
from modgen_timestamp import date_stamp
from vending_machine_simulator import MaterialsContainersDispenser
from vending_machine_simulator import AcceptedCoinsDispenser
from vending_machine_simulator import DrinksMenu
from vending_machine_simulator import VendingMachineFinancials

# ###################################################################################
# ## ===vending_machine_simulator=> ITD2 Business Operations Parameters
# ###################################################################################

ITD2_INGREDIENTS = ["water", "milk", "coffee"]
ITD2_MATERIALS_DISPENSER_CAPACITY = {"water": 1000, "milk": 300, "coffee": 60}
ITD2_ACCEPTED_COINS = {'Penny': 0.01, 'Nickel': 0.05, 'Dime': 0.10, 'Quarter': 0.25}

ITD2_MENU = {
	'expresso': {
		'price': 1.5,
		'bom': {"water": 50, "milk": 0, "coffee": 18},
		'command': '/e'
	},
	'late': {
		'price': 1.0,
		'bom': {"water": 200, "milk": 150, "coffee": 24},
		'command': '/l'
	},
	'cappuccino': {
		'price': 3.0,
		'bom': {"water": 250, "milk": 100, "coffee": 24},
		'command': '/c'
	
	}
}

itd2_admin_commands = {
	'/r': "Report containers current volume",
	'/f': "Refill containers to full capacity",
	'/a': "Add new maintenance command"
}



ERROR_CODES = {
	"dispenser shut down ordered": 0,
	"material_container_refill_failure": 90,
	"operations_status not recognizable - program failure": 91,
	"admin_commands inconsistency - addition failed": 92,
	"make drink_order failed - unable to update materials_dispenser volumes": 93,
	"program inconsistency - drink available but not enough materials": 94
}



# ###################################################################################
# ## ===vending_machine_simulator=> Initialize Objects
# ###################################################################################


# ########## Instantiate Materials Dispenser ##########

itd2_materials = MaterialsContainersDispenser()

for material, dispenser_capacity in ITD2_MATERIALS_DISPENSER_CAPACITY.items():
	mat_flag = itd2_materials.allocate_material_container(
		material,
		dispenser_capacity
	)
	if not mat_flag:
		print(
			f"\n======vms/materials_dispenser/instantiate=> {date_stamp()}"
			f" : Addition of {material} container failed"
		)
	else:
		print(
			f" \n======vms/materials_dispenser/instantiate> {date_stamp()}"
			f" {material} container capacity of {dispenser_capacity}"
			f" ADDED successfully"
		)

# ########## Instantiate Cash Dispenser ##########

itd2_coins = AcceptedCoinsDispenser()

for coin, coin_value in ITD2_ACCEPTED_COINS.items():
	coin_flag = itd2_coins.add_accepted_coins(
		coin,
		coin_value
	)
	if not coin_flag:
		print(
			f"\n======vms/coins_dispenser/instantiate=> {date_stamp()}"
			f" : Addition of {coin} container failed"
		)
	else:
		print(
			f"\n======vms/coins_dispenser/instantiate=> {date_stamp()}"
			f" : {coin} container for {coin_value} US$ Coins "
			f" ADDED successfully"
		)

# ########## Instantiate Drink Menu ##########
	
itd2_menu = DrinksMenu()


for drink in ITD2_MENU.keys():
	drink_price = ITD2_MENU[drink]['price']
	drink_bom = ITD2_MENU[drink]['bom']
	drink_command = ITD2_MENU[drink]['command']
	if itd2_menu.add_drink(drink, drink_price, drink_bom, drink_command):
		print(
			f"\n======vms/DrinkMenu/instantiate=> {date_stamp()}"
			f" : {drink} Menu with price {drink_price} US$ and command {drink_command}"
			f" ADDED successfully"
		)
	else:
		print(
			f"\n======vms/DrinkMenu/instantiate=> {date_stamp()}"
			f" : Addition of {drink} container failed"
		)


# ########## Instantiate ITD2_DRINKS_BUSINESS Financials ##########

itd2_finance = VendingMachineFinancials()

itd2_finance.reset_revenue()



# ###################################################################################
# ## ===vending_machine_simulator=> Vending Machine Operations Local Routines
# ###################################################################################
"""
	This "section'" manages customer orders, payment checkout, making the drink takeout ingredients
	
	attributes:
	
	methods:
		def check_drink_availability(self, drink):
		def ask_user_drink(self):
		def drink_checkout(self, drink_order):
		def make_drink(self, drink_order):
		
	external methods activated:
		drinks_menu.exist_drink
		drinks_menu.get_drink_price
		drinks_menu.get_drink_bom
		materials_dispenser.exist_material_container
		materials_dispenser.get_volume_material_container
		accepted_coins.get_all_coins
		accepted_coins.get_coin_value

"""

def check_drink_availability(drink_order: str) -> bool:
	"""
	Checks if all ingredients are available to make the drink_order
	:param drink_order:
	:return: True if the drink_order can be made False otherwise

	external methods activated:
		drinks_menu.exist_drink
		drinks_menu.get_drink_bom
		materials_dispenser.exist_material_container
		materials_dispenser.get_volume_material_container

	"""
	count_ok = 0
	
	if itd2_menu.exist_drink(drink_order):
		ordered_drink_bom = itd2_menu.get_drink_bom(drink_order)
		for ingredient in ordered_drink_bom:
			vol_required = ordered_drink_bom[ingredient]
			if itd2_materials.exist_material_container(ingredient):
				# The ingredient has a container in the dispenser - check volume
				
				vol_available = itd2_materials.get_volume_material_container(ingredient)
				if vol_available >= vol_required:
					count_ok += 1
	
		return count_ok == len(ordered_drink_bom)
	return False

	



def ask_user_drink():
	"""
	Scans the Drinks Menu - If drink can be made displays menu choice: price & command
	:return selecting_drink:
	:return drinks_available:

	external methods activated:
		drinks_menu.get_all_drinks
		drinks_menu.exist_drink
		drinks_menu.get_drink_price
		drinks_menu.get_drink_command
		materials_dispenser.exist_material_container
		materials_dispenser.get_volume_material_container
	"""
	print(f"\n===vms=> Welcome to the ITD2 Drink Dispenser")
	print(f"\n Below the following drinks you can select at this time {date_stamp()} ")

	drinks_in_menu = itd2_menu.get_all_drinks()
	drinks_available = False
	for this_drink in drinks_in_menu:
		if check_drink_availability(this_drink):
			drinks_available = True
			this_drink_price = itd2_menu.get_drink_price(this_drink)
			this_drink_command = itd2_menu.get_drink_command(this_drink)
			print(
				f"Want {this_drink} for {this_drink_price} US$?"
				f"then type: {this_drink_command}"
			)
	if drinks_available:
		user_drink_choice = input("So what is your choice? =?> ")
		print(f"\n===vms/ask_user_drink=> You entered command {user_drink_choice}")
		for selecting_drink in drinks_in_menu:
			user_drink_command = itd2_menu.get_drink_command(selecting_drink)
			if user_drink_choice == user_drink_command:
				return selecting_drink, drinks_available

	else:
		selecting_drink = '#'
		return selecting_drink, drinks_available


def drink_checkout(drink_order):
	"""

	:param drink_order:
	:return:

	external methods activated:
		drinks_menu.get_drink_price
		accepted_coins.get_all_coins
		accepted_coins.get_coin_value

	"""
	
	ordered_drink_price = itd2_menu.get_drink_price(drink_order)
	current_payment = 0
	coins_accepted = itd2_coins.get_all_coins()
	for one_coin in coins_accepted:
		number_coins = int(input(f" <{one_coin}> : How many?"))
		one_coin_value = itd2_coins.get_coin_value(one_coin)
		current_payment += one_coin_value * number_coins
		if ordered_drink_price <= current_payment:
			change = current_payment - ordered_drink_price
			print(
				f"\n===vms/drink_checkout=> You are all set for your <{drink_order}> "
				f"and your change is <{change}>"
			)
			return change, True
	
	# at this level the user introduced an insufficient amount to pay for his drink_order
	change = - current_payment
	print(
		f"\n===vms/drink_checkout=> {current_payment:.2f} is insufficient for your"
		f"<{drink_order}> that costs: <{ordered_drink_price}"
		f" Here is your change: {change:.2f}"
	)
	return change, False


def make_drink(drink_order):
	"""
	Drink consumption requires ingredients, this method reduces volume accordingly to drink_bom
	:param drink_order:
	:return:

	external methods activated:
		drinks_menu.exist_drink
		drinks_menu.get_drink_price
		drinks_menu.get_drink_bom
		materials_dispenser.exist_material_container
		materials_dispenser.takeout_material_container
	"""
	if itd2_menu.exist_drink(drink_order):
		ordered_drink_bom = itd2_menu.get_drink_bom(drink_order)
		for ingredient in ordered_drink_bom:
			vol_required = ordered_drink_bom[ingredient]
			if itd2_materials.exist_material_container(ingredient):
				# The ingredient has a container in the dispenser - check volume
				new_volume = itd2_materials.takeout_material_container(
					ingredient, vol_required
				)
				if new_volume < 0:  # program error make_drink should not have been activated
					return material, False
		return '#', True
	return '#', False


# ###################################################################################
# ## ===vending_machine_simulator=> Drinks Business Maintenance Local Routines
# ###################################################################################

	
def add_admin_command(control_command: str, control_message: str):
	"""
	
	:param control_command: 
	:param control_message: 
	:return: 
	"""
	# control_command_keystroke, control_command_message = list(control_command.items())[0]
	# print(
	# 	f"\n===DrinksBusinessMaintenance/add_admin_command=> @ {date_stamp()}"
	# 	f"\n parameter control_command: <{control_command}>"
	# 	f"\n variable control_command_keystroke: <{control_command_keystroke} ")
	
	for command in itd2_admin_commands:
		if command == control_command:
			print(
				f"\n===vms/add_admin_command=> {date_stamp()}"
				f"{control_command} already available in the admin commands list"
			)
			return False
	itd2_admin_commands[control_command] = control_message
	return True
	
def report_containers_levels():
	"""

	:return:
	"""
	
	print(
		f"At this point of time: {date_stamp()}"
		f"The Containers are in the following status:"
	)
	materials = itd2_materials.get_all_materials()
	for one_material in materials:
		material_capacity = itd2_materials.get_capacity_material_container(one_material)
		material_volume = itd2_materials.get_volume_material_container(one_material)

		print(
			f" Container of: <{one_material}> with total capacity of {material_capacity}"
			f" is currently filled at {material_volume} level"
		)
	
def refill_all_containers():
	"""

	:return:
	"""
	all_materials = itd2_materials.get_all_materials()
	materials_volume = {}
	for specific_material in all_materials:
		specific_volume = itd2_materials.refill_material_container(specific_material)
		materials_volume[specific_material] = specific_volume
	return materials_volume




# ###################################################################################
# ## ===vending_machine_simulator=> Local Routines
# ###################################################################################



def clear_terminal():
	"""
	
	:return:
	"""
	print(f"\n===vms/clear_terminal=> Clearing Panel")
	time.sleep(1)
	os.system('cls')
	
def set_timer(seconds):
	"""
	
	:param seconds:
	:return:
	"""
	print(f"Timer set for {seconds} seconds.")
	time.sleep(seconds)
	print("Timer expired!")

def print_program_error(source: str,error_message: str) -> int :
	error_code = ERROR_CODES[error_message]
	print(
		f" \n {source} - {date_stamp()}"
		f" \n {error_message} - Raising error Code {error_code}"
	)
	return error_code
	
	
# ###################################################################################
# ## ===vending_machine_simulator=> Business Launch Initialization
# ###################################################################################

"""
=> Local Attributes:
	itd2_materials = MaterialsContainersDispenser()
	itd2_coins = AcceptedCoinsDispenser()
	itd2_menu = DrinksMenu()
	itd2_finance = VendingMachineFinancials()
	itd2_admin_commands
	
"""

# ########## Refill the Materials Dispenser Containers ##########

for material in itd2_materials.materials_containers:
	if itd2_materials.refill_material_container(material):
		material_volume = itd2_materials.get_volume_material_container(material)
		print(
			f"\n======vms/BusinessLaunch/SetupOperations=> {date_stamp()}"
			f"\n{material} successful refill to capacity, volume = {material_volume}"
		)
	
	else:
		ERROR_MESSAGE = 'material_container_refill_failure'
		error_anchor = '====vms/BusinessLaunch/SetupOperations=>'
		error_code = print_program_error(error_anchor, ERROR_MESSAGE)
	
		sys.exit(error_code)

		
# we need now to initiate accounting operations

itd2_finance.reset_revenue()

operations = 'running'



# ###################################################################################
# ## ===vending_machine_simulator=> Loop Engine
# ###################################################################################

while operations != 'shutdown':
	
	# ########## Initializing New Cycle - Local Variables Setup ##########
	
	clear_terminal()
	
	
	# ########## Request User Selection ##########
	if operations == 'running':
		ordered_drink, drink_availability_flag = ask_user_drink()
		if drink_availability_flag:
			if ordered_drink == '#':
				# invalid user choice
				print(f"\n===vms=> Your order is invalid - Please reorder drink")
				continue
	
			print(f"\n===vms=> You ordered {ordered_drink}")
			change_back, checkout_flag = drink_checkout(ordered_drink)
			if checkout_flag:
				print(
					f"\n===vms/checkout-{ordered_drink} SUCCESSFUL"
					f"\n Here is your change: {change_back}"
				)
				
				make_material, make_flag = make_drink(ordered_drink)
				if make_flag:
					print(
						f"\n===vms=> Making drink {ordered_drink} - Please wait"
					)
					time.sleep(4)  # coffee being filled
					print(
						f"\n===vms=> Drink {ordered_drink}) is ready - Enjoy!"
					)
					continue
		
				# Big trouble the drink was considered available but not enough material to make it
				print(
					f"\n===vms=> Big Trouble - Make {ordered_drink} failed"
					f"\n As we cannot make your drink your payment {change_back} is available below"
				)
				ERROR_MESSAGE = 'material_container_refill_failure'
				error_anchor = '===vms/MakeOrder=>'
				error_code = print_program_error(error_anchor, ERROR_MESSAGE)
				operations = 'shutdown'
				sys.exit(error_code)
				
		else:  # There are no more drinks available to sell - Maintenance required
			print(
				f"\n===vms/engine=> Maintenance operations triggered"
				f"- NO DRINKS AVAILABLE in ITD2-VMS"
				f"\n If you are a Drink Dispenser Admin put your id-key to enable admin commands"
			)
			operations = 'maintenance'
			continue
		

	elif operations == 'maintenance':

		for admin_command, admin_command_message in itd2_admin_commands.items():
			print(
				f"For {admin_command_message} type {admin_command}"
			)
		admin_prompt = f"\n So what kind of maintenance you want to do?"
		admin_choice = input(admin_prompt)
		print(f"\n===vms/MaintenanceOperation=> Your command {admin_choice}")
		
		# ########## Process Admin Selection ##########
		user_selection = False
		if admin_choice in itd2_admin_commands:
			user_selection = True
			
			if admin_choice == '/r':  # Admin wants a Status Report
				report_containers_levels()
				time.sleep(3)
			elif admin_choice == '/f':  # Admin want to refill all containers
				
				materials_containers_volume = refill_all_containers()

				for material, volume in materials_containers_volume.items():
					if volume == 0:
						error_anchor = '===vms/Maintenance=>'
						ERROR_MESSAGE = f"{material} container_refill_failure - Shut Down Triggered"
						error_code = print_program_error(error_anchor, ERROR_MESSAGE)
						operations = 'shutdown'
						sys.exit(error_code)

			else:
				# admin_choice = '/s' - Admin wants to shut down the drink_order dispenser
				print(
					f"\n===vms/Maintenance/AdminCommand=> @ {date_stamp()}"
					f"\n Shut Down command triggered by administrator"
				)
				operations = 'shutdown'
				
		else:
			# Admin Command not recognized by the system
			print(
				f"\n===vms/Maintenance/AdminCommand=> @ {date_stamp()}"
				f"\n Your command <{admin_choice}> was not recognized"
				f"\n Please select only the commands that are displayed on the screen"
			)
	
			
	elif operations == 'shut down':
		error_anchor = f"===vms/maintenance=>  @ {date_stamp()}"
		ERROR_MESSAGE = "dispenser shut down ordered"
		error_code = print_program_error(error_anchor, ERROR_MESSAGE)
		sys.exit(error_code)
	
	else:
		ERROR_MESSAGE = 'operations status not recognizable - program failure'
		error_anchor = f"===vms/engine=>  @ {date_stamp()}"
		error_code = print_program_error(error_anchor, ERROR_MESSAGE)
		sys.exit(error_code)

		
print(f"\n===vending_machine_simulator=> <20240225-v2> exec@: {date_stamp()}")
