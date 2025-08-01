# AnyIdea? - Activity Suggestion App �

A simple and intuitive app that helps you figure out what to do when you're at home and bored, based on your budget, available time, and preferences.

## 👥 Team
- **Orion** - Backend Developer (Junior Dev)
- **Anita** - Frontend Developer (CS First Year)

## 🎯 Project Overview

**AnyIdea?** is an activity suggestion application where users input their available budget, time, and preferences, and receive personalized recommendations for things to do at home or nearby.

### Core Features
- Budget-based activity suggestions
- Time-based recommendations (how long you have available)
- Food/cooking suggestions
- Indoor and outdoor activity options
- Location-based recommendations using geolocation
- Weather-aware outdoor activity suggestions
- AI-powered intelligent suggestions using OpenRouter
- Smart recommendations engine
- Clean, user-friendly interface

## 🛠️ Tech Stack

### Frontend (Anita's Responsibility)
- **TypeScript** - Type-safe JavaScript
- **CSS** - Styling and responsive design
- **HTML** - Structure and markup
- **Geolocation API** - Browser location services

### Backend (Orion's Responsibility)
- **Python** - Backend logic and API
- **FastAPI/Flask** - Web framework
- **SQLite/PostgreSQL** - Database
- **Weather API** - Weather data integration
- **Google Places/Yelp API** - Location-based business data
- **OpenRouter API** - Free AI models for intelligent suggestions

---

## 📋 Product Requirements Document (PRD)

### 🎯 User Story
*"As someone who's bored at home, I want to input my available budget, time, and preferences so that I can get personalized suggestions for activities I can do right now."*

### 🔧 Functional Requirements

#### Input Features
1. **Budget Input**
   - Available spending money
   - Budget range (free, under $20, under $50, etc.)
   - Currency selection

2. **Time Available**
   - How much time you have (30 mins, 1-2 hours, half day, full day)
   - Current time of day
   - Immediate vs planned activity
3. **Food/Cooking Preferences**
   - Do you want to cook or order food?
   - Dietary restrictions
   - Kitchen equipment available
   - Cooking skill level
   - Meal type (snack, full meal, dessert)

4. **Activity Preferences**
   - Indoor vs outdoor activities
   - Solo vs social activities
   - Activity types (creative, productive, entertainment, exercise, learning)
   - Energy level (low energy/relaxing vs high energy/active)
   - Mood (want to learn something, be entertained, be productive, etc.)

5. **Location & Environment**
   - Enable geolocation for nearby suggestions
   - Weather considerations for outdoor activities
   - Transportation preferences (walking distance, driving, public transport)
   - Local business hours and availability

#### Output Features
1. **Personalized Activity Suggestions**
   - Immediate activity options
   - Step-by-step instructions
   - Required materials/ingredients
   - Time estimates
   - Difficulty level

2. **Smart Recommendations**
   - Budget-appropriate suggestions
   - Time-optimized activities
   - Weather-appropriate options (if outdoor)
   - Location-based nearby activities
   - AI-generated personalized suggestions
   - Skill-level matched activities

---

## 🗓️ Development Timeline & Tasks

### Phase 1: Foundation (Week 1-2)
**Goal: Set up project structure and basic functionality**

#### Orion's Tasks (Backend)
- [ ] Set up Python backend environment
- [ ] Choose and configure web framework (FastAPI recommended)
- [ ] Design database schema
- [ ] Create basic API endpoints:
  - [ ] User input endpoint (`/api/suggest`)
  - [ ] Get activity recommendations endpoint (`/api/activities`)
  - [ ] Location services endpoint (`/api/location`)
  - [ ] AI suggestions endpoint (`/api/ai-suggest`)
- [ ] Set up basic data models
- [ ] Create simple activity recommendation algorithm
- [ ] Integrate OpenRouter API for AI suggestions
- [ ] Integrate geolocation and weather APIs
- [ ] Set up CORS for frontend communication

#### Anita's Tasks (Frontend)
- [ ] Set up TypeScript project structure
- [ ] Create basic HTML structure
- [ ] Design input forms:
  - [ ] Budget input form
  - [ ] Time available picker
  - [ ] Food/cooking preferences form
  - [ ] Activity preferences form
  - [ ] Location permission request
