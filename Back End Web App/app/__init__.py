from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object('app.config.Config')
    

    # Initialize PricingEngine once and attach to app
    from app.services.pricing_engine import PricingEngine
    app.pricing_engine = PricingEngine()
    
    # Load the dataset
    app.pricing_engine.load_data("AmesHousing.csv") 
    
    # train the model
    app.pricing_engine.train_model()

    # Register blueprints
    from .routes import api
    app.register_blueprint(api)

    return app

app = create_app()