from fastapi import APIRouter
import asyncio
from .agents import PlannerAgent, SearchAgent, HotelAgent, PricingAgent
from .memory import InMemorySessionService
from .observability import log_event, new_trace_id

router = APIRouter()
planner = PlannerAgent()
search = SearchAgent()
hotel = HotelAgent()
pricing = PricingAgent()
sessions = InMemorySessionService()

@router.post("/plan")
async def plan_trip(payload: dict):
    trace_id = new_trace_id()
    log_event("request_received", trace_id=trace_id)
    sk = await planner.propose_skeleton(payload)
    attractions, hotels = await asyncio.gather(
        search.search_attractions(payload['destination']),
        hotel.find_hotels(payload['destination'], payload['start_date'], payload['end_date'], payload['budget'])
    )
    cost = await pricing.estimate_cost(sk, hotels, payload.get('travelers',1))
    plan = await planner.refine(sk, attractions, hotels, cost)
    sessions.save(payload.get('user_id','anon'), {'latest_plan': plan})
    return plan
