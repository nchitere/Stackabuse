# Import necessary modules from Flask
from flask import Flask, request
# Import SQLAlchemy and Migrate for database interaction and migrations
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize the Flask application
app = Flask(__name__)

# Set the URI for the PostgfreSQL database to be used in the application
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/cars_api"
# Initialize SQLAlchemy with the Flask application instance
db = SQLAlchemy(app)
# Initialize Flask-Migrate with the Flask application instance and SQLAlchemy database instance
migrate = Migrate(app, db)

# Create a model representing the 'cars' table in the database
class CarsModel(db.Model):
    __tablename__ = 'cars'

    # Define columns in the 'cars' table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    model = db.Column(db.String())
    doors = db.Column(db.Integer())
    color = db.Column(db.String())
    horsepower= db.Column(db.String())

    # Constructor to initialize the model with values for name, model, and doors
    def __init__(self, name, model, doors,color, horsepower):
        self.name = name
        self.model = model
        self.doors = doors
        self.color = color
        self.horsepower =horsepower

    # Representation method to provide a readable representation of the model object
    def __repr__(self):
        return f"<Car {self.name}>"

# Define a route for handling requests to '/cars' endpoint
@app.route('/cars', methods=['POST', 'GET'])
def handle_cars():
    # Handle POST requests to create a new car entry in the database
    if request.method == 'POST':
        # Check if the request payload is in JSON format
        if request.is_json:
            # Parse JSON data from the request
            data = request.get_json()
            print(data,">>>>>>>>>>>>>>>>>>>")#know where data has been created in the logs
            # Create a new car object with data from the JSON payload
            new_car = CarsModel(name=data['name'], 
                                model=data['model'], doors=data['doors'],
                                    color=data['color'], horsepower=data['horsepower'])
            # Add the new car object to the database session
            db.session.add(new_car)
            # Commit the changes to the database
            db.session.commit()
            # Return a success message indicating the creation of the new car entry
            return {"message": f"car {new_car.name} has been created successfully."}
        # Return an error message if the request payload is not in JSON format
        else:
            return {"error": "The request payload is not in JSON format"}

    # Handle GET requests to retrieve all car entries from the database
    elif request.method == 'GET':
        # Query all car objects from the database
        cars = CarsModel.query.all()
        # Format the results as a list of dictionaries containing car information
        results = [
            {
                "name": car.name,
                "model": car.model,
                "doors": car.doors,
                "color": car.color,
                "horsepower":car.horsepower
            } for car in cars]
        # Return the count of car entries and the list of car information dictionaries
        return {"count": len(results), "cars": results}

# Define a route for handling requests to '/cars/<car_id>' endpoint
@app.route('/cars/<car_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_car(car_id):
    # Query the car object from the database with the specified car ID
    car = CarsModel.query.get_or_404(car_id)

    # Handle GET requests to retrieve the car information
    if request.method == 'GET':
        # Create a dictionary containing car information
        response = {
            "name": car.name,
            "model": car.model,
            "doors": car.doors,
            "color": car.color,
            "horsepower":car.horsepower
        }
        # Return a success message and the car information dictionary
        return {"message": "success", "car": response}

    # Handle PUT requests to update the car information
    elif request.method == 'PUT':
        # Parse JSON data from the request
        data = request.get_json()
        # Update the car object with new data from the JSON payload
        car.name = data['name']
        car.model = data['model']
        car.doors = data['doors']
        car.color = data['color']
        # Add the updated car object to the database session
        db.session.add(car)
        # Commit the changes to the database
        db.session.commit()
        # Return a success message indicating the successful update of the car information
        return {"message": f"car {car.name} successfully updated"}

    # Handle DELETE requests to delete the car entry from the database
    elif request.method == 'DELETE':
        # Delete the car object from the database session
        db.session.delete(car)
        # Commit the changes to the database
        db.session.commit()
        # Return a success message indicating the successful deletion of the car entry
        return {"message": f"Car {car.name} successfully deleted."}

# Define a route for handling requests to '/favicon.ico' endpoint
@app.route('/favicon.ico')
def favicon():
    # Return an empty response with a 200 status code for favicon.ico requests
    return '', 200

# Uncomment the following code to run the Flask application
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', debug=True)
