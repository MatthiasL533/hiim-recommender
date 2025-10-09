import ollama
import json
import re

class OllamaHandler:
    def __init__(self, model_name="llama2:7b"):
        self.model_name = model_name
        self.client = ollama.Client()
        
    def get_recommendations(self, user_input, esg_context):
        """Get structured ESG recommendations using Ollama"""
        
        prompt = self._build_structured_prompt(user_input, esg_context)
        
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
    
    def _build_structured_prompt(self, user_input, esg_context):
        """Build a prompt that forces structured JSON output"""
        
        return f"""You are an expert ESG (Environmental, Social, Governance) assessment consultant.
Analyze the user's requirements and recommend the most suitable ESG methods from the available repository using chain-of-thought reasoning.

USER REQUIREMENTS:
Assessment Focus: {user_input['focus']}
Industry/Context: {user_input['industry']}
Specific Needs: {user_input['needs']}
Key Objectives: {user_input['objectives']}

Repository: {esg_context}

CHAIN-OF-THOUGHT ANALYSIS PROCESS:
STEP 1: Classification Reasoning
First, determine which broad method classification best fits the user's needs:

ESEA (Environmental and Social Economic Assessment): Environmental/social impact assessment, stakeholder analysis, economic evaluation
SIA (Social Impact Assessment): Social effects, community impacts, human rights, stakeholder welfare
LCA (Life Cycle Assessment): Environmental impacts across product/service lifecycle, resource use, sustainability metrics

Analyze:

Primary focus area (environmental, social, economic, or combination)
Assessment type needed (impact, performance, compliance, reporting)
Scope and stage (planning, operation, product lifecycle, organizational)

STEP 2: Method Evaluation Criteria
For each method in the selected classification, evaluate against these dimensions:

Description Match: How well does the method's description align with user needs?
How relevant are the method's classified rationale and ratings compared to user's initial needs?

STEP 3: Scoring Logic

Analyze each CSV field
Weigh each capability based on user's stated objectives
Calculate total relevance score for each method
Rank methods and select top 3

INSTRUCTIONS:

Perform classification reasoning to select ESEA, SIA, or LCA
Analyze methods within selected classification against all evaluation criteria
Review Description and rationale fields
Match method capabilities to user requirements
Select the TOP 3 most suitable methods
Return your response as VALID JSON only

RETURN STRICT JSON FORMAT (no other text):
{{
"classification_reasoning": {{
"selected_classification": "ESEA/SIA/LCA",
"primary_focus_identified": "Description of user's main concern",
"assessment_type": "Type of assessment needed",
"scope_and_stage": "Relevant scope/stage identified",
"classification_justification": "Why this classification was selected"
}},
"user_needs_summary": "Brief analysis of user's specific ESG method requirements",
"recommendations": [
{{
"rank": 1,
"method_name": "Exact method name from CSV",
"overall_fit_score": "High/Medium/Low",
"justification": "Detailed explanation of why this method is the best fit",
"key_strengths": ["Strength 1", "Strength 2", "Strength 3"],
"applicable_scenarios": ["Scenario 1", "Scenario 2"]
}},
{{
"rank": 2,
"method_name": "Exact method name from CSV",
"overall_fit_score": "High/Medium/Low",
"justification": "Detailed explanation of why this method is a strong fit",
"key_strengths": ["Strength 1", "Strength 2", "Strength 3"],
"applicable_scenarios": ["Scenario 1", "Scenario 2"]
}},
{{
"rank": 3,
"method_name": "Exact method name from CSV",
"overall_fit_score": "High/Medium/Low",
"justification": "Detailed explanation of why this method is a good fit",
"key_strengths": ["Strength 1", "Strength 2", "Strength 3"],
"applicable_scenarios": ["Scenario 1", "Scenario 2"]
}}
],
"selection_rationale": "Overall explanation of why these three methods together best serve the user's needs"
}}

IMPORTANT GUIDELINES:

Use exact method names from the CSV repository
Base analysis on actual CSV data fields
Quote or reference specific purpose-rationale content when justifying scores
Ensure classification_reasoning clearly shows chain-of-thought process
If user needs span multiple classifications, select the primary one and note in justification
Be specific about which CSV fields drove each assessment"""
    
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