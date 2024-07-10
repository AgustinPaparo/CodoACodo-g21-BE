from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from conf import *
from .models import Property
from .utils import delete_from_github, upload_photos_to_github


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
    
    formatted_direccion = property.direccion.replace(" ", "_")
    directory_name = f"{property.propietario_id}-{formatted_direccion}"
    
    for image_path in property.imagenes:
        try:
            path = f'{directory_name}/{image_path.strip()}'
            delete_from_github(path)
        except Exception as e:
            print(path)
            print(e)
            return jsonify({'message': f'Error deleting image from GitHub: {str(e)}'}), 500

    property.delete()
    return jsonify({'message': 'Property deleted successfully'})


@bp.route("/api/new_property", methods=["POST"])
def new_property():
    propietario_id = request.form['propietario_id']
    direccion = request.form['direccion']
    tipo = request.form['tipo']
    habitaciones = request.form['habitaciones']
    banos = request.form['banos']
    tamano = request.form['tamano']
    cochera = request.form.get('cochera') == 'true'
    precio = request.form['precio']
    estado = request.form['estado']
    tipo_contrato = request.form['tipo_contrato']

    photos = request.files.getlist('photos')
    
    # enviar las fotos a que le cambie el nombre y luego las almacene en github
    try:
        array_photos_path = upload_photos_to_github(photos, propietario_id, direccion)
    except Exception as e:
        return jsonify({"message": str(e)}), 500

    new_property = Property(
        propietario_id=propietario_id,
        direccion=direccion,
        tipo=tipo,
        habitaciones=habitaciones,
        banos=banos,
        tamano=tamano,
        cochera=cochera,
        precio=precio,
        estado=estado,
        tipo_contrato=tipo_contrato,
        imagenes= array_photos_path,
    )

    try:
        new_property.save()
    except Exception as e:
        print(e)
        return jsonify({"error": e}), 415


    return jsonify({"message": "Task created successfully"}), 201


