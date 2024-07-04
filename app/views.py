from flask import Blueprint, request, jsonify
from conf import *
from .models import Property


bp = Blueprint("views", __name__)


@bp.route("/", methods=["GET"])
def index():
    test_connection()
    return jsonify({"mensaje": "Pagina inicio BACKEND - CodoACodo 2024 Grupo N°21"})


@bp.route("/api/properties", methods=["GET"])
def all_properties():
    """Trae todas las propiedades"""

    propiedades = Property.get_all_properties()
    serialized_properties = [p.serialize() for p in propiedades]

    return serialized_properties


@bp.route("/api/new_property", methods=["POST"])
def new_property():
    """Ingresa una nueva propidad a la DB"""

    data = request.json

    new_property = Property(
        propietario_id=data["propietario_id"],
        direccion=data["direccion"],
        tipo=data["tipo"],
        habitaciones=data["habitaciones"],
        banos=data["banos"],
        tamano=data["tamano"],
        cochera=data["cochera"],
        precio=data["precio"],
        estado=data["estado"],
        tipo_contrato=data["tipo_contrato"],
        imagenes= [],
    )

    try:
        new_property.save()
    except Exception as e:
        print(e)
        return jsonify({"error": e}), 415

    return jsonify({"message": "Task created successfully"}), 201


@bp.route("/api/update_property/<int:prop_id>", methods=["PUT"])
def update_property(prop_id):
    """Actualiza una propiedad según su ID"""

    property = Property.get_property_by_id(prop_id)

    if not property:
        return jsonify({"message": "Property not found"}), 404

    data = request.json

    property.propietario_id = data["propietario_id"],
    property.direccion = data["direccion"],
    property.tipo = data["tipo"],
    property.habitaciones = data["habitaciones"],
    property.banos = data["banos"],
    property.tamano = data["tamano"],
    property.cochera = data["cochera"],
    property.precio = data["precio"],
    property.estado = data["estado"],
    property.tipo_contrato = data["tipo_contrato"],
    property.imagenes = data["imagenes"]

    property.save()

    return jsonify({"message": "Property updated successfully"})


@bp.route("/api/get_property/<int:prop_id>", methods=["GET"])
def get_property(prop_id=None):
    """Devuelve una propiedad segun su ID"""

    if prop_id is not None:
        property = Property.get_property_by_id(prop_id)

    prop2json = jsonify(property.serialize())

    return prop2json


@bp.route("/api/delete_property/<int:prop_id>", methods=["DELETE"])
def delete_property(prop_id):
    """ Elimina una propiedad de la db segun su ID """

    property = Property.get_property_by_id(prop_id)
    if not property:
        return jsonify({'message': 'Property not found'}), 404

    property.delete()
    return jsonify({'message': 'Property deleted successfully'})