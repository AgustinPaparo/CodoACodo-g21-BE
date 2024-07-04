from flask import Flask
from conf import init_app, get_db, create_table_properties
from .views import bp as views_bp
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

init_app(app)

# Crear tabla de propiedades al iniciar la aplicación
with app.app_context():
    create_table_properties()

from app import views
app.register_blueprint(views_bp)