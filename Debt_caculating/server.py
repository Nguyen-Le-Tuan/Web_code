from flask import Flask, request, jsonify, render_template
from collections import defaultdict

app = Flask(__name__)

debts = defaultdict(lambda: defaultdict(int))

@app.route('/')
def home():
    return render_template('index.html', debts=debts)

@app.route('/add_debt', methods=['POST'])
def add_debt():
    data = request.json
    debtor = data['debtor']
    creditor = data['creditor']
    amount = data['amount']
    
    debts[debtor][creditor] += amount
    return jsonify({"message": "Debt recorded."})

@app.route('/simplify_debts', methods=['GET'])
def simplify_debts():
    simplified = {}
    for debtor in debts:
        for creditor, amount in debts[debtor].items():
            if amount > 0:
                for indirect in debts:
                    if indirect != debtor and debts[creditor].get(indirect, 0) > 0:
                        min_amount = min(amount, debts[creditor][indirect])
                        debts[debtor][indirect] += min_amount
                        debts[debtor][creditor] -= min_amount
                        debts[creditor][indirect] -= min_amount
    
    for debtor, creditors in debts.items():
        simplified[debtor] = {c: a for c, a in creditors.items() if a > 0}
    
    return jsonify(simplified)

@app.route('/get_debts', methods=['GET'])
def get_debts():
    return jsonify(debts)

@app.route('/initialize_sample_debts', methods=['POST'])
def initialize_sample_debts():
    sample_debts = [
        ("A", "B", 10000),
        ("B", "C", 15000),
        ("C", "D", 20000),
        ("D", "E", 25000),
        ("E", "F", 30000),
        ("F", "A", 35000)
    ]
    for debtor, creditor, amount in sample_debts:
        debts[debtor][creditor] += amount
    return jsonify({"message": "Sample debts initialized."})

if __name__ == '__main__':
    app.run(debug=True)
