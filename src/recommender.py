from src.data_loader import ESGDataLoader
from src.llm_handler import OllamaHandler


class ESGRecommender:
    def __init__(self):
        self.data_loader = ESGDataLoader()
        self.llm_handler = OllamaHandler()

    def recommend(self, company_name, description, field, activities, esg_requirements, purpose_goal):
        """Main method to get ESG recommendations"""

        print("📁 Loading ESG framework data...")
        esg_context = self.data_loader.get_methods_context()

        # Prepare company info with all parameters
        company_info = {
            'name': company_name,
            'description': description,
            'field': field,
            'activities': activities,
            'ESG requirements': esg_requirements,
            'Purpose/end goal': purpose_goal
        }
        recommendations = self.llm_handler.get_recommendations(company_info, esg_context)

        return recommendations