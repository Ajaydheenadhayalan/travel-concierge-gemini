from .tools import google_search_attractions, hotel_openapi_search, simple_pricing_estimate
from .llm_client import generate_text
import json, asyncio

class PlannerAgent:
    async def propose_skeleton(self, req):
        # Use Gemini to propose a multi-day skeleton
        system = "You are an expert travel planner. Produce a JSON skeleton with days and time slots given the request." 
        user = f"Request: {req}"
        prompt = [ {"role":"system","content":system}, {"role":"user","content":user} ]
        try:
            resp = generate_text(prompt, model="gemini-1.5", max_output_tokens=600)
            # try parse JSON from response content
            text = resp.get('content','')
            try:
                return json.loads(text)
            except Exception:
                # fallback simple skeleton
                return {"days": [ {"day":1, "slots": {"morning":null, "afternoon":null, "evening":null} } , {"day":2, "slots":{}}, {"day":3, "slots":{}} ] }
        except Exception:
            return {"days": [ {"day":1, "slots":{}} ] }

    async def refine(self, skeleton, attractions, hotels, pricing):
        system = "You are an assistant that merges skeleton + attractions + hotels into a final itinerary JSON."
        user = f"Skeleton: {skeleton}\nAttractions: {attractions}\nHotels: {hotels}\nEstimated cost: {pricing}"
        prompt = [{"role":"system","content":system},{"role":"user","content":user}]
        try:
            resp = generate_text(prompt, model="gemini-1.5", max_output_tokens=800)
            text = resp.get('content','')
            try:
                return json.loads(text)
            except Exception:
                itinerary = {"day_1": {"morning": attractions[0] if attractions else {}, "evening": {"dinner":"Local restaurant"}}}
                return {"itinerary": itinerary, "hotels": hotels, "total_estimated_cost": pricing, "confidence_score": 0.8}
        except Exception:
            itinerary = {"day_1": {"morning": attractions[0] if attractions else {}, "evening": {"dinner":"Local restaurant"}}}
            return {"itinerary": itinerary, "hotels": hotels, "total_estimated_cost": pricing, "confidence_score": 0.7}

class SearchAgent:
    async def search_attractions(self, city):
        return await google_search_attractions(city)

class HotelAgent:
    async def find_hotels(self, city, checkin, checkout, budget):
        return await hotel_openapi_search(city, checkin, checkout, budget)

class PricingAgent:
    async def estimate_cost(self, itinerary, hotels, travelers=1):
        return simple_pricing_estimate(itinerary.get('days',[]), hotels, travelers)
