# Back-End Web App

This project is a Flask web application that provides a RESTful API for pricing 
houses using machine learning techniques. It utilizes libraries such as NumPy, 
Pandas, Matplotlib, and SciPy to build a pricing engine that can predict house 
prices based on various input features.

## Building/Running
To build the web app, perform the following:

- Open a command prompt 
- Change to the "Back End Web Server" directory
- Ensure dependent packages are installed.  If not, run "pip install -r app/requirements.txt" 
- Run "py server.py"  

The server should start and will listen on port 10000.  

## API Endpoints

- `POST /predict`: Accepts input features for a house and returns the predicted price.
- `GET /priceRequest`: Accepts house feature parameters as query string and returns a response object containing the same fields, the generated price, and an optional message.

## Dependencies

This project requires the following Python packages:

- Flask
- NumPy
- Pandas
- Matplotlib
- SciPy
