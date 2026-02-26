from flask import Flask, render_template, request, jsonify, session
import json
import random
import uuid
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-this-in-production')

# Data storage file
DATA_FILE = 'data.json'

# College locations for meetups
MEETING_LOCATIONS = [
    "Library ",
    "khem  ji",
    "Parking Lot",
    "TC",
    "Basketball Court",
    "Campus Garden - Bench Area"
]

# Available time slots (assuming weekdays 12PM-8PM)
TIME_SLOTS = [
    "12:00 PM", "1:00 PM", "2:00 PM", "3:00 PM"
]

# Available years
YEARS = ["1st Year", "2nd Year", "3rd year", "4th Year", "Graduate"]

def load_data():
    """Load user data from JSON file"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except:
            return {"users": [], "matches": []}
    return {"users": [], "matches": []}

def save_data(data):
    """Save user data to JSON file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def calculate_hobby_score(user1_hobbies, user2_hobbies):
    """Calculate compatibility score based on shared hobbies"""
    hobbies1 = set(hobby.strip().lower() for hobby in user1_hobbies.split(','))
    hobbies2 = set(hobby.strip().lower() for hobby in user2_hobbies.split(','))
    
    shared = len(hobbies1.intersection(hobbies2))
    total = len(hobbies1.union(hobbies2))
    
    if total == 0:
        return 0
    return shared / total

def find_matches(user):
    """Find potential matches for a user"""
    data = load_data()
    users = data["users"]
    matches = data["matches"]
    
    # Get list of already matched user IDs
    matched_users = set()
    for match in matches:
        matched_users.add(match["user1_id"])
        matched_users.add(match["user2_id"])
    
    potential_matches = []
    
    for potential_match in users:
        # Skip if same user or already matched
        if (potential_match["id"] == user["id"] or 
            potential_match["id"] in matched_users):
            continue
            
        # Check gender compatibility
        if (user["preferred_gender"] == potential_match["gender"] and 
            potential_match["preferred_gender"] == user["gender"] and
            user["preferred_year"] == potential_match["year"]):
            
            # Calculate hobby compatibility score
            hobby_score = calculate_hobby_score(user["hobbies"], potential_match["hobbies"])
            
            potential_matches.append({
                "match": potential_match,
                "hobby_score": hobby_score
            })
    
    return potential_matches

def create_match(user1, user2):
    """Create a match between two users"""
    data = load_data()
    
    # Generate anonymous IDs
    anonymous_id1 = f"DATE{random.randint(1000, 9999)}"
    anonymous_id2 = f"DATE{random.randint(1000, 9999)}"
    
    # Pick random location (time will be negotiated by users)
    location = random.choice(MEETING_LOCATIONS)
    
    # Create match record with negotiation features
    match = {
        "id": str(uuid.uuid4()),
        "user1_id": user1["id"],
        "user2_id": user2["id"],
        "user1_anonymous_id": anonymous_id1,
        "user2_anonymous_id": anonymous_id2,
        "location": location,
        "date": (datetime.now() + timedelta(days=random.randint(1, 7))).strftime("%Y-%m-%d"),
        "created_at": datetime.now().isoformat(),
        # Time negotiation features
        "time_status": "pending",  # pending, proposed, accepted, counter_proposed
        "proposed_time": None,
        "proposed_by": None,
        "time_history": [],
        # Chat features
        "chat_messages": [],
        "chat_enabled": True
    }
    
    data["matches"].append(match)
    save_data(data)
    
    return match

@app.route('/')
def index():
    """Home page with registration form"""
    return render_template('index.html', years=YEARS)

