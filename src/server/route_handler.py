# 📍 src/server/route_handler.py

from flask import render_template
from app import app

@app.route('/admin')
def admin_page():
    return render_template('admin.html')

@app.route('/client')
def client_page():
    return render_template('client.html')
v