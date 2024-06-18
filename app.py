from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import logging
from vending_machine.vending_machine import VendingMachine
from vending_machine.vending_machine_data import materials_capacity, coin_values, menu, drink_price

app = Flask(__name__)
app.config['DEBUG'] = True  # Set debug mode to True
app.secret_key = 'your_secret_key'

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

vending_machine = VendingMachine(materials_capacity, coin_values, menu, drink_price)

# Refill the vending machine on server start
vending_machine.refill()


@app.route('/')
def index():
	logger.debug("Menu: %s", menu)
	logger.debug("Drink Prices: %s", drink_price)
	
	maintenance_message = None
	
	# Check if any drinks are available
	if vending_machine.check_maintenance():
		maintenance_message = 'No drinks available - Maintenance required'
	
	return render_template(
		'index.html',
		menu=menu,
		drink_price=drink_price,
		coin_values=coin_values,
		maintenance_message=maintenance_message
	)


@app.route('/make_drink', methods=['POST'])
def make_drink():
	data = request.json
	drink = data.get('drink')
	
	if not drink:
		return jsonify({'status': 'error', 'message': 'No drink specified'}), 400
	
	if vending_machine.make_drink(drink):
		return jsonify({'status': 'success', 'message': f'{drink.capitalize()} is being made'})
	else:
		return jsonify({'status': 'error', 'message': 'Insufficient ingredients'}), 400


@app.route('/check_drink_availability', methods=['GET'])
def check_drink_availability():
	if vending_machine.check_maintenance():
		return jsonify(
			{'maintenance': True, 'message': 'No drinks ! - Maintenance required'})
	
	available_drinks = [drink for drink in menu.keys() if vending_machine.check_availability(drink)]
	return jsonify({'available_drinks': available_drinks, 'maintenance': False})


# Other routes remain the same as previously defined

if __name__ == '__main__':
	app.run(debug=True)
