from src.data_loader import ESGDataLoader
from src.llm_handler import OllamaHandler

class ESGRecommender:
    def __init__(self):
        self.data_loader = ESGDataLoader()
        self.llm_handler = OllamaHandler()
    
    def recommend(self, focus, industry, needs, objectives):
        """Main method to get ESG recommendations"""
        
        print("📁 Loading ESG framework data...")
        esg_context = self.data_loader.get_methods_context()
        
        # Prepare company info
        user_input = {
            'focus': focus,
            'industry': industry,
            'needs': needs,
            'objectives': objectives
        }
        
        # Get LLM recommendations
        recommendations = self.llm_handler.get_recommendations(user_input, esg_context)
        
        return recommendations