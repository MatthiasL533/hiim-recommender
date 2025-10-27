from src.data_loader import DataLoader
from src.llm_handler import OllamaHandler


class Recommender:
    def __init__(self):
        self.data_loader = DataLoader()
        self.llm_handler = OllamaHandler()

    def recommend(self, company_name, description, field, activities, hiim_requirements, purpose_goal):
        """Main method to get ESG recommendations"""

        print("📁 Loading ESG framework data...")
        hiim_context = self.data_loader.get_methods_context()

        # Prepare company info with all parameters
        company_info = {
            'name': company_name,
            'description': description,
            'field': field,
            'activities': activities,
            'ESG requirements': hiim_requirements,
            'Purpose/end goal': purpose_goal
        }
        recommendations = self.llm_handler.get_recommendations(company_info, hiim_context)

        return recommendations
