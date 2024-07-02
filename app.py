from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import logging
from vending_machine.vending_machine import VendingMachine
from vending_machine.vending_machine_data import materials_capacity, coin_values, menu, drink_price
from vending_machine.vending_machine_data import vending_machine_states, vending_machine_current_state

import time

app = Flask(__name__)
app.config['DEBUG'] = True  # Set debug mode to True
app.secret_key = 'your_secret_key'

# Configure Flask-Session
from flask_session import Session
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_KEY_PREFIX'] = 'vending_machine_'
Session(app)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

vending_machine = VendingMachine(
    materials_capacity,
    coin_values,
    menu,
    drink_price,
    vending_machine_states,
    vending_machine_current_state
)

# Refill the vending machine on server start
vending_machine.refill()

@app.route('/')
def index():
    logger.debug("===app-route.index=> Activated !")
    logger.debug("Menu: %s", menu)
    logger.debug("Drink Prices: %s", drink_price)

    return render_template(
        'index.html',
        menu=menu,
        drink_price=drink_price,
        coin_values=coin_values,
        current_state=vending_machine.get_state(),  # Ensure current state is passed
        possible_states=vending_machine_states
    )

@app.route('/make_drink', methods=['POST'])
def make_drink():
    data = request.json
    drink = data.get('drink')

    logger.debug(f"===app-route.make_drink=> Activated with drink: {drink}")

    if not drink:
        logger.debug("No drink specified")
        return jsonify({'status': 'error', 'message': 'No drink specified'}), 400

    current_time = time.time()
    last_request_time = session.get('last_make_drink_request_time', 0)
    debounce_interval = 2  # 2 seconds debounce interval

    if current_time - last_request_time < debounce_interval:
        logger.debug("Duplicate request detected within debounce interval")
        return jsonify({'status': 'error', 'message': 'Duplicate request detected'}), 400

    session['last_make_drink_request_time'] = current_time

    if vending_machine.check_availability(drink):
        logger.debug(f"===app-route.make_drink=> check_availability confirms {drink} is makeable")
        logger.debug(f"===app-route.make_drink=> ACTIVATING vending_machine.MAKE_DRINK method ")
        if vending_machine.make_drink(drink):
            logger.debug(f"===app-route.make_drink=> vending_machine.make_drink confirms {drink} ONGOING")
            return jsonify({'status': 'success', 'message': f'{drink.capitalize()} is being made'})
        else:
            logger.debug(f"===app-route.make_drink=> vending_machine.make_drink states {drink} NOT_OK")
            return jsonify({'status': 'error', 'message': 'Error making drink'}), 500
    else:
        logger.debug(f"===app-route.make_drink=> check_availability states {drink} NOT MAKEABLE")
        return jsonify({'status': 'error', 'message': 'Insufficient ingredients'}), 400

@app.route('/check_drink_availability', methods=['GET'])
def check_drink_availability():
    available_drinks = [drink for drink in menu.keys() if vending_machine.check_availability(drink)]
    logger.debug(f"===app-route.check_drink_availability => Available drinks: {available_drinks}")
    return jsonify(
        {'available_drinks': available_drinks, 'current_state': vending_machine.get_state()})

@app.route('/admin/refill')
def refill():
    logger.debug("===app-route.admin-refill => Refill ACTIVATED")
    vending_machine.refill()
    vending_machine.current_state = vending_machine_states[0]  # Set to 'in_operation'
    flash('All containers have been refilled.', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
