# Streamlit Parser - CV2Profile Deployment

This repository contains a streamlit app for parsing CVs and creating standardized profiles using AI technology.

## Deployment Instructions

### Local Development
1. Clone this repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - MacOS/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run the app: `streamlit run main.py`

### Streamlit Cloud Deployment
1. Fork or push this repository to your GitHub account
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Click "New app"
4. Select this repository, branch and main.py file
5. Add your OpenAI API key to the Streamlit secrets:
   ```
   openai_api_key = "your-openai-api-key"
   ```
6. Deploy!

## Features
- Upload CV documents (PDF, DOCX, PNG, JPG)
- Extract structured data using AI
- Edit and reorganize CV data
- Generate standardized profiles
- Multiple template options
- Save customized settings

## System Requirements
- Python 3.7+
- Tesseract OCR (installed automatically in Streamlit Cloud)
- OpenAI API key

## Important Files
- `main.py`: Entry point for the application
- `src/ui/app.py`: Main application interface
- `src/core/ai_extractor.py`: AI processing with OpenAI
- `src/templates/template_generator.py`: Profile generation
- `.streamlit/secrets.toml`: Configuration for API keys (create from secrets_template.toml)

## Troubleshooting
- If images don't display correctly, check the static/images directory
- For OCR issues, make sure Tesseract is properly installed
- API key issues are usually resolved by checking your secrets configuration 