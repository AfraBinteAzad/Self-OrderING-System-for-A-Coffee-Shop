from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/order', methods=['POST'])
def order():
    data = request.get_json()
    coffee = data.get('coffee')
    return jsonify({'message': f'Thank you for ordering {coffee}!'})


@app.route('/cart')
def cart():
    return render_template('cart.html')


if __name__ == '__main__':
    app.run(debug=True)


