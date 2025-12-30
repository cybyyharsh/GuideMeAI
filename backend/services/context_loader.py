import os

class ContextLoader:
    def __init__(self):
        self.context_dir = os.path.join(os.path.dirname(__file__), '..', 'context')
    
    def load_context(self, context_type):
        """Load context information from markdown files"""
        context_file = os.path.join(self.context_dir, f"{context_type}.md")
        
        try:
            with open(context_file, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return f"No specific context available for {context_type}"
        except Exception as e:
            return f"Error loading context: {str(e)}"
    
    def load_city_profile(self):
        """Load general city profile information"""
        return self.load_context('city_profile')