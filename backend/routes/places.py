from flask import Blueprint, request, jsonify
from services.ollama_client import OllamaClient
from services.context_loader import ContextLoader

bp = Blueprint('places', __name__, url_prefix='/api/places')

@bp.route('/discover', methods=['POST'])
def discover_places():
    data = request.get_json()
    query = data.get('query', '')
    
    try:
        context_loader = ContextLoader()
        places_context = context_loader.load_context('places')
        
        client = OllamaClient()
        response = client.generate_response(query, 'places', places_context)
        
        return jsonify({'places': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500