from flask import Flask, request, jsonify

def handler(request):
    if request.method == "POST":
        data = request.get_json()
        category = data.get("category")
        amount = data.get("amount")
        date = data.get("date")
        notes = data.get("notes", "")
        # Add your logic to add expense here
        if category and amount and date:
            return jsonify({"message": "Expense added successfully"})
        else:
            return jsonify({"message": "Missing required fields"}), 400
    else:
        return jsonify({"message": "Method not allowed"}), 405
