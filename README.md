# ✈️ Travel Concierge AI Agent

**A multi-agent AI system designed to streamline travel planning.**

The **Travel Concierge AI Agent** is a comprehensive solution that generates detailed itineraries, suggests accommodations, estimates costs, and refines plans based on user feedback. Built on a robust multi-agent architecture powered by **Google Gemini**, it serves as a bridge between complex travel data and user-friendly planning.

---

## 🚀 Key Features

* **Full Itinerary Generation:** Creates detailed day-by-day plans including morning, afternoon, and evening activities.
* **Smart Hotel Recommendations:** Suggests stays that strictly adhere to the user's specific budget and location preferences.
* **Cost Estimation:** Provides a calculated estimate of the total trip cost (flights, hotels, food, and activities).
* **Iterative Refinement:** Users can modify plans using natural language (e.g., *"Make the trip shorter,"* *"Find cheaper hotels,"* or *"Focus on museums"*).
* **Structured Output:** Delivers data in clean, parseable JSON format for easy frontend integration.
* **Modern Stack:** High-performance Backend (**FastAPI**) paired with a reactive Frontend (**React**).

---

## 🧠 Agent Architecture

This system utilizes a **Multi-Agent Orchestration** pattern. Each agent specializes in a specific domain, ensuring high accuracy and modularity.

### 1. 👮 Coordinator Agent
* **Role:** The "Manager."
* **Function:** Manages the conversation history (memory), routes user requests to the appropriate sub-agents, and ensures the final output meets the user's requirements.

### 2. 🗓️ Planner Agent
* **Role:** The "Architect."
* **Function:** structures the logical flow of the trip. It merges data from the Search and Hotel agents to create the final day-by-day schedule.

### 3. 🔍 Search Agent
* **Role:** The "Scout."
* **Function:** Identifies top-rated attractions, hidden gems, and restaurants based on the destination and user interests.

### 4. 🏨 Hotel Agent
* **Role:** The "Concierge."
* **Function:** Finds accommodation options. It analyzes pricing, amenities, and proximity to city centers to provide the best recommendations within budget.

### 5. 💰 Pricing Agent
* **Role:** The "Accountant."
* **Function:** Aggregates costs from hotels and activities to generate a realistic total trip estimate.

### 6. 🛠️ Refinement Agent
* **Role:** The "Editor."
* **Function:** Takes an existing itinerary and modifies specific parameters (duration, cost, activity type) without rebuilding the entire plan from scratch.

---

## 🛠️ Tech Stack

### Backend
* **Framework:** FastAPI (Python)
* **LLM:** Google Gemini (via API)
* **Orchestration:** LangChain / Custom Agent Graph
* **Data Validation:** Pydantic

### Frontend
* **Framework:** React.js
* **Styling:** Tailwind CSS
* **State Management:** React Context / Redux

---
