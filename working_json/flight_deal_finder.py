import json
json_response_string = '''
{
  "route": "Delhi → Mumbai",
  "search_date": "2026-06-10",
  "flights": [
    {"flight_id": "AI-201", "airline": "Air India", "departure": "06:00", "price": 4500, "seats_available": 3},
    {"flight_id": "6E-305", "airline": "IndiGo", "departure": "09:30", "price": 3800, "seats_available": 1},
    {"flight_id": "SG-112", "airline": "SpiceJet", "departure": "13:15", "price": 3200, "seats_available": 0},
    {"flight_id": "UK-444", "airline": "Vistara", "departure": "17:45", "price": 5100, "seats_available": 5},
    {"flight_id": "6E-890", "airline": "IndiGo", "departure": "21:00", "price": 3600, "seats_available": 2}
  ]
}'''

data = json.loads(json_response_string)

available_seats = [ 
    flight for flight in data["flights"] 
    if flight["seats_available"]>=2
    ]

#print (available_seats)

best_deal= min(available_seats, key=lambda flight:flight["price"])

# print ("Airline:", best_deal["airline"])
# print ("Flight id:", best_deal["flight_id"])
# print ("Price:", best_deal["price"])

booking_summary= {
    "route": "Delhi → Mumbai",
    "selected_flight_id": best_deal["flight_id"],
    "airline" : best_deal["airline"],
    "departure" : best_deal["departure"],
    "price" : best_deal["price"],
    "status" : "ready to book",
}

flight_deal = json.dumps(booking_summary, indent=2)

print (flight_deal)
