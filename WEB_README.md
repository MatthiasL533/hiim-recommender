# ESG Recommender Web Application

A modern web-based interface for the ESG Method Recommender system, built with Flask and Bootstrap.

## Features

### 🌐 Web Interface
- **Modern UI**: Clean, responsive design with Bootstrap 5
- **Company Form**: Easy-to-use form for entering company information
- **AI Recommendations**: Get personalized ESG method recommendations
- **Method Browser**: Browse all available ESG methods with filtering
- **Method Details**: Detailed view of each ESG method

### 🔍 Method Discovery
- **Search & Filter**: Find methods by name, developer, or scope
- **Scope Filtering**: Filter by Environmental, Social, Ethical, or Economic scope
- **Developer Filtering**: Filter by method developer/organization
- **Detailed Information**: View comprehensive method details

### 🤖 AI Integration
- **Local AI**: Uses Ollama for privacy-first AI recommendations
- **No Data Sharing**: All processing happens locally
- **Smart Matching**: AI analyzes your company profile for best matches

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set up Ollama (for AI recommendations)
```bash
# Install Ollama from https://ollama.ai/
ollama pull llama2:7b
ollama serve
```

### 3. Run the Web Application
```bash
python run_web.py
```

### 4. Open in Browser
Navigate to: http://localhost:5000

## Usage

### Getting Recommendations
1. Fill in your company information:
   - Company Name
   - Industry/Field
   - Company Description
   - Key Activities/Products

2. Click "Get ESG Recommendations"
3. Review AI-generated recommendations
4. Explore detailed method information

### Browsing Methods
1. Click "All Methods" in the navigation
2. Use filters to narrow down results:
   - Search by name or description
   - Filter by scope (Environmental, Social, etc.)
   - Filter by developer
3. Click on any method for detailed information

## API Endpoints

The web app also provides REST API endpoints:

- `GET /api/methods` - Get all methods as JSON
- `GET /api/methods/<scope>` - Get methods by scope (Environmental, Social, etc.)

## File Structure

```
├── app.py                 # Main Flask application
├── run_web.py            # Web app launcher script
├── templates/            # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Home page with company form
│   ├── results.html      # Recommendation results
│   ├── methods.html      # Method browser
│   └── method_detail.html # Individual method details
├── static/               # Static files (CSS, JS, images)
└── src/                  # Core application modules
    ├── data_loader.py    # CSV data handling
    ├── recommender.py    # Recommendation logic
    └── llm_handler.py    # AI integration
```

## System Requirements

- Python 3.8+
- Flask 2.3+
- Pandas 1.5+
- Ollama (for AI features)

## Troubleshooting

### Ollama Issues
- Ensure Ollama is installed: https://ollama.ai/
- Start Ollama service: `ollama serve`
- Install a model: `ollama pull llama2:7b`

### Web App Issues
- Check if port 5000 is available
- Ensure all dependencies are installed
- Check console output for error messages

### Data Issues
- Ensure `data/csv_impactmeasurement_repo.csv` exists
- Check file permissions and format

## Development

To run in development mode:
```bash
export FLASK_ENV=development
python app.py
```

The app will automatically reload on code changes.

## License

This project is part of the ESG Recommender system.