- [ ] Create basic CSS styling
- [ ] Set up form validation
- [ ] Implement geolocation functionality
- [ ] Create results display area

#### Shared Tasks
- [ ] Define API contract/documentation
- [ ] Set up development environment
- [ ] Create project documentation
- [ ] Weekly sync meetings

### Phase 2: Core Features (Week 3-4)
**Goal: Implement main functionality**

#### Orion's Tasks (Backend)
- [ ] Implement activity recommendation engine
- [ ] Add budget filtering logic
- [ ] Create activity database/data structures
- [ ] Integrate AI-powered suggestions via OpenRouter
- [ ] Integrate location-based filtering
- [ ] Add weather API integration
- [ ] Implement nearby business/venue lookup
- [ ] Add data persistence
- [ ] Implement error handling
- [ ] Add input validation
- [ ] Create mock activity data for testing

#### Anita's Tasks (Frontend)
- [ ] Connect forms to backend API
- [ ] Create results display components
- [ ] Implement loading states
- [ ] Add error handling UI
- [ ] Style the activity suggestions page
- [ ] Make forms responsive
- [ ] Add basic animations/transitions

### Phase 3: Enhancement (Week 5-6)
**Goal: Polish and improve user experience**

#### Orion's Tasks (Backend)
- [ ] Optimize recommendation algorithm
- [ ] Enhance AI prompt engineering for better suggestions
- [ ] Add more detailed budget breakdowns
- [ ] Implement caching for better performance
- [ ] Add logging and monitoring
- [ ] Create API documentation
- [ ] Add unit tests

#### Anita's Tasks (Frontend)
- [ ] Improve UI/UX design
- [ ] Add mobile responsiveness
- [ ] Implement better form UX
- [ ] Add progress indicators
- [ ] Create better error messages
- [ ] Add accessibility features

### Phase 4: Testing & Deployment (Week 7)
**Goal: Test and deploy the application**

#### Orion's Tasks (Backend)
- [ ] Set up deployment environment
- [ ] Configure production database
- [ ] Implement security measures
- [ ] Performance testing
- [ ] Create deployment scripts

#### Anita's Tasks (Frontend)
- [ ] Cross-browser testing
- [ ] Mobile device testing
- [ ] User experience testing
- [ ] Bug fixes and polish
- [ ] Create user documentation

---

## 📁 Project Structure

```
AnyIdea?/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── styles/
│   │   ├── types/
│   │   └── utils/
│   ├── index.html
│   ├── main.ts
│   └── package.json
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   └── utils/
│   ├── main.py
│   ├── requirements.txt
│   └── config.py
├── docs/
├── tests/
└── README.md
```

## 🎨 Design Guidelines

### For Anita (Frontend)
- **Keep it simple**: Focus on clean, intuitive design
- **Mobile-first**: Design for mobile, then scale up
- **User feedback**: Always show loading states and success/error messages
- **Accessibility**: Use semantic HTML and proper contrast
- **Consistency**: Use consistent spacing, colors, and typography

### Color Scheme Suggestions
- Primary: `#3B82F6` (blue)
- Secondary: `#10B981` (green)
- Accent: `#F59E0B` (orange)
- Background: `#F9FAFB` (light gray)
- Text: `#1F2937` (dark gray)

## 🚀 Learning Resources for Anita

