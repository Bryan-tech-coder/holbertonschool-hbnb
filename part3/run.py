from app import create_app
from config import Config

# Create the Flask app using the configuration
app = create_app(Config)

if __name__ == "__main__":
    # Run the development server
    app.run(debug=True)
