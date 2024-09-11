from flask import Flask, jsonify, request
import requests
from flask_cors import CORS
import os
import hubspot
from hubspot.crm.contacts import SimplePublicObjectInput, ApiException
from hubspot.crm.contacts import Filter, FilterGroup

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv('SYSTEMEKEY')
BASE_API_URL = 'https://api.systeme.io/api/'

@app.route('/')
def index():
    return "Hello, World! This is the backend of the Astrocoders project. (And probably you shouldn't be here)"

@app.route('/create_contact', methods=['POST'])
def create_contact():
    # Obtiene los datos enviados desde el formulario en el frontend
    data = request.get_json()
    
    nombre = data.get('first_name')
    email = data.get('email')

    print(f"Nombre: {nombre}")
    print(f"Email: {email}")

    # Verificación simple de los datos
    if not nombre or not email:
        return jsonify({"error": "Nombre y email son requeridos"}), 400

    # Configuración de la API de systeme.io
    url = "https://api.systeme.io/api/contacts"
    payload = {
         "fields": [
        {
            "slug": "first_name",
            "value": nombre
        }
    ],
    "tags": [
        {
          "id": 1040049,
          "name": "Astrocoders Android"
        }
      ],
        "locale": "en",
        "email": email
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-API-Key": API_KEY
    }

    # Realiza la solicitud a la API de systeme.io
    response = requests.post(url, json=payload, headers=headers)

    # Maneja la respuesta
    if response.status_code == 201 or response.status_code == 200:
        # La API de systeme.io devuelve el contacto creado
        contact_data = response.json()
        contactId = contact_data.get('id')
        print(f"Contacto creado: {contactId}")
        addTag(contactId)

        return jsonify({"contact": contact_data}), 200
    else:
        # Si hay un error, devuelve un mensaje
        return jsonify({"error": "No se pudo crear el contacto"}), response.status_code
    
@app.route('/update_lead', methods=['POST'])
def update_lead():
     # Obtener el email de la solicitud
    email = request.json.get('email')

    if not email:
        return jsonify({"error": "Falta el email del lead"}), 400

    # Obtener el contact_id a partir del email
    contact = client.crm.contacts.basic_api.get_by_id(email, id_property='email')
    print(contact)
    contact_id = contact.id

    if not contact_id:
        return jsonify({"error": "No se encontró ningún contacto con ese email"}), 404

    # Definir las propiedades a actualizar
    properties = {
        "lifecyclestage": "840184806"
    }
    simple_public_object_input = SimplePublicObjectInput(properties=properties)

    try:
        # Intentar actualizar el contacto en HubSpot
        api_response = client.crm.contacts.basic_api.update(contact_id=contact_id, simple_public_object_input=simple_public_object_input)
        return jsonify({"message": "Lead actualizado correctamente", "contact_id": contact_id})
    except ApiException as e:
        # Si ocurre un error, devolver el mensaje de error
        return jsonify({"error": f"Excepción al llamar a la API: {e}"}), 500    

def addTag(contactId):
    url = f"https://api.systeme.io/api/contacts/{contactId}/tags"
    payload = { "tagId": 1040049 }
    headers = {
    "content-type": "application/json",
    "X-API-Key": API_KEY
}
    response = requests.post(url, json=payload, headers=headers)
    if(response.status_code == 204):
        print("Tag añadido")
    return response