# !/usr/bin/env python
# coding: utf-8

"""
# u100d_coffee-machine - 20240115-v1
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
import time
import os

# ###################################################################################
# ## ===u100d_coffee-machine=> Variables & Constants
# ###################################################################################

"""
"""

ITD2_INGREDIENTS = ["water", "milk", "coffee"]
ITD2_ACCEPTED_COINS = ["Penny", "Nickel", "Dime", "Quarter"]
ITD2_DRINKS = ["expresso", "latte", "cappuccino"]
ITD2_ACCEPTED_COINS_VALUES = {
	"Penny": 0.01,
	"Nickel": 0.05,
	"Dime": 0.10,
	"Quarter": 0.25
}

ITD2_DRINKS_BOM = {
	"expresso": {"water": 50, "milk": 0, "coffee": 18},
	"latte": {"water": 200, "milk": 150, "coffee": 24},
	"cappuccino": {"water": 250, "milk": 100, "coffee": 24}
}
dispenser_prices = {
	"expresso": 1.5,
	"latte": 2.5,
	"cappuccino": 3
}

DRINK_SELECTION = {
	"/e": 'expresso',
	"/l": 'latte',
	"/c": 'cappuccino'
}

current_drink_availability = {}


# current_dispenser_resource = {}

# ###################################################################################
# ## ===u100d_coffee-machine=> Local Routines
# ###################################################################################



def clear_terminal():
	print(f" Finishing execution of last order")
	time.sleep(5)
	os.system('cls')

def dispenser_refill_ingredients():
	"""
	=> This routine fills coins_dispenser resources at maximum capacity
	:return: current_resource: dictionary with ingredients filled
	"""
	dispenser_resources_capacity = {
		"water": 300,
		"milk": 200,
		"coffee": 100
	}
	current_resource = {}
	global ITD2_INGREDIENTS
	for resource in INGREDIENTS:
		current_resource[resource] = dispenser_resources_capacity[resource]
	return current_resource


def update_dispenser_container(user_drink):
	global ITD2_INGREDIENTS
	global ITD2_DRINKS
	global ITD2_DRINKS_BOM
	global current_dispenser_resource
	# user_drink_bom = {}
	user_drink_bom = BOM[user_drink]
	"""
	print(
		f"\n===update_dispenser_container> BEFORE UPDATE ordered_drink: {user_drink}"
		f"coins_dispenser contains: \n{current_dispenser_resource}"
	)
	"""
	for res in INGREDIENTS:
		if current_dispenser_resource[res] >= user_drink_bom[res]:
			current_dispenser_resource[res] -= user_drink_bom[res]
		else:
			current_dispenser_resource[res] = 0
	"""
	print(
		f"\n===update_dispenser_container> AFTER UPDATE ordered_drink: {user_drink}"
		f" coins_dispenser contains: \n{current_dispenser_resource}"
	)
	"""
	return


def dispenser_check_availability():
	"""
	
	:return:
	"""
	availability = {}
	just_one_drink = False
	global ITD2_INGREDIENTS
	global ITD2_DRINKS
	global ITD2_DRINKS_BOM
	global current_dispenser_resource
	for drink in DRINKS:
		count_ok = 0
		availability[drink] = False
		for res in INGREDIENTS:
			drink_bom = BOM[drink]
			required = drink_bom[res]
			available = current_dispenser_resource[res]
			if available >= required:
				count_ok += 1
		if count_ok == len(INGREDIENTS):
			availability[drink] = True
			just_one_drink = True
	
	return availability, just_one_drink


def sum_coins(coins):
	amount = 0
	global ITD2_ACCEPTED_COINS
	global ITD2_ACCEPTED_COINS_VALUES
	for coin in ACCEPTED_COINS:
		amount = amount + int(coins[coin]) * COINS_VALUES[coin]
	return amount


def checkout_drink(drink):
	global dispenser_prices
	drink_price = dispenser_prices[drink]
	coins_entered = {}
	print(f"\n You selected {drink} that costs {drink_price} US$")
	for coin in ITD2_ACCEPTED_COINS:
		number_coins = input(f"How many {coin} do you have?")
		coins_entered[coin] = number_coins
	print(coins_entered)
	total_payed = sum_coins(coins_entered)
	if total_payed >= drink_price:
		payok = True
		change = total_payed - drink_price
	else:
		payok = False
		change = total_payed
	
	return payok, change


# ###################################################################################
# ## ===u100d_coffee-machine=> Initialization
# ###################################################################################
# we need first to refill the coins_dispenser ingredients


current_dispenser_resource = dispenser_refill_ingredients()
one_drink = True  # Initially the coins_dispenser is full so there is at least one ordered_drink to offer
# print(current_dispenser_resource)

# ###################################################################################
# ## ===u100d_coffee-machine=> Loop Engine
# ###################################################################################

while one_drink:
	# Call the function to clear the terminal
	current_drink_availability, one_drink = dispenser_check_availability()
	# print(f"\n===u100d_coffee-machine=> Current drinks availability: {current_drink_availability}")
	
	# ###################################################################################
	print(f"\n Welcome to the Python Drink Dispenser")
	print(f"\n Below the following actions you can undertake at this time {date_stamp()} ")
	print(f"If you have Admin authorisation you can launch a coins_dispenser refill by typing /r ")
	
	for my_drink in ITD2_DRINKS:
		if current_drink_availability[my_drink]:
			print(f"Want {my_drink} for {dispenser_prices[my_drink]} US$? => type /{my_drink[0]}")
	prompt1 = "So what is your choice? =?> "
	user_choice = input(prompt1)
	print(f"\n===u100d_coffee-machine=> You ordered {user_choice}")
	if user_choice in DRINK_SELECTION:
		selected_drink = DRINK_SELECTION[user_choice]
		if current_drink_availability[selected_drink]:
			payment, change_back = checkout_drink(selected_drink)
			if payment:
				print(f"\n Here is your ordered ordered_drink <{selected_drink}>")
				print(f"\n Here is your change <{change_back}>")
				print(f"\n Many thanks for using our services - Till soon!")
				update_dispenser_container(selected_drink)
			else:
				print(f"\n Insufficient payment for your ordered ordered_drink <{selected_drink}>")
				print(f"\n Payed {change_back} but your ordered_drink costs {dispenser_prices[selected_drink]}")
				print(f"\n Here is your payment back - Till soon!")
		else:
			print(
				f"\n Sorry, but {selected_drink} is not available at this time"
				f"\n Please select only the drinks available that are displayed on the screen"
			)
	else:
		print(
			f"\n Sorry, but {user_choice} is not a recognized command"
			f"\n Select the drinks available displayed on the screen with the proper command"
		)

	clear_terminal()
		
print(f"\n Urgent Python Drink Dispenser is Empty!!")
print(f"Waiting for MAINTENANCE to launch a coins_dispenser refill")

print(f"\n===u100d_coffee-machine=> <20240115-v1> exec@: {date_stamp()}")
