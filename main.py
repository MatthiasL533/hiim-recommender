from src.recommender import ESGRecommender

def check_ollama_setup():
    """Check if Ollama is properly set up"""
    import subprocess
    import sys
    
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Ollama is not installed or not in PATH")
            print("Please install Ollama from https://ollama.ai/")
            return False
        
        # Check if we have at least one model
        if "llama2" not in result.stdout and "gemma" not in result.stdout and "mistral" not in result.stdout:
            print("⚠️  No suitable models found. Pulling llama2:7b...")
            subprocess.run(['ollama', 'pull', 'llama2:7b'])
        
        return True
        
    except FileNotFoundError:
        print("❌ Ollama is not installed")
        print("Please install Ollama from https://ollama.ai/")
        return False

def main():
    print("ESG Reporting Method Recommender")
    print("==============================================")
    print("Using Local Ollama AI")
    print("==============================================\n")
    
    # Check Ollama setup
    if not check_ollama_setup():
        return
    
    # Get company information
    print("Enter information:")
    print("-" * 30)

    company_name = input("Company Name: ").strip()
    description = input("Company Description: ").strip()
    field = input("Industry/Field: ").strip()
    activities = input("Key Activities/Products: ").strip()
    esg_requirements = input("ESG Requirements: ").strip()
    purpose_goal = input("Purpose/End Goal: ").strip()

    if not all([company_name, description, field, activities, esg_requirements, purpose_goal]):
        print("❌ Please fill in all fields")
        return

    
    # Initialize recommender
    recommender = ESGRecommender()
    
    print("\n" + "=" * 50)
    print("🔍 Analyzing your company and ESG frameworks...")
    print("This may take 20-30 seconds...")
    print("=" * 50 + "\n")
    
    try:
        # Get recommendations
                # Get recommendations
        recommendations = recommender.recommend(
            company_name, description, field, activities, esg_requirements, purpose_goal
        )
        
        print(recommendations)
        
    except KeyboardInterrupt:
        print("\n⏹️  Process interrupted by user")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("\n💡 Troubleshooting tips:")
        print("1. Ensure Ollama is running: 'ollama serve'")
        print("2. Check if model is installed: 'ollama list'")
        print("3. Pull a model: 'ollama pull llama2:7b'")

if __name__ == "__main__":
    main()