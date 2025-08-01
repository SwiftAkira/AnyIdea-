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

## � **Current Progress Status**

### ✅ **Completed (Phase 1 & 2 Backend - Orion)**
- **Full FastAPI Backend Setup**: Python 3.11 + Conda environment
- **Smart AI Integration**: moonshotai/kimi-k2:free model generating detailed activity suggestions
- **Real Weather Data**: WeatherAPI.com integration for weather-aware recommendations
- **Comprehensive Data Models**: Pydantic schemas for request/response validation
- **Production-Ready API**: Error handling, logging, CORS, input validation
- **Core Endpoints**: `/api/suggest`, `/api/ai-suggest`, `/health`
- **Advanced AI Prompting**: Context-aware suggestions with step-by-step instructions
- **✅ Database Implementation**: Complete SQLite database with user management and custom categories
- **✅ Custom Categories**: Users can create and manage personalized activity categories
- **✅ Data Persistence**: All user data properly stored and retrieved from database
- **✅ User Session Management**: Session-based user isolation and data management
- **✅ Database Health Monitoring**: Health check endpoint for database connectivity

### 🏗️ **In Progress**
- **Frontend Development** (Anita) - TypeScript/HTML/CSS web interface
- **API Integration** - Connecting frontend forms to backend endpoints

### 📋 **Next Up**
- **Location Services**: Google Places API for nearby venues
- **Activity Logging**: Integrate activity suggestion tracking into main endpoints
- **Enhanced Features**: User history and popular activity tracking

---

## �📋 Product Requirements Document (PRD)

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
- [x] Set up Python backend environment (Conda + Python 3.11)
- [x] Choose and configure web framework (FastAPI)
- [x] Design database schema
- [x] Create basic API endpoints:
  - [x] User input endpoint (`/api/suggest`)
  - [x] Custom categories endpoint (`/api/activities/custom`)
  - [x] Database health endpoint (`/api/database/health`)
  - [x] AI suggestions endpoint (`/api/ai-suggest`)
  - [x] Health check endpoint (`/health`)
- [x] Set up basic data models (Pydantic schemas)
- [x] Create intelligent activity recommendation algorithm
- [x] Integrate OpenRouter API for AI suggestions (moonshotai/kimi-k2:free)
- [x] Integrate weather APIs (WeatherAPI.com)
- [x] Implement SQLite database with full schema
- [x] Create database service layer with user management
- [x] Implement custom category CRUD operations
- [ ] Integrate geolocation services
- [x] Set up CORS for frontend communication

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
- [x] Implement intelligent activity recommendation engine
- [x] Add budget filtering logic (built into AI prompts)
- [x] Create activity database/data structures
- [x] Integrate AI-powered suggestions via OpenRouter (moonshotai/kimi-k2:free)
- [ ] Integrate location-based filtering
- [x] Add weather API integration (WeatherAPI.com)
- [ ] Implement nearby business/venue lookup (Google Places/Yelp)
- [x] Add data persistence (SQLite)
- [x] Implement user session management and custom categories
- [x] Create database service layer with full CRUD operations
- [x] Implement basic error handling and logging
- [x] Add comprehensive input validation (Pydantic)
- [x] Create database health monitoring
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
- [x] Optimize recommendation algorithm (Advanced AI prompting)
- [x] Enhance AI prompt engineering for better suggestions
- [x] Add detailed budget breakdowns (built into suggestions)
- [ ] Implement caching for better performance
- [x] Add logging and monitoring (FastAPI + Python logging)
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
├── backend/                 # Web API server (✅ COMPLETED)
│   ├── app/
│   │   ├── models/
│   │   │   ├── schemas.py   # ✅ Pydantic data models
│   │   │   └── database.py  # ✅ SQLAlchemy database models
│   │   ├── services/        # ✅ Business logic services
│   │   │   ├── __init__.py
│   │   │   ├── openrouter_service.py  # ✅ AI integration
│   │   │   ├── weather_service.py     # ✅ Weather API
│   │   │   └── database_service.py    # ✅ Database operations
│   │   └── utils/           # Helper functions
│   ├── data/                # ✅ Database storage
│   │   └── anyidea.db      # ✅ SQLite database file
│   ├── main.py              # ✅ FastAPI app entry point
│   ├── database.py          # ✅ Database configuration
│   ├── requirements.txt     # ✅ Python dependencies
│   ├── config.py            # ✅ Environment configuration
│   ├── .env                 # ✅ API keys and settings
│   └── .gitignore           # ✅ Git ignore file
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

