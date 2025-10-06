import pandas as pd
import os

class ESGDataLoader:
    def __init__(self, data_path="data/esg_methods.csv"):
        self.data_path = data_path
        self.esg_data = None
    
    def load_data(self):
        """Load ESG methods data from CSV"""
        try:
            self.esg_data = pd.read_csv(self.data_path)
            print(f"✅ Loaded {len(self.esg_data)} ESG methods")
            return self.esg_data
        except FileNotFoundError:
            print(f"❌ Error: CSV file not found at {self.data_path}")
            return None
    
    def get_methods_context(self):
        """Format ESG methods for LLM context"""
        if self.esg_data is None:
            self.load_data()
        
        context = "AVAILABLE ESG REPORTING METHODS:\n\n"
        for _, row in self.esg_data.iterrows():
            context += f"Method: {row['method_name']}\n"
            context += f"Description: {row['description']}\n"
            context += f"Framework Type: {row['framework_type']}\n"
            context += f"Applicable Industries: {row['applicability_industries']}\n"
            context += f"Difficulty: {row['difficulty_level']}\n"
            context += f"Focus Areas: {row['focus_areas']}\n"
            context += "─" * 50 + "\n\n"
        
        return context