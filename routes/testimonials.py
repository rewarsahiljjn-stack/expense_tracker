from flask import Blueprint, render_template

testimonials_bp = Blueprint('testimonials', __name__)

@testimonials_bp.route('/testimonials')
def testimonials():
    reviews = [
        {"name": "John Doe", "review": "This expense tracker has revolutionized how I manage my finances. Highly recommend!"},
        {"name": "Jane Smith", "review": "Easy to use and very intuitive. Saved me a lot of time."},
        {"name": "Mike Johnson", "review": "Great features and excellent support. Five stars!"},
        {"name": "Emily Davis", "review": "The dashboard is fantastic. Love the charts!"},
        {"name": "Chris Brown", "review": "Secure and reliable. Perfect for personal finance."},
        {"name": "Sarah Wilson", "review": "Import/export functionality is a game changer."},
        {"name": "David Lee", "review": "Clean UI and responsive design. Works great on mobile."},
        {"name": "Lisa Garcia", "review": "Helped me track expenses effortlessly. Thank you!"},
        {"name": "Tom Anderson", "review": "Best expense tracker I've used. Worth every penny."},
        {"name": "Anna Martinez", "review": "User-friendly and feature-rich. Highly satisfied."},
        {"name": "Robert Taylor", "review": "The analytics are spot on. Great insights."},
        {"name": "Maria Rodriguez", "review": "Simple yet powerful. My go-to app for expenses."}
    ]
    return render_template('testimonials.html', reviews=reviews)