## 🏗️ **Technical Implementation (Orion's Achievements)**

### ✅ **FastAPI Backend Architecture**
- **Modern API Framework**: FastAPI with automatic OpenAPI documentation
- **Type Safety**: Full Pydantic integration for request/response validation
- **Error Handling**: Comprehensive exception handling with proper HTTP status codes
- **CORS Configuration**: Ready for frontend integration
- **Environment Management**: Secure API key handling with python-dotenv

### ✅ **AI-Powered Suggestion Engine**
- **Model**: moonshotai/kimi-k2:free via OpenRouter API
- **Advanced Prompting**: Context-aware prompts with weather, budget, and preference integration
- **JSON Response Parsing**: Robust extraction and validation of AI-generated suggestions
- **Fallback System**: Graceful degradation when AI services are unavailable
- **Response Quality**: AI generates detailed instructions, material lists, and cost breakdowns

### ✅ **Weather Integration**
- **Real-time Data**: WeatherAPI.com integration for current conditions
- **Location-based**: Coordinates-based weather lookup (currently San Francisco)
- **Activity Matching**: Weather-appropriate activity filtering and suggestions
- **Comprehensive Data**: Temperature, humidity, and weather condition descriptions

### ✅ **Data Models & Validation**
- **Comprehensive Schemas**: Complete Pydantic models for all data structures
- **Enum-based Options**: Structured choices for activity types, energy levels, etc.
- **Flexible Preferences**: Support for dietary restrictions, skill levels, and social preferences
- **Request Validation**: Automatic input validation with detailed error responses

### ✅ **Database Architecture**
- **SQLite Database**: Lightweight, file-based database at `./data/anyidea.db`
- **SQLAlchemy ORM**: Modern Python ORM with declarative models
- **Complete Schema**: 6 main tables for users, categories, activity logs, and history
- **Session Management**: User isolation with session-based data management
- **Transaction Safety**: Proper commit/rollback handling for data integrity
- **Health Monitoring**: Database connectivity and status endpoints

### ✅ **Database Models**
- **Users**: Session-based user management with preferences
- **CustomCategory**: User-created activity categories with descriptions
- **ActivitySuggestionLog**: Tracking of AI-generated suggestions
- **ActivitySuggestionItem**: Individual suggestion details and metadata
- **ActivityHistory**: User activity completion and feedback tracking
- **PopularActivity**: Analytics for trending activities and suggestions

### ✅ **Custom Categories Feature**
- **Create Categories**: Users can add personalized activity categories
- **Category Management**: Full CRUD operations for custom categories
- **User Isolation**: Each user sees only their own custom categories
- **Data Persistence**: Categories saved permanently to database
- **Integration Ready**: Custom categories available for activity filtering

### ✅ **API Endpoints**
- `POST /api/suggest` - Main suggestion endpoint with full feature integration
- `POST /api/activities/custom` - Create custom activity categories
- `GET /api/activities/custom` - Retrieve user's custom categories
- `GET /api/database/health` - Database connectivity and status check
- `GET /api/ai-suggest` - AI service status and configuration
- `GET /health` - Health check endpoint
- `GET /` - Welcome message with API information

## 🤖 AI Integration Details

### OpenRouter Integration  
**AnyIdea?** uses OpenRouter to access free AI models for generating intelligent, personalized activity suggestions. This allows the app to:

- **Understand Context**: AI analyzes user preferences, mood, weather, and location to suggest relevant activities
- **Creative Suggestions**: Generate unique ideas beyond pre-defined categories  
- **Personalized Instructions**: Provide step-by-step guidance tailored to user skill level
- **Dynamic Responses**: Adapt suggestions based on real-time conditions

### AI Model Selection
- **Primary**: moonshotai/kimi-k2:free (currently implemented and working)
- **Fallback**: Basic rule-based recommendations if AI is unavailable
- **Cost**: Utilize free tier to keep the project budget-friendly

### AI Prompt Strategy
The AI receives structured prompts including:
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

### API Testing Examples

With the backend running on `http://localhost:8000`, you can test these working endpoints:

#### Get AI-Generated Suggestions
```bash
curl -X POST "http://localhost:8000/api/suggest" \
  -H "Content-Type: application/json" \
  -d '{
    "location": "San Francisco, CA",
    "activity_type": "creative",
    "mood": "relaxed",
    "energy_level": "medium",
    "budget": 25,
    "duration": 90
  }'
```

