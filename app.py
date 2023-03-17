from cpsim_app.extensions import app, db
from cpsim_app.routes import main
from cpsim_app.routes import auth
from flask import Flask, request, redirect, render_template, url_for, jsonify

app.register_blueprint(main)
app.register_blueprint(auth)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

