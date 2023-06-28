import json
from flask import Flask, request

app = Flask(__name__)

airlines = [
    { "name": 'Delta'},
    { "name": 'American Airlines'},
    { "name": 'Alaska Airlines'},
  ]

airports = [
  {
    "AirportCode": "SFO",
    "AirportName": "San Francisco International Airport",
    "Country": "United States",
    "State": "California",
    "City": "San Francisco"
  },
  {
    "AirportCode": "LAX",
    "AirportName": "Los Angeles International Airport",
    "Country": "United States",
    "State": "California",
    "City": "Los Angeles"
  },
  {
    "AirportCode": "JFK",
    "AirportName": "John F. Kennedy International Airport",
    "Country": "United States",
    "State": "New York",
    "City": "New York City"
  }
]


flights = [
  {
    "FlightNumber": 1234,
    "Airline": "United Airlines",
    "Seats": 150,
    "OriginAirport": "SFO",
    "DestinationAirport": "LAX"
  },
  {
    "FlightNumber": 5678,
    "Airline": "American Airlines",
    "Seats": 200,
    "OriginAirport": "JFK",
    "DestinationAirport": "SFO"
  },
  {
    "FlightNumber": 9012,
    "Airline": "Delta Airlines",
    "Seats": 100,
    "OriginAirport": "LAX",
    "DestinationAirport": "JFK"
  }
]

@app.route("/airlines")
def get_airlines():
  return json.dumps(airlines)

@app.route("/airports")
def get_airports():
  return json.dumps(airports)

@app.route("/flights/<flightnumber>/<value>")
def get_flights(flightnumber='all',value='all'):
  global flights
  if flightnumber == 'all' and value == 'all':
    return json.dumps(flights)
  else:
    print(value, type(value))
    flights = [flight for flight in flights if flight[flightnumber] == int(value)]
    return json.dumps(flights)

@app.route("/airlines", methods=["POST"])
def post_airline():
  data = request.get_json()
  airline = {
    "name": data["name"]
    }
  airlines.append(airline)
  return json.dumps(airline)

@app.route("/airports", methods=["POST"])
def post_airport():
  data = request.get_json()
  airport = {
    "AirportCode": data['AirportCode'],
    "AirportName": data['AirportName'],
    "Country": data['Country'],
    "State": data['State'],
    "City": data['City']
  }
  airports.append(airport)
  return json.dumps(airport)

@app.route("/flights", methods=["POST"])
def post_flight():
  data = request.get_json()
  flight = {
    "FlightNumber": data['FlightNumber'],
    "Airline": data['Airline'],
    "Seats": data['Seats'],
    "OriginAirport": data['OriginAirport'],
    "DestinationAirport": data['DestinationAirport']
  }
  flights.append(flight)
  return json.dumps(flight)

# Flights update based on flight number
@app.route("/flights/<flightnumber>/<variabletoupdate>/<newvalue>", methods=["PUT"])
def update_flight(flightnumber,variabletoupdate,newvalue):
    
    global flights   
    flight = [flight for flight in flights if flight['FlightNumber'] == int(flightnumber)][0]
    #Update flight
    flight[variabletoupdate] = newvalue
    #Removing old flight
    flights = [flight for flight in flights if flight['FlightNumber'] != int(flightnumber)]
    #Adding updated flight
    flights.append(flight)
    return json.dumps(flights)


# Delete a flight based on flightnumber 
@app.route("/flights/<flightnumber>", methods=["DELETE"])
def delete_flight(flightnumber):
    global flights
    flights = [flight for flight in flights if flight['FlightNumber'] != int(flightnumber)]
    print(flights)
    return json.dumps(flights)
  
if __name__ == "__main__":
  app.run(host="localhost", port=1337)

