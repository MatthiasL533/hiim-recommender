import ollama
import json
import re

class OllamaHandler:
    def __init__(self, model_name="llama2:7b"):
        self.model_name = model_name
        self.client = ollama.Client()
        
    def get_recommendations(self, company_info, esg_context):
        """Get structured ESG recommendations using Ollama"""
        
        prompt = self._build_structured_prompt(company_info, esg_context)
        
        try:
            print("🤖 Generating recommendations with Ollama...")
            response = self.client.generate(
                model=self.model_name,
                prompt=prompt,
                options={
                    'temperature': 0.1,  # Low temperature for consistent output
                    'num_predict': 600,  # Increased token limit for JSON
                    'top_k': 40,
                    'top_p': 0.9
                }
            )
            
            return self._parse_and_format_response(response['response'])
            
        except Exception as e:
            return f"❌ Error: {str(e)}\n\nPlease ensure Ollama is running and the model '{self.model_name}' is installed."
    
    def _build_structured_prompt(self, company_info, esg_context):
        """Build a prompt that forces structured JSON output"""
        
        return f"""You are an expert ESG (Environmental, Social, Governance) reporting consultant. 
Analyze the following company and recommend the most suitable ESG reporting frameworks from the available options.

COMPANY ANALYSIS:
- Company Name: {company_info['name']}
- Industry/Field: {company_info['field']}
- Company Description: {company_info['description']}
- Key Activities: {company_info['activities']}

{esg_context}

INSTRUCTIONS:
1. Analyze the company's industry, activities, and characteristics
2. Match against the available ESG frameworks' applicability, focus areas, and difficulty
3. Select the TOP 3 most suitable frameworks
4. Return your response as VALID JSON only

CRITERIA FOR MATCHING:
- Industry alignment
- Company size and complexity
- Focus area relevance
- Implementation difficulty
- Stakeholder expectations

RETURN STRICT JSON FORMAT (no other text):
{{
  "company_analysis": "Brief analysis of company's ESG needs",
  "recommendations": [
    {{
      "rank": 1,
      "method_name": "Exact method name from available options",
      "fit_score": "High/Medium/Low",
      "justification": "Detailed explanation of why this framework fits",
      "key_benefits": ["Benefit 1", "Benefit 2", "Benefit 3"],
      "implementation_tips": ["Tip 1", "Tip 2"]
    }},
    {{
      "rank": 2,
      "method_name": "Exact method name from available options", 
      "fit_score": "High/Medium/Low",
      "justification": "Detailed explanation of why this framework fits",
      "key_benefits": ["Benefit 1", "Benefit 2", "Benefit 3"],
      "implementation_tips": ["Tip 1", "Tip 2"]
    }},
    {{
      "rank": 3,
      "method_name": "Exact method name from available options",
      "fit_score": "High/Medium/Low", 
      "justification": "Detailed explanation of why this framework fits",
      "key_benefits": ["Benefit 1", "Benefit 2", "Benefit 3"],
      "implementation_tips": ["Tip 1", "Tip 2"]
    }}
  ]
}}

IMPORTANT: Use only the exact method names provided in the available options."""
    
    def _parse_and_format_response(self, response):
        """Parse the LLM response and format it nicely"""
        
        # Try to extract JSON from the response
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        
        if not json_match:
            return self._format_fallback_response(response)
        
        try:
            data = json.loads(json_match.group())
            return self._format_structured_recommendations(data)
        except json.JSONDecodeError:
            return self._format_fallback_response(response)
    
    def _format_structured_recommendations(self, data):
        """Format the structured data into a nice readable output"""
        
        formatted = "🚀 ESG REPORTING RECOMMENDATIONS\n"
        formatted += "=" * 60 + "\n\n"
        
        # Company analysis
        formatted += "📊 COMPANY ANALYSIS:\n"
        formatted += f"{data.get('company_analysis', 'Analysis not provided')}\n\n"
        
        formatted += "🏆 TOP 3 RECOMMENDED FRAMEWORKS:\n"
        formatted += "=" * 60 + "\n\n"
        
        # Recommendations
        for rec in data.get('recommendations', []):
            rank = rec.get('rank', 'N/A')
            method = rec.get('method_name', 'Unknown Method')
            fit_score = rec.get('fit_score', 'Unknown')
            justification = rec.get('justification', '')
            
            formatted += f"#{rank} {method} ({fit_score} Fit)\n"
            formatted += f"📋 Why it fits: {justification}\n\n"
            
            # Benefits
            benefits = rec.get('key_benefits', [])
            if benefits:
                formatted += "✅ Key Benefits:\n"
                for benefit in benefits[:3]:  # Limit to top 3 benefits
                    formatted += f"   • {benefit}\n"
            
            # Implementation tips
            tips = rec.get('implementation_tips', [])
            if tips:
                formatted += "\n💡 Implementation Tips:\n"
                for tip in tips[:2]:  # Limit to top 2 tips
                    formatted += f"   • {tip}\n"
            
            formatted += "\n" + "─" * 50 + "\n\n"
        
        return formatted
    
    def _format_fallback_response(self, response):
        """Fallback formatting if JSON parsing fails"""
        return f"""📊 ESG Recommendations (Raw Output):

{response}

Note: For better formatting, ensure the Ollama model returns valid JSON."""