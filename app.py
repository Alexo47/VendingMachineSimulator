from flask import Flask, render_template, request, redirect, url_for, flash
from vending_machine.vending_machine import VendingMachine

app = Flask(__name__)
app.secret_key = 'your_secret_key'

materials_capacity = {"water": 1000, "milk": 300, "coffee": 60}
coin_values = {'Penny': 0.01, 'Nickel': 0.05, 'Dime': 0.10, 'Quarter': 0.25}
menu = {
    'expresso': {'price': 1.5, 'bom': {"water": 50, "milk": 0, "coffee": 18}, 'command': '/e'},
    'latte': {'price': 2.5, 'bom': {"water": 200, "milk": 150, "coffee": 24}, 'command': '/l'},
    'cappuccino': {'price': 3.0, 'bom': {"water": 250, "milk": 100, "coffee": 24}, 'command': '/c'}
}

vending_machine = VendingMachine(materials_capacity, coin_values, menu)

@app.route('/')
def index():
    available_drinks = [drink for drink in vending_machine.menu.get_drinks() if
                        vending_machine.check_availability(drink)]
    drink_availability = {drink: vending_machine.check_availability(drink) for drink in
                          vending_machine.menu.get_drinks()}
    return render_template('index.html', drinks=available_drinks, menu=menu,
                           coin_values=coin_values, drink_availability=drink_availability)

def safe_int(value, default=0):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

@app.route('/order/<drink>', methods=['GET', 'POST'])
def order(drink):
    if request.method == 'POST':
        payment = {coin: safe_int(request.form.get(coin)) for coin in coin_values}
        change = vending_machine.process_payment(drink, payment)
        if change is not None:
            vending_machine.make_drink(drink)
            flash(f'Drink {drink} made successfully. Change: ${change:.2f}', 'success')
        else:
            flash('Insufficient payment. Please try again.', 'danger')
        return redirect(url_for('index'))
    return render_template('order.html', drink=drink, price=menu[drink]['price'], coins=coin_values)

@app.route('/admin/refill')
def refill():
    vending_machine.refill()
    flash('All containers have been refilled.', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
