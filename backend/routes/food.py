from flask import Blueprint, request, jsonify
from services.ollama_client import OllamaClient
from services.context_loader import ContextLoader

bp = Blueprint('food', __name__, url_prefix='/api/food')

@bp.route('/recommendations', methods=['POST'])
def get_food_recommendations():
    data = request.get_json()
    query = data.get('query', '')
    
    try:
        context_loader = ContextLoader()
        food_context = context_loader.load_context('food')
        
        client = OllamaClient()
        response = client.generate_response(query, 'food', food_context)
        
        return jsonify({'recommendations': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500