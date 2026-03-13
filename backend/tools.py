from langchain_core.tools import tool

# Data for the tools (Bengaluru Locations)
ticket_prices = {
    "whitefield": 120,
    "electronic city": 150,
    "marathahalli": 100,
    "indiranagar": 130,
    "koramangala": 140,
    "btm layout": 110,
    "yelahanka": 160,
    "hebbal": 150,
    "malleshwaram": 125,
    "rajajinagar": 135
}

weather_data = {
    "whitefield": {"temp": 26, "condition": "Partly Cloudy"},
    "electronic city": {"temp": 27, "condition": "Sunny"},
    "marathahalli": {"temp": 26, "condition": "Cloudy"},
    "indiranagar": {"temp": 27, "condition": "Clear"},
    "koramangala": {"temp": 26, "condition": "Partly Cloudy"},
    "btm layout": {"temp": 27, "condition": "Sunny"},
    "yelahanka": {"temp": 25, "condition": "Windy"},
    "hebbal": {"temp": 26, "condition": "Cloudy"},
    "malleshwaram": {"temp": 26, "condition": "Clear"},
    "rajajinagar": {"temp": 26, "condition": "Partly Cloudy"}
}

@tool
def get_ticket_price(destination_city: str) -> str:
    """Get the price of a trip to a destination city."""
    print(f"🎫 Tool: get_ticket_price({destination_city})")
    city = destination_city.lower()
    price = ticket_prices.get(city, None)
    if price:
        return f"Trip to {destination_city}: ₹{price}"
    return f"No trips available to {destination_city}"

@tool
def get_all_prices() -> str:
    """Get prices for all available destinations."""
    print(f"📋 Tool: get_all_prices()")
    prices = [f"{city.title()}: ₹{price}" for city, price in ticket_prices.items()]
    return "Available destinations: " + ", ".join(prices)

@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    print(f"🌤️ Tool: get_weather({city})")
    city_lower = city.lower()
    weather = weather_data.get(city_lower, None)
    if weather:
        return f"Weather in {city}: {weather['temp']}°C, {weather['condition']}"
    return f"Weather data not available for {city}"

@tool
def book_flight(origin_city: str, destination_city: str, passenger_name: str) -> str:
    """Book a trip for a passenger from an origin to a destination."""
    print(f"🚗 Tool: book_flight({origin_city} to {destination_city}, for {passenger_name})")
    dest = destination_city.lower()
    price = ticket_prices.get(dest, None)
    if price:
        confirmation = f"BK{hash(passenger_name + dest) % 10000:04d}"
        return f"✅ Booked! {passenger_name} from {origin_city} → {destination_city}. Confirmation: {confirmation}. Total: ₹{price}"
    return f"Cannot book trip to {destination_city} - destination not available"

tools = [get_ticket_price, get_all_prices, get_weather, book_flight]