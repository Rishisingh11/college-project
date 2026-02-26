# College Blind Date Project

A Flask web application that helps college students find anonymous dates based on their preferences and shared interests.

## Features

- **User Registration**: Students can sign up with their gender, year, preferred dating criteria, and hobbies
- **Smart Matching**: Algorithm matches users based on gender preferences, academic year, and hobby compatibility
- **Anonymous Dating**: Users get anonymous IDs to maintain privacy until they meet
- **Random Meetups**: System generates random meeting locations and times on campus
- **Real-time Updates**: Automatic checking for new matches
- **Admin Dashboard**: View system statistics and manage users/matches

## How It Works

1. **Sign Up**: Fill out the registration form with your preferences
2. **Wait for Match**: System searches for compatible users in real-time
3. **Get Matched**: Receive anonymous ID, meeting location, and time
4. **Meet Up**: Find each other using anonymous IDs at the specified location
5. **Decide Together**: Choose whether to reveal real identities

## Installation

1. Install Python 3.7+
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:

   ```bash
   python app.py
   ```

4. Open your browser to `http://localhost:5000`

## 🚀 Quick Deploy to Production

### Option 1: One-Click Heroku Deploy (Windows)

```bash
deploy.bat
```

### Option 2: Manual Heroku Deploy

```bash
python deploy_helper.py
git add . && git commit -m "Deploy"
heroku create your-app-name
heroku config:set SECRET_KEY=your-generated-key
git push heroku main
```

### Other Hosting Options

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions on:

- 🚂 Railway
- 🎨 Render
- 🐍 PythonAnywhere
- 🌊 DigitalOcean
- And more!

## Project Structure

```
college-blind-date/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── data.json             # Data storage (auto-generated)
├── templates/
│   ├── index.html        # Main user interface
│   └── admin.html        # Admin dashboard
└── static/
    └── style.css         # Styling and animations
```

## Configuration

### Meeting Locations

Edit the `MEETING_LOCATIONS` list in `app.py` to customize campus locations:

```python
MEETING_LOCATIONS = [
    "University Library - Study Room 3",
    "Student Union - Coffee Shop",
    # Add your campus locations...
]
```

### Time Slots

Modify `TIME_SLOTS` in `app.py` for different meeting times:

```python
TIME_SLOTS = [
    "12:00 PM", "1:00 PM", "2:00 PM",
    # Add your preferred times...
]
```

### Academic Years

Update `YEARS` array for your institution's class system:

```python
YEARS = ["Freshman", "Sophomore", "Junior", "Senior", "Graduate"]
```

## Matching Algorithm

The system uses a sophisticated matching algorithm that:

1. **Filters by Preferences**: Only matches users whose gender preferences align
2. **Academic Year Matching**: Matches based on preferred year criteria
3. **Hobby Compatibility**: Calculates shared interest scores for better matching
4. **Weighted Random Selection**: Higher hobby compatibility increases match probability
5. **One-Time Matching**: Each user can only be matched once (prevents duplicate matches)

## Security & Privacy Features

- **Session Management**: User data stored in secure sessions
- **Anonymous IDs**: Random generated IDs protect real identities
- **Data Persistence**: JSON file storage (easily replaceable with database)
- **Input Validation**: All form inputs are validated and sanitized

## Admin Features

Visit `/admin` to access the admin dashboard which shows:

- **System Statistics**: Total users, matches, and success rates
- **User Management**: View all registered users and their status
- **Match Tracking**: Monitor all created matches and meeting details
- **Analytics**: Gender distribution, popular hobbies, and compatibility analysis

## API Endpoints

- `GET /` - Main registration page
- `POST /register` - Submit user registration and find matches
- `GET /check_match` - Check for new matches (AJAX)
- `GET /stats` - Get system statistics (JSON)
- `GET /admin` - Admin dashboard

## Customization Options

### Hobby Scoring

Modify the `calculate_hobby_score()` function to change how hobby compatibility is calculated.

### Matching Weights

Adjust the weighting system in the matching algorithm to prioritize different factors.

### UI Themes

Edit `static/style.css` to customize colors, fonts, and animations.

## Technical Details

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Data Storage**: JSON file (production should use database)
- **Styling**: Modern CSS with animations and responsive design
- **AJAX**: Real-time updates without page refreshes

## Production Deployment

For production use:

1. **Database**: Replace JSON storage with PostgreSQL/MySQL
2. **Security**: Change the secret key and add HTTPS
3. **Hosting**: Deploy on Heroku, AWS, or similar platform
4. **Email**: Add email notifications for matches
5. **Mobile**: Consider a mobile app version

## Demo Data

The system generates realistic demo scenarios:

- Random anonymous IDs (e.g., "DATE4532")
- Campus location suggestions
- Flexible time slots
- Hobby compatibility percentages

## Contributing

Feel free to contribute by:

- Adding new matching criteria
- Improving the UI/UX
- Adding notification systems
- Enhancing the admin dashboard
- Adding mobile responsiveness improvements

## License

This project is open source and available under the MIT License.

---

**Note**: This is designed for educational/campus use. Always ensure compliance with your institution's policies and local privacy laws.
