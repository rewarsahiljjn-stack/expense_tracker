from flask import Flask, request, jsonify

def handler(request):
    if request.method == "POST":
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        # Add your user registration logic here
        if username and password:
            return jsonify({"message": "User registered successfully"})
        else:
            return jsonify({"message": "Missing username or password"}), 400
    else:
        return jsonify({"message": "Method not allowed"}), 405
