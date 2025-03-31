import os
from flask import Flask, render_template, redirect, url_for, flash, request, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import (UserMixin, login_user, LoginManager, login_required, current_user, logout_user)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from chatbot import get_chat_response
from dotenv import load_dotenv


load_dotenv()

#Flask App Config
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fitness_chatbot.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'images', 'profile_pictures')

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


#Models & Helpers
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    profile_picture = db.Column(db.String(150), default='default.png')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#Routes

@app.route('/')
@login_required
def home():
    return render_template('index.html')


# Authentication
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash('Username already exists. Please choose a different one.', 'warning')
            return redirect(url_for('register'))

        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


@app.route('/change_profile_picture', methods=['GET', 'POST'])
@login_required
def change_profile_picture():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            file.save(file_path)

            current_user.profile_picture = filename
            db.session.commit()

            flash('Profile picture updated successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid file type. Only PNG, JPG, JPEG, or GIF allowed.', 'danger')
            return redirect(request.url)

    return render_template('change_profile_picture.html')


# Conversation Endpoints

@app.route('/get_conversations', methods=['GET'])
@login_required
def get_conversations():
    conversations = session.get('conversations', [])
    return jsonify({"conversations": conversations})


@app.route('/get_conversation/<int:conversation_id>', methods=['GET'])
@login_required
def get_conversation_by_id(conversation_id):

    conversations = session.get('conversations', [])
    conv = next((c for c in conversations if c["id"] == conversation_id), None)
    if not conv:
        return jsonify({"error": "Invalid conversation ID"}), 400

    # Return only the history, no processing
    return jsonify({"history": conv["history"]})

@app.route('/get_response', methods=['POST'])
@login_required
def get_response():
    data = request.get_json()
    user_message = data.get('message', '').strip()
    conversation_id = data.get('conversation_id', None)

    if not user_message:
        return jsonify({"message": "Please enter a message."}), 400

    if 'conversations' not in session:
        session['conversations'] = []

    conversations = session['conversations']

    # Find or create the conversation
    conv = None
    if conversation_id:
        conv = next((c for c in conversations if c["id"] == conversation_id), None)

    if conv is None:
        new_id = len(conversations) + 1
        conv = {
            "id": new_id,
            "name": f"Conversation {new_id}",
            "history": []
        }
        conversations.append(conv)
        session['conversations'] = conversations

    # Append the user message here (only once)
    if not conv["history"] or conv["history"][-1]["content"] != user_message or conv["history"][-1]["role"] != "user":
        conv["history"].append({"role": "user", "content": user_message})

    # Now call get_chat_response, where we REMOVE the user append
    assistant_reply, updated_history = get_chat_response(user_message, conv["history"])

    # Update history in the session
    conv["history"] = updated_history
    session['conversations'] = conversations

    return jsonify({
        "message": assistant_reply,
        "conversation_id": conv["id"]
    })


# New Conversation (No Deletion)

@app.route('/new_conversation', methods=['POST'])
@login_required
def new_conversation():
    """
    Creates a brand new conversation without deleting the old ones.
    """
    conversations = session.get('conversations', [])

    # Determine new conversation ID
    if conversations:
        new_id = max(conv['id'] for conv in conversations) + 1
    else:
        new_id = 1

    new_name = f"Conversation {new_id}"
    new_conv = {
        "id": new_id,
        "name": new_name,
        "history": []
    }

    conversations.append(new_conv)
    session['conversations'] = conversations

    return jsonify({
        "message": f"New conversation created: {new_name}",
        "conversation_id": new_id,
        "conversation_name": new_name
    })


# Delete Conversation

@app.route('/delete_conversation/<int:conversation_id>', methods=['POST'])
@login_required
def delete_conversation(conversation_id):
    """
    Removes a specific conversation from session.
    """
    conversations = session.get('conversations', [])
    original_length = len(conversations)

    # Filter out the conversation we want to delete
    updated = [c for c in conversations if c['id'] != conversation_id]
    session['conversations'] = updated

    if len(updated) < original_length:
        return jsonify({"message": f"Conversation {conversation_id} deleted."})
    else:
        return jsonify({"error": f"No conversation found with ID {conversation_id}."}), 404




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
