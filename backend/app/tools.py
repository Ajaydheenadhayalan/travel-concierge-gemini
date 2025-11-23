import asyncio
async def google_search_attractions(city,query="top",limit=5):
    await asyncio.sleep(0.05)
    return [{"name":f"{city} Museum","desc":"Popular","time":"2h"},{"name":f"{city} Park","desc":"Scenic","time":"1.5h"}][:limit]

async def hotel_openapi_search(city,checkin,checkout,max_price):
    await asyncio.sleep(0.05)
    return [
        {"name":f"{city} Budget Inn","price_per_night": max(20, max_price*0.25),"rating":4.0,"link":"http://example.com/1"},
        {"name":f"{city} Comfort Stay","price_per_night": max(50, max_price*0.4),"rating":4.3,"link":"http://example.com/2"},
        {"name":f"{city} Premium","price_per_night": max(100, max_price*0.6),"rating":4.7,"link":"http://example.com/3"},
    ]

def simple_pricing_estimate(itinerary, hotels, travelers=1):
    days = max(1, len(itinerary))
    hotel_cost = hotels[0]['price_per_night'] * days * travelers if hotels else 50*days*travelers
    activities_cost = 30 * days * travelers
    return hotel_cost + activities_cost