@app.route('/register', methods=['POST'])
def register():
    """Handle user registration"""
    try:
        # Get form data
        gender = request.form.get('gender')
        preferred_gender = request.form.get('preferred_gender')
        year = request.form.get('year')
        preferred_year = request.form.get('preferred_year')
        hobbies = request.form.get('hobbies')
        contact_info = request.form.get('contact_info')
        
        # Validate required fields
        if not all([gender, preferred_gender, year, preferred_year, hobbies]):
            return jsonify({"error": "All fields are required"}), 400
        
        # Create user object
        user = {
            "id": str(uuid.uuid4()),
            "gender": gender,
            "preferred_gender": preferred_gender,
            "year": year,
            "preferred_year": preferred_year,
            "hobbies": hobbies,
            "contact_info": contact_info,
            "created_at": datetime.now().isoformat()
        }
        
        # Load data and add user
        data = load_data()
        data["users"].append(user)
        save_data(data)
        
        # Store user ID in session
        session['user_id'] = user['id']
        
        # Try to find matches immediately
        potential_matches = find_matches(user)
        
        if potential_matches:
            # Sort by hobby compatibility (higher score = better match)
            potential_matches.sort(key=lambda x: x["hobby_score"], reverse=True)
            
            # Add randomness - higher hobby scores get better chances
            weights = []
            for i, match in enumerate(potential_matches):
                # Base weight + bonus for hobby compatibility
                weight = 1 + (match["hobby_score"] * 3)
                weights.append(weight)
            
            # Weighted random selection
            if weights:
                selected_match = random.choices(potential_matches, weights=weights)[0]
                match_record = create_match(user, selected_match["match"])
                
                return jsonify({
                    "status": "matched",
                    "anonymous_id": match_record["user2_anonymous_id"],
                    "location": match_record["location"],
                    "time": match_record["time"],
                    "date": match_record["date"],
                    "hobby_compatibility": f"{selected_match['hobby_score']:.0%}"
                })
        
        return jsonify({"status": "waiting", "message": "You're in the system! We'll notify you when a match is found."})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/check_match')
def check_match():
    """Check if user has been matched and get match details"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "User not found"}), 400
    
    data = load_data()
    
    for match in data["matches"]:
        if match["user1_id"] == user_id:
            return jsonify({
                "status": "matched",
                "match_id": match["id"],
                "anonymous_id": match["user2_anonymous_id"],
                "location": match["location"],
                "date": match["date"],
                "time_status": match.get("time_status", "pending"),
                "proposed_time": match.get("proposed_time"),
                "proposed_by": match.get("proposed_by"),
                "is_proposer": match.get("proposed_by") == user_id,
                "chat_enabled": match.get("chat_enabled", True)
            })
        elif match["user2_id"] == user_id:
            return jsonify({
                "status": "matched",
                "match_id": match["id"],
                "anonymous_id": match["user1_anonymous_id"],
                "location": match["location"],
                "date": match["date"],
                "time_status": match.get("time_status", "pending"),
                "proposed_time": match.get("proposed_time"),
                "proposed_by": match.get("proposed_by"),
                "is_proposer": match.get("proposed_by") == user_id,
                "chat_enabled": match.get("chat_enabled", True)
            })
    
    return jsonify({"status": "waiting"})

@app.route('/propose_time', methods=['POST'])
def propose_time():
    """User proposes a meeting time"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "User not found"}), 400
    
    data = request.get_json()
    proposed_time = data.get('time')
    
    if not proposed_time:
        return jsonify({"error": "Time is required"}), 400
    
    # Find user's match
    match_data = load_data()
    user_match = None
    
    for match in match_data["matches"]:
        if match["user1_id"] == user_id or match["user2_id"] == user_id:
            user_match = match
            break
    
    if not user_match:
        return jsonify({"error": "No match found"}), 404
    
    # Update time proposal
    user_match["proposed_time"] = proposed_time
    user_match["proposed_by"] = user_id
    user_match["time_status"] = "proposed"
    
    # Add to history
    if "time_history" not in user_match:
        user_match["time_history"] = []
    
    user_match["time_history"].append({
        "time": proposed_time,
        "proposed_by": user_id,
        "timestamp": datetime.now().isoformat(),
        "action": "proposed"
    })
    
    save_data(match_data)
    return jsonify({"status": "success", "message": "Time proposed successfully"})

