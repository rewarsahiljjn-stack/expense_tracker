from flask import Flask, request, jsonify

def handler(request):
    if request.method == "GET":
        # Add your logic to fetch and return expenses here
        expenses = [
            {"id": 1, "category": "Food", "amount": 20, "date": "2023-01-01", "notes": "Lunch"},
            {"id": 2, "category": "Transport", "amount": 15, "date": "2023-01-02", "notes": "Bus fare"},
        ]
        return jsonify({"expenses": expenses})
    else:
        return jsonify({"message": "Method not allowed"}), 405
