def handler(request):
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/html"},
        "body": """
        <html>
        <head><title>Expense Tracker</title></head>
        <body>
            <h1>Welcome to Expense Tracker</h1>
            <p>This is a placeholder homepage. Please use the API endpoints for functionality.</p>
        </body>
        </html>
        """
    }