#### Create Custom Activity Category
```bash
curl -X POST "http://localhost:8000/api/activities/custom?session_id=your_user_id" \
  -H "Content-Type: application/json" \
  -d '{
    "category_name": "Mindfulness",
    "description": "Meditation and mindfulness activities"
  }'
```

#### Get User's Custom Categories
```bash
curl -X GET "http://localhost:8000/api/activities/custom?session_id=your_user_id"
```

#### Check Database Health
```bash
curl -X GET "http://localhost:8000/api/database/health"
```

#### Check API Health
```bash
curl "http://localhost:8000/health"
```

**Example Response**:
```json
{
  "suggestions": [
    {
      "title": "Neighborhood Photo Walk & Coffee",
      "description": "A creative photography expedition through your neighborhood...",
      "duration": 90,
      "estimated_cost": 12,
      "materials_needed": ["Smartphone or camera", "Comfortable walking shoes"],
      "instructions": ["Start at a local coffee shop...", "Walk through 3-4 blocks..."]
    }
  ],
  "weather_context": "Current weather: Mist, 57°F",
  "personalization_notes": "Suggestions tailored for medium energy creative activities..."
}
```

**Example Custom Category Response**:
```json
{
  "status": "accepted",
  "message": "Custom category 'Mindfulness' has been created successfully",
  "accepted": true,
  "category": {
    "id": "mindfulness",
    "name": "Mindfulness",
    "description": "Meditation and mindfulness activities",
    "icon": null,
    "type": "custom",
    "created_at": "2025-08-01T19:11:16.608542"
  },
  "usage_instructions": "You can now use this category in your activity preferences"
}
```

**Example Database Health Response**:
```json
{
  "status": "healthy",
  "database_path": "./data/anyidea.db",
  "database_exists": true,
  "message": "Database connection successful"
}
```

#### Check API Health
```bash
curl "http://localhost:8000/health"
```

### Running the Backend

1. **Activate Environment**: `conda activate anyidea`
2. **Install Dependencies**: `pip install -r requirements.txt`  
3. **Set Environment Variables**: Copy `.env.example` to `.env` and add API keys
4. **Start Server**: `uvicorn main:app --reload`
5. **View Documentation**: Visit `http://localhost:8000/docs` for interactive API docs

## 🔮 **Phase 2 Development Goals**

### Immediate Next Steps
- [ ] **Activity Suggestion Logging**: Integrate database logging into main `/api/suggest` endpoint
- [ ] **User History Tracking**: Implement activity completion and feedback tracking
- [ ] **Popular Activities Analytics**: Track and recommend trending activities
- [ ] **Location Services**: Add Google Places API for location-based venue suggestions
- [ ] **Yelp Integration**: Restaurant and business recommendations based on activity type

### Enhanced Features  
- [ ] **Activity Sharing**: Social features for sharing favorite discoveries
- [ ] **Offline Mode**: Local activity database for when APIs are unavailable
- [ ] **Photo Integration**: Activity photo uploads and galleries
- [ ] **Calendar Integration**: Schedule suggested activities
- [ ] **Weather Notifications**: Push alerts for ideal activity weather
- [ ] **Custom Category Enhancement**: Add icons and color coding to custom categories

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

## 🗄️ **Database Status & Capabilities**

### ✅ Currently Implemented
- **User Management**: Automatic user creation and session management
- **Custom Categories**: Full CRUD operations for user-created activity categories
- **Data Persistence**: SQLite database with proper transaction handling
- **User Isolation**: Session-based data separation between users
- **Database Health**: Monitoring and status endpoints for database connectivity
- **Schema Complete**: All 6 database tables created and ready for use

### 🔄 Ready for Integration
- **Activity Logging**: Database models ready for suggestion tracking
- **User History**: Tables prepared for activity completion tracking
- **Analytics**: Popular activity tracking infrastructure in place

### 📊 Database Statistics
- **Database Location**: `./data/anyidea.db`
- **Tables**: 6 (users, custom_categories, activity_suggestion_logs, activity_suggestion_items, activity_history, popular_activities)
- **Current Features**: User management ✅, Custom categories ✅, Health monitoring ✅
- **Status**: Fully operational with proper commit/rollback handling

---

**Happy Coding! 🚀**

*Remember: This is a learning project, so don't worry about making it perfect. Focus on learning and having fun building together!*
