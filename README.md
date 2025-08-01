# AnyIdea? - Activity Suggestion Web App 🌐

A simple and intuitive web application that helps you figure out what to do when you're at home and bored, based on your budget, available time, and preferences.nyIdea? - Activity Suggestion App �

A simple and intuitive app that helps you figure out what to do when you're at home and bored, based on your budget, available time, and preferences.

## 👥 Team
- **Orion** - Backend Developer (Junior Dev)
- **Anita** - Frontend Developer (CS First Year)

## 🎯 Project Overview

**AnyIdea?** is a web-based activity suggestion application where users input their available budget, time, and preferences, and receive personalized recommendations for things to do at home or nearby. The app runs entirely in the browser with a Python backend API.

### Core Features
- Budget-based activity suggestions
- Time-based recommendations (how long you have available)
- Food/cooking suggestions
- Indoor and outdoor activity options
- Location-based recommendations using geolocation
- Weather-aware outdoor activity suggestions
- AI-powered intelligent suggestions using OpenRouter
- Smart recommendations engine
- Responsive web design for all devices
- Clean, user-friendly web interface

## 🛠️ Tech Stack

### Frontend (Anita's Responsibility) - Web Client
- **TypeScript** - Type-safe JavaScript for the web
- **CSS3** - Modern styling and responsive design
- **HTML5** - Semantic markup and structure
- **Vanilla JS/TS** - No frameworks to keep it simple for learning
- **Web APIs**: Geolocation API, Fetch API
- **Development**: Live server for local development

### Backend (Orion's Responsibility) - Web API
- **Python** - Backend logic and REST API
- **FastAPI** - Modern, fast web framework for APIs
- **SQLite** - Lightweight database (can upgrade to PostgreSQL later)
- **Weather API** - Weather data integration
- **Google Places/Yelp API** - Location-based business data
- **OpenRouter API** - Free AI models for intelligent suggestions
- **CORS** - Cross-origin resource sharing for web client

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
- [ ] Create basic HTML structure and layout
- [ ] Design responsive web forms:
  - [ ] Budget input form
  - [ ] Time available picker
  - [ ] Food/cooking preferences form
  - [ ] Activity preferences form
  - [ ] Location permission request
- [ ] Create modern CSS styling (CSS Grid/Flexbox)
- [ ] Set up client-side form validation
- [ ] Implement geolocation functionality
- [ ] Create results display area
- [ ] Set up live development server

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
- [ ] Connect web forms to backend REST API
- [ ] Create responsive results display components
- [ ] Implement loading states and spinners
- [ ] Add user-friendly error handling UI
- [ ] Style the activity suggestions page
- [ ] Ensure mobile-responsive design
- [ ] Add smooth animations/transitions

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
- [ ] Improve responsive web design
- [ ] Add mobile-first CSS optimizations
- [ ] Implement progressive web app features
- [ ] Add better form UX patterns
- [ ] Create loading progress indicators
- [ ] Improve error messages and user feedback
- [ ] Add web accessibility features (ARIA labels, etc.)

### Phase 4: Testing & Deployment (Week 7)
**Goal: Test and deploy the application**

#### Orion's Tasks (Backend)
- [ ] Set up web hosting/deployment environment
- [ ] Configure production database
- [ ] Implement API security measures
- [ ] Performance testing for web API
- [ ] Create deployment scripts for web server

#### Anita's Tasks (Frontend)
- [ ] Cross-browser web testing (Chrome, Firefox, Safari)
- [ ] Mobile device testing (responsive design)
- [ ] Web accessibility testing
- [ ] Bug fixes and UI polish
- [ ] Create user documentation/help page

---

## 📁 Project Structure

```
AnyIdea?/
├── frontend/                 # Web client
│   ├── src/
│   │   ├── components/       # Reusable web components
│   │   ├── styles/          # CSS files
│   │   ├── types/           # TypeScript type definitions
│   │   └── utils/           # Helper functions
│   ├── public/              # Static assets
│   ├── index.html           # Main HTML file
│   ├── main.ts              # Entry point
│   └── package.json         # Dependencies
├── backend/                 # Web API server
│   ├── app/
│   │   ├── models/          # Data models
│   │   ├── routes/          # API endpoints
│   │   ├── services/        # Business logic
│   │   └── utils/           # Helper functions
│   ├── main.py              # FastAPI app entry point
│   ├── requirements.txt     # Python dependencies
│   └── config.py            # Configuration
├── docs/                    # Documentation
├── tests/                   # Test files
└── README.md
```

## 🎨 Design Guidelines

### For Anita (Frontend Web Development)
- **Mobile-first responsive design**: Design for mobile, then scale up to desktop
- **Modern web standards**: Use semantic HTML5, CSS Grid/Flexbox
- **User feedback**: Always show loading states and success/error messages
- **Web accessibility**: Use ARIA labels, semantic markup, and proper contrast
- **Cross-browser compatibility**: Test on Chrome, Firefox, and Safari
- **Progressive enhancement**: Ensure basic functionality works without JavaScript

### Color Scheme Suggestions
- Primary: `#3B82F6` (blue)
- Secondary: `#10B981` (green)
- Accent: `#F59E0B` (orange)
- Background: `#F9FAFB` (light gray)
- Text: `#1F2937` (dark gray)

## 🚀 Learning Resources for Anita

### Web Development Basics
- [MDN Web Docs](https://developer.mozilla.org/en-US/) - Complete web development reference
- [HTML5 Semantic Elements](https://developer.mozilla.org/en-US/docs/Web/HTML/Element)
- [CSS Grid Guide](https://css-tricks.com/snippets/css/complete-guide-grid/)
- [Flexbox Guide](https://css-tricks.com/snippets/css/a-guide-to-flexbox/)
- [Responsive Web Design](https://web.dev/responsive-web-design-basics/)

### TypeScript for Web
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [TypeScript in 5 minutes](https://www.typescriptlang.org/docs/handbook/typescript-in-5-minutes.html)

### Web APIs & Forms
- [Form Validation Best Practices](https://web.dev/learn/forms/)
- [Fetch API for API calls](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)
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
- [ ] User can successfully input preferences via web forms
- [ ] App generates reasonable activity suggestions
- [ ] Budget filtering works accurately
- [ ] Time-based recommendations are appropriate
- [ ] Web interface is intuitive for first-time users
- [ ] App works on mobile and desktop browsers
- [ ] API response time under 3 seconds
- [ ] Cross-browser compatibility (Chrome, Firefox, Safari)
- [ ] Mobile-responsive design works on different screen sizes

## 💡 Future Ideas
- Integration with recipe APIs
- Weather-based activity suggestions ✅ (Already planned)
- User activity history and favorites
- Social features (share activities with friends)
- Location-based suggestions (nearby activities) ✅ (Already planned)
- AI-powered suggestions ✅ (Already planned)
- Progressive Web App (PWA) features
- Offline functionality with service workers
- Push notifications for activity reminders
- Seasonal activity recommendations
- Skill progression tracking
- Integration with ride-sharing apps for transportation
- Real-time business hours and availability
- User reviews and ratings for suggested activities
- AI learning from user feedback to improve suggestions
- Voice input for activity requests
- AI-generated custom recipes based on available ingredients
- Web sharing API for easy activity sharing

---

**Happy Coding! 🚀**

*Remember: This is a learning project, so don't worry about making it perfect. Focus on learning and having fun building together!*
