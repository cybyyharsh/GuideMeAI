from flask import Blueprint, request, jsonify
from services.ollama_client import OllamaClient
from services.context_loader import ContextLoader

bp = Blueprint('traffic', __name__, url_prefix='/api/traffic')

@bp.route('/info', methods=['POST'])
def get_traffic_info():
    data = request.get_json()
    query = data.get('query', '')
    
    try:
        context_loader = ContextLoader()
        traffic_context = context_loader.load_context('traffic')
        
        client = OllamaClient()
        response = client.generate_response(query, 'traffic', traffic_context)
        
        return jsonify({'traffic_info': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500