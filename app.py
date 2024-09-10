from flask import Flask, jsonify, request
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

API_KEY = 'ucih8jttqu1cnbozmwgaeazeci1mmfuxzw9pcl126frcnpihot2069hpitrp9yjv'
BASE_API_URL = 'https://api.systeme.io/api/'

# Ruta para obtener contactos (ya existente)
@app.route('/get_contacts', methods=['GET'])
def get_contacts():
    headers = {
        'X-API-Key': API_KEY
    }
    try:
        response = requests.get(BASE_API_URL + 'contacts', headers=headers)
        
        rate_limit = response.headers.get('X-RateLimit-Limit')
        remaining_requests = response.headers.get('X-RateLimit-Remaining')
        refill_time = response.headers.get('X-RateLimit-Refill')

        print(f"Límite de solicitudes: {rate_limit}")
        print(f"Solicitudes restantes: {remaining_requests}")
        print(f"Tiempo para recargar las solicitudes: {refill_time}")

        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/create_contact', methods=['POST'])
def create_contact():
    # Obtiene los datos enviados desde el formulario en el frontend
    data = request.get_json()
    
    nombre = data.get('nombre')
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
        "X-API-Key": "ucih8jttqu1cnbozmwgaeazeci1mmfuxzw9pcl126frcnpihot2069hpitrp9yjv"  # Reemplaza con tu API Key
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
    

def addTag(contactId):
    url = f"https://api.systeme.io/api/contacts/{contactId}/tags"
    payload = { "tagId": 1040049 }
    headers = {
    "content-type": "application/json",
    "X-API-Key": "ucih8jttqu1cnbozmwgaeazeci1mmfuxzw9pcl126frcnpihot2069hpitrp9yjv"
}
    response = requests.post(url, json=payload, headers=headers)
    if(response.status_code == 204):
        print("Tag añadido")
    return response