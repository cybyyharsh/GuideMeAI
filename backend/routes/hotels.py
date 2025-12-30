from flask import Blueprint, request, jsonify
from services.ollama_client import OllamaClient
from services.context_loader import ContextLoader

bp = Blueprint('hotels', __name__, url_prefix='/api/hotels')

@bp.route('/search', methods=['POST'])
def search_hotels():
    data = request.get_json()
    query = data.get('query', '')
    
    try:
        context_loader = ContextLoader()
        hotels_context = context_loader.load_context('hotels')
        
        client = OllamaClient()
        response = client.generate_response(query, 'hotels', hotels_context)
        
        return jsonify({'hotels': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500