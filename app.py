from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

def let_flight():
    url = "https://api.aviationstack.com/v1/flights?access_key=b14e5d900b501861bc654e9f32f43589"
    return url  # Return the URL instead of making a request inside this function

@app.route('/', methods=['GET'])
def search_flights():
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    airline = request.args.get('airline')

    # Build request parameters
    params = {
        "dep_iata": origin if origin else None,
        "arr_iata": destination if destination else None,
        "airline_iata": airline if airline else None,
    }

    # Remove None values
    params = {k: v for k, v in params.items() if v is not None}

    try:
        # Fetch flight data using the flight() function
        response = requests.get(let_flight(), params=params)
        response.raise_for_status()  # Raise an error for HTTP failures
        data = response.json()

        if "data" not in data or not data["data"]:
            return jsonify({"error": "No flight data available"}), 404

        # Extract relevant flight details
        flights = []
        for flight in data["data"]:
            flights.append({
                "flight_number": flight.get("flight", {}).get("iata"),
                "airline": flight.get("airline", {}).get("name"),
                "departure_airport": flight.get("departure", {}).get("airport"),
                "arrival_airport": flight.get("arrival", {}).get("airport"),
                "departure_time": flight.get("departure", {}).get("estimated"),
                "arrival_time": flight.get("arrival", {}).get("estimated"),
                "status": flight.get("flight_status"),
            })

        return jsonify(flights)

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to fetch flight data", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

