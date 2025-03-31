# 💪 AI Fitness Chatbot Project

Welcome to the **AI Fitness Chatbot**—your new interactive fitness companion designed to guide you seamlessly toward your health goals! Whether you're looking to shed weight, build muscle, improve your nutrition, or enhance your recovery, our intelligent chatbot is here to help you every step of the way.

---

## 🌟 Features

- **Personalized Fitness Advice**: Get tailored recommendations based on your fitness goals, from weight loss to muscle gain.
- **Smart Chatting**: Powered by OpenAI’s GPT models (GPT-4o-mini), ensuring accurate, insightful, and natural-sounding responses.
- **Interactive Web Interface**: Enjoy a user-friendly experience with modern chat bubbles, a convenient sidebar for conversation history, and a stylish dark mode.
- **Persistent Conversations**: Chat history is saved securely, so your conversations are available anytime you revisit.
- **Robust Error Handling**: Friendly notifications guide you smoothly if something goes wrong, making your interaction seamless.

---

## 🚀 Tech Stack

- **Backend**: Python, Flask
- **AI Integration**: OpenAI GPT-4o-mini
- **Frontend**: HTML, CSS, Flask
- **Database**: SQLite
- **Security & Authentication**: Flask-Login

---

## 🛠️ Technical Details

### Chatbot Logic (`chatbot.py`)
- **Natural Language Understanding**: Classifies user inputs and responds using predefined greetings or dynamically generated responses through OpenAI’s GPT-4o-mini.
- **Contextual Awareness**: Maintains conversation history for coherent and personalized interactions.
- **Error Handling**: Gracefully manages API errors, ensuring users always receive meaningful fitness-related responses.

### Web Interface (`UI.py`)
- **User Authentication**: Securely handles registration and login using hashed passwords with Flask-Login.
- **Session Management**: Utilizes Flask sessions for maintaining chat histories.
- **Profile Management**: Allows users to customize their profiles by uploading profile pictures securely.
- **Conversation Management**: Efficiently manages creating, fetching, and deleting conversation histories, providing a seamless user experience.

---

## 🎯 Recent Improvements

- **Enhanced Personalization**: Responses now dynamically adapt to your fitness goals and preferences.
- **Improved Design**: Sleek, intuitive UI with enhanced visuals.
- **Error Management**: Effective handling and clear communication for smoother user experiences.
- **Persistent Chat History**: Conversations are securely stored, making interactions feel personal and continuous.

---

## 📌 Roadmap & Future Plans

We're continually improving! Upcoming features include:

- 📈 **Progress Tracking**: Visualize your fitness journey with graphs and stats.
- 🌐 **Multilingual Support**: Access advice in various languages.
- 🎙️ **Voice Interaction**: Hands-free chatbot interactions.
- 🐞 **Bug Fixes & Optimizations**: Continued improvements to logic and UI responsiveness.


---

## 🙌 Contributing

Feel free to suggest improvements or open a pull request. Let's make fitness accessible and enjoyable for everyone!


