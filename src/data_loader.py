import pandas as pd
import os

class DataLoader:
    def __init__(self, data_path="data/csv_impactmeasurement_repo.csv"):
        self.data_path = data_path
        self.hiim_data = None
    
    def load_data(self):
        """Load methods data from semicolon-separated CSV"""
        try:
            # Read CSV with semicolon separator
            self.hiim_data = pd.read_csv(self.data_path, sep=';', encoding='utf-8')
            print(f"✅ Loaded {len(self.hiim_data)} ESG impact measurement methods")
            print(f"📊 Dataset contains {len(self.hiim_data.columns)} columns")
            return self.hiim_data
        except FileNotFoundError:
            print(f"❌ Error: CSV file not found at {self.data_path}")
            return None
        except Exception as e:
            print(f"❌ Error loading data: {str(e)}")
            return None
    
    def get_methods_context(self):
        """Format methods for LLM context"""
        if self.hiim_data is None:
            self.load_data()
        
        if self.hiim_data is None:
            return "No data available"
        
        context = "AVAILABLE ESG IMPACT MEASUREMENT METHODS:\n\n"
        
        for _, row in self.hiim_data.iterrows():
            # Get method name (handle potential NaN values)
            method_name = row.get('method name', 'Unknown Method')
            if pd.isna(method_name):
                method_name = 'Unknown Method'
            
            # Get description
            description = row.get('description', 'No description available')
            if pd.isna(description):
                description = 'No description available'
            
            # Get developer
            developer = row.get('developer', 'Unknown Developer')
            if pd.isna(developer):
                developer = 'Unknown Developer'
            
            # Get release year
            release_year = row.get('release year', 'Unknown')
            if pd.isna(release_year):
                release_year = 'Unknown'
            
            # Get latest version
            latest_version = row.get('latest version', 'Unknown')
            if pd.isna(latest_version):
                latest_version = 'Unknown'
            
            # Get tool support
            tool_support = row.get('tool support', 'Not specified')
            if pd.isna(tool_support):
                tool_support = 'Not specified'
            
            # Get impact score if available
            impact_score = row.get('impactscore (max12)', 'Not rated')
            if pd.isna(impact_score):
                impact_score = 'Not rated'
            
            context += f"Method: {method_name}\n"
            context += f"Developer: {developer}\n"
            context += f"Release Year: {release_year}\n"
            context += f"Latest Version: {latest_version}\n"
            context += f"Tool Support: {tool_support}\n"
            context += f"Impact Score: {impact_score}\n"
            context += f"Description: {description[:200]}{'...' if len(str(description)) > 200 else ''}\n"
            context += "─" * 50 + "\n\n"
        
        return context
    
    def get_method_by_name(self, method_name):
        """Get specific method details by name"""
        if self.hiim_data is None:
            self.load_data()
        
        if self.hiim_data is None:
            return None
        
        # Search for method by name (case insensitive)
        method_row = self.hiim_data[
            self.hiim_data['method name'].str.contains(method_name, case=False, na=False)
        ]
        
        if len(method_row) > 0:
            return method_row.iloc[0].to_dict()
        return None
    
    def get_methods_by_scope(self, scope_type):
        """Get methods that include specific scope (Ethical, Social, Environmental, Economic)"""
        if self.hiim_data is None:
            self.load_data()
        
        if self.hiim_data is None:
            return None
        
        scope_column = f"scope_{scope_type}"
        if scope_column in self.hiim_data.columns:
            methods = self.hiim_data[
                self.hiim_data[scope_column].str.contains("Is included", case=False, na=False)
            ]
            return methods
        return None
    
    def get_data_summary(self):
        """Get summary statistics about the dataset"""
        if self.hiim_data is None:
            self.load_data()
        
        if self.hiim_data is None:
            return "No data available"
        
        summary = {
            'total_methods': len(self.hiim_data),
            'columns': len(self.hiim_data.columns),
            'developers': self.hiim_data['developer'].nunique() if 'developer' in self.hiim_data.columns else 0,
            'release_years': self.hiim_data['release year'].nunique() if 'release year' in self.hiim_data.columns else 0
        }
        
        return summary