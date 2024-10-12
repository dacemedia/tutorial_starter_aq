# Install virtualenv if you don't have it
pip install virtualenv

# Create a virtual environment
virtualenv weather_env

# Activate the virtual environment (Windows)
weather_env\Scripts\activate

# Activate the virtual environment (Linux/macOS)
source weather_env/bin/activate

pip install requests

python weather_app.py