### TypeScript Basics
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [TypeScript in 5 minutes](https://www.typescriptlang.org/docs/handbook/typescript-in-5-minutes.html)

### CSS/Styling
- [CSS Grid Guide](https://css-tricks.com/snippets/css/complete-guide-grid/)
- [Flexbox Guide](https://css-tricks.com/snippets/css/a-guide-to-flexbox/)
- [CSS-Tricks](https://css-tricks.com/)

### Form Handling
- [Form Validation Best Practices](https://web.dev/learn/forms/)
- [Fetch API for API calls](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)

### Geolocation & APIs
- [Geolocation API Guide](https://developer.mozilla.org/en-US/docs/Web/API/Geolocation_API)
- [Working with External APIs](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Client-side_web_APIs/Introduction)

## 🤖 AI Integration Details

### OpenRouter Integration
**AnyIdea?** uses OpenRouter to access free AI models for generating intelligent, personalized activity suggestions. This allows the app to:

- **Understand Context**: AI analyzes user preferences, mood, weather, and location to suggest relevant activities
- **Creative Suggestions**: Generate unique ideas beyond pre-defined categories
- **Personalized Instructions**: Provide step-by-step guidance tailored to user skill level
- **Dynamic Responses**: Adapt suggestions based on real-time conditions

### AI Model Selection
- **Primary**: Use free models available on OpenRouter (e.g., Llama, Mistral)
- **Fallback**: Basic rule-based recommendations if AI is unavailable
- **Cost**: Utilize free tier to keep the project budget-friendly

### AI Prompt Strategy
The AI will receive structured prompts including:
- User preferences and constraints
- Current weather and location data
- Available nearby businesses/venues
- Time and budget limitations

Example AI prompt:
```
"A person in San Francisco with $20, 2 hours free time, wants outdoor activities, 
beginner fitness level, partly cloudy 68°F weather. Suggest 3 specific activities 
with exact locations, costs, and step-by-step instructions."
```

## 📝 API Documentation (Draft)

### POST /api/suggest
**Request:**
```json
{
  "budget": 20,
  "currency": "USD",
  "timeAvailable": 120,
  "timeUnit": "minutes",
  "location": {
    "latitude": 37.7749,
    "longitude": -122.4194,
    "allowLocationAccess": true
  },
  "foodPreferences": {
    "wantToCook": true,
    "dietary": ["vegetarian"],
    "skillLevel": "beginner",
    "mealType": "lunch"
  },
  "activityPreferences": {
    "location": "outdoor",
    "socialLevel": "solo",
    "activityTypes": ["exercise", "sightseeing"],
    "energyLevel": "medium",
    "mood": "get_some_fresh_air"
  }
}
```

**Response:**
```json
{
  "suggestions": [
    {
      "type": "ai_generated",
      "title": "Golden Gate Park Photography Walk",
      "description": "AI-suggested scenic route combining exercise with creative photography",
      "timeRequired": 90,
      "cost": 0,
      "difficulty": "easy",
      "distance": "0.8 miles away",
      "address": "Golden Gate Park, San Francisco, CA",
      "weather_appropriate": true,
      "ai_reasoning": "Perfect weather for outdoor photography, matches your creative and exercise preferences",
      "instructions": [
        "Start at McLaren Lodge (park entrance)",
        "Walk to Stow Lake for water reflections",
        "Visit Japanese Tea Garden for architectural shots",
        "End at Conservatory of Flowers for colorful subjects"
      ]
    },
    {
      "type": "local_business",
      "title": "Visit Local Coffee Shop + Sketching",
      "description": "AI-enhanced suggestion: Combine cafe visit with creative sketching",
      "timeRequired": 60,
      "cost": 8,
      "difficulty": "easy",
      "distance": "0.3 miles away",
      "address": "Blue Bottle Coffee, 315 Linden St",
      "hours": "Open until 6 PM",
      "rating": 4.5,
      "ai_enhancement": "Bring a sketchbook to draw cafe scenes and people-watch creatively"
    }
  ],
  "weather": {
    "current": "Partly cloudy, 68°F",
    "suitable_for_outdoor": true
  },
  "ai_metadata": {
    "model_used": "llama-3.1-8b",
    "reasoning": "Combined user preferences for outdoor activities and creativity with current weather conditions"
  }
}
```

## 🎯 Success Metrics
- [ ] User can successfully input preferences
- [ ] App generates reasonable activity suggestions
- [ ] Budget filtering works accurately
- [ ] Time-based recommendations are appropriate
- [ ] Interface is intuitive for first-time users
- [ ] App works on mobile and desktop
- [ ] Response time under 3 seconds

## 💡 Future Ideas
- Integration with recipe APIs
- Weather-based activity suggestions ✅ (Already planned)
- User activity history and favorites
- Social features (share activities with friends)
- Location-based suggestions (nearby activities) ✅ (Already planned)
- AI-powered suggestions ✅ (Already planned)
- Seasonal activity recommendations
- Skill progression tracking
- Integration with ride-sharing apps for transportation
- Real-time business hours and availability
- User reviews and ratings for suggested activities
- AI learning from user feedback to improve suggestions
- Voice input for activity requests
- AI-generated custom recipes based on available ingredients

---

**Happy Coding! 🚀**

*Remember: This is a learning project, so don't worry about making it perfect. Focus on learning and having fun building together!*