@app.route('/respond_time', methods=['POST'])
def respond_time():
    """User responds to a time proposal (accept or counter-propose)"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "User not found"}), 400
    
    data = request.get_json()
    action = data.get('action')  # 'accept' or 'counter'
    new_time = data.get('time')  # required for counter
    
    if action not in ['accept', 'counter']:
        return jsonify({"error": "Invalid action"}), 400
    
    if action == 'counter' and not new_time:
        return jsonify({"error": "Time is required for counter-proposal"}), 400
    
    # Find user's match
    match_data = load_data()
    user_match = None
    
    for match in match_data["matches"]:
        if match["user1_id"] == user_id or match["user2_id"] == user_id:
            user_match = match
            break
    
    if not user_match:
        return jsonify({"error": "No match found"}), 404
    
    # Check if user is not the proposer
    if user_match.get("proposed_by") == user_id:
        return jsonify({"error": "Cannot respond to your own proposal"}), 400
    
    if action == 'accept':
        user_match["time_status"] = "accepted"
        user_match["time"] = user_match["proposed_time"]  # Set final time
        
        # Add to history
        user_match["time_history"].append({
            "time": user_match["proposed_time"],
            "proposed_by": user_id,
            "timestamp": datetime.now().isoformat(),
            "action": "accepted"
        })
        
        message = "Time accepted! Your date is confirmed."
        
    else:  # counter
        user_match["proposed_time"] = new_time
        user_match["proposed_by"] = user_id
        user_match["time_status"] = "counter_proposed"
        
        # Add to history
        user_match["time_history"].append({
            "time": new_time,
            "proposed_by": user_id,
            "timestamp": datetime.now().isoformat(),
            "action": "counter_proposed"
        })
        
        message = "Counter-proposal sent!"
    
    save_data(match_data)
    return jsonify({"status": "success", "message": message})

@app.route('/send_message', methods=['POST'])
def send_message():
    """Send a chat message to matched user"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "User not found"}), 400
    
    data = request.get_json()
    message_text = data.get('message', '').strip()
    
    if not message_text:
        return jsonify({"error": "Message cannot be empty"}), 400
    
    if len(message_text) > 500:
        return jsonify({"error": "Message too long (max 500 characters)"}), 400
    
    # Find user's match
    match_data = load_data()
    user_match = None
    
    for match in match_data["matches"]:
        if match["user1_id"] == user_id or match["user2_id"] == user_id:
            user_match = match
            break
    
    if not user_match:
        return jsonify({"error": "No match found"}), 404
    
    if not user_match.get("chat_enabled", True):
        return jsonify({"error": "Chat is disabled for this match"}), 403
    
    # Add message
    if "chat_messages" not in user_match:
        user_match["chat_messages"] = []
    
    message = {
        "id": str(uuid.uuid4()),
        "sender_id": user_id,
        "message": message_text,
        "timestamp": datetime.now().isoformat(),
        "read": False
    }
    
    user_match["chat_messages"].append(message)
    
    save_data(match_data)
    return jsonify({"status": "success", "message": "Message sent"})

@app.route('/get_messages')
def get_messages():
    """Get chat messages for matched user"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "User not found"}), 400
    
    # Find user's match
    match_data = load_data()
    user_match = None
    
    for match in match_data["matches"]:
        if match["user1_id"] == user_id or match["user2_id"] == user_id:
            user_match = match
            break
    
    if not user_match:
        return jsonify({"error": "No match found"}), 404
    
    # Get messages and mark as read for this user
    messages = user_match.get("chat_messages", [])
    
    # Mark messages as read
    for msg in messages:
        if msg["sender_id"] != user_id:
            msg["read"] = True
    
    save_data(match_data)
    
    # Return messages with anonymized sender info
    chat_messages = []
    for msg in messages:
        is_own_message = msg["sender_id"] == user_id
        chat_messages.append({
            "id": msg["id"],
            "message": msg["message"],
            "timestamp": msg["timestamp"],
            "is_own": is_own_message,
            "sender": "You" if is_own_message else "Your Match"
        })
    
    return jsonify({"messages": chat_messages})

@app.route('/stats')
def stats():
    """Display system statistics"""
    data = load_data()
    return jsonify({
        "total_users": len(data["users"]),
        "total_matches": len(data["matches"]),
        "waiting_users": len(data["users"]) - (len(data["matches"]) * 2)
    })

@app.route('/cancel_match', methods=['POST'])
def cancel_match():
    """Cancel matchmaking and clear user session"""
    user_id = session.get('user_id')
    if user_id:
        data = load_data()
        
        # Remove user from users list if they haven't been matched yet
        data['users'] = [user for user in data['users'] if user['id'] != user_id]
        
        # Remove any existing matches for this user
        data['matches'] = [match for match in data['matches'] 
                          if match['user1_id'] != user_id and match['user2_id'] != user_id]
        
        save_data(data)
    
    # Clear session
    session.clear()
    return jsonify({"status": "cancelled"})

@app.route('/admin')
def admin():
    """Admin page to view all data (for testing)"""
    data = load_data()
    return render_template('admin.html', data=data)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('FLASK_ENV') == 'development')