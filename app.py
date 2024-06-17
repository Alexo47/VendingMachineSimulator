import logging
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
# from flask_debugtoolbar import DebugToolbarExtension
from vending_machine.vending_machine import VendingMachine

# Assuming vending_machine_data.py is a Python file
from vending_machine.vending_machine_data import (
    materials_capacity,
    coin_values,
    menu,
    drink_price,
)

app = Flask(__name__)
app.config['DEBUG'] = True  # Set debug mode to True
app.secret_key = 'your_secret_key'
# toolbar = DebugToolbarExtension(app)

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

vending_machine = VendingMachine(materials_capacity, coin_values, menu, drink_price)

@app.route('/')
def index():


    # Log the menu
    logger.debug("Menu: %s", menu)
    logger.debug("Drink Prices: %s", drink_price)
    
    return render_template(
        'index.html',
        menu=menu,
        drink_price=drink_price,
        coin_values=coin_values
    )

def safe_int(value, default=0):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default



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
    available_drinks = [drink for drink in menu.keys() if vending_machine.check_availability(drink)]
    return jsonify({'available_drinks': available_drinks})

@app.route('/order/<drink>', methods=['POST'])
def order(drink):
    data = request.get_json()  # Assuming the request is JSON formatted
    payment = data.get('payment', 0)  # Extract payment from JSON data
    if drink in drink_price:
        price = drink_price[drink]
        if payment >= price:
            # Check if ingredients are available
            if vending_machine.check_availability(drink):
                change = payment - price
                vending_machine.make_drink(drink)
                return jsonify({'status': 'success', 'change': change, 'message': f'Drink {drink} made successfully. Change: ${change:.2f}'}), 200
            else:
                return jsonify({'status': 'error', 'message': 'Insufficient ingredients to make this drink.'}), 400
        else:
            return jsonify({'status': 'error', 'message': 'Insufficient payment. Please try again.'}), 400
    else:
        return jsonify({'status': 'error', 'message': 'Drink not found.'}), 404

@app.route('/admin/refill')
def refill():
    vending_machine.refill()
    flash('All containers have been refilled.', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
