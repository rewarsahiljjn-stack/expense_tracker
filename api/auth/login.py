from flask import Flask, request, jsonify

def handler(request):
    if request.method == "POST":
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        # Add your authentication logic here
        if username == "admin" and password == "password":
            return jsonify({"message": "Login successful"})
        else:
            return jsonify({"message": "Invalid credentials"}), 401
    else:
        return jsonify({"message": "Method not allowed"}), 405
