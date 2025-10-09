from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import os
import subprocess
import sys
from src.recommender import ESGRecommender
from src.data_loader import ESGDataLoader

app = Flask(__name__)
app.secret_key = 'esg_recommender_secret_key_2024'

# Global variables
recommender = None
data_loader = None

def check_ollama_setup():
    """Check if Ollama is properly set up"""
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        if result.returncode != 0:
            return False, "Ollama is not installed or not in PATH"
        
        # Check if we have at least one model
        if "llama2" not in result.stdout and "gemma" not in result.stdout and "mistral" not in result.stdout:
            return False, "No suitable models found. Please install a model with 'ollama pull llama2:7b'"
        
        return True, "Ollama is ready"
        
    except FileNotFoundError:
        return False, "Ollama is not installed. Please install from https://ollama.ai/"

def initialize_services():
    """Initialize the recommender and data loader services"""
    global recommender, data_loader
    try:
        if recommender is None:
            recommender = ESGRecommender()
        if data_loader is None:
            data_loader = ESGDataLoader()
            # Load data immediately
            data_loader.load_data()
        return True, "Services initialized successfully"
    except Exception as e:
        return False, f"Failed to initialize services: {str(e)}"

@app.route('/')
def index():
    """Main page with company information form"""
    ollama_status, ollama_message = check_ollama_setup()
    services_status, services_message = initialize_services()
    
    return render_template('index.html', 
                         ollama_status=ollama_status, 
                         ollama_message=ollama_message,
                         services_status=services_status,
                         services_message=services_message)

@app.route('/recommend', methods=['POST'])
def recommend():
    """Handle recommendation requests"""
    try:
        # Get form data
        company_name = request.form.get('company_name', '').strip()
        description = request.form.get('description', '').strip()
        field = request.form.get('field', '').strip()
        activities = request.form.get('activities', '').strip()
        
        # Validate input
        if not all([company_name, description, field, activities]):
            flash('Please fill in all fields', 'error')
            return redirect(url_for('index'))
        
        # Check Ollama status
        ollama_ready, ollama_message = check_ollama_setup()
        if not ollama_ready:
            flash(f'Ollama not ready: {ollama_message}', 'error')
            return redirect(url_for('index'))
        
        # Initialize services if not already done
        if recommender is None:
            services_ready, services_message = initialize_services()
            if not services_ready:
                flash(f'Service initialization failed: {services_message}', 'error')
                return redirect(url_for('index'))
        
        # Get recommendations
        recommendations = recommender.recommend(company_name, description, field, activities)
        
        return render_template('results.html', 
                             company_name=company_name,
                             recommendations=recommendations)
        
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/methods')
def methods():
    """Display all available ESG methods"""
    try:
        # Always initialize services for this route
        services_ready, services_message = initialize_services()
        if not services_ready:
            flash(f'Service initialization failed: {services_message}', 'error')
            return redirect(url_for('index'))
        
        # Get data summary
        summary = data_loader.get_data_summary()
        
        # Get all methods
        methods_data = data_loader.esg_data
        
        return render_template('methods.html', 
                             methods=methods_data,
                             summary=summary)
        
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/method/<method_name>')
def method_detail(method_name):
    """Display detailed information about a specific method"""
    try:
        if data_loader is None:
            services_ready, services_message = initialize_services()
            if not services_ready:
                flash(f'Service initialization failed: {services_message}', 'error')
                return redirect(url_for('index'))
        
        # Get method details
        method = data_loader.get_method_by_name(method_name)
        
        if method is None:
            flash(f'Method "{method_name}" not found', 'error')
            return redirect(url_for('methods'))
        
        return render_template('method_detail.html', method=method)
        
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
        return redirect(url_for('methods'))

@app.route('/api/methods')
def api_methods():
    """API endpoint to get all methods as JSON"""
    try:
        if data_loader is None:
            services_ready, services_message = initialize_services()
            if not services_ready:
                return jsonify({'error': services_message}), 500
        
        # Get all methods as JSON
        methods_data = data_loader.esg_data.to_dict('records')
        return jsonify(methods_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/methods/<scope>')
def api_methods_by_scope(scope):
    """API endpoint to get methods by scope"""
    try:
        if data_loader is None:
            services_ready, services_message = initialize_services()
            if not services_ready:
                return jsonify({'error': services_message}), 500
        
        # Get methods by scope
        methods = data_loader.get_methods_by_scope(scope)
        
        if methods is None:
            return jsonify({'error': f'Invalid scope: {scope}'}), 400
        
        methods_data = methods.to_dict('records')
        return jsonify(methods_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5550)
