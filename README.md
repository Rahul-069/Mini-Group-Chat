# Mini-Group-Chat

A **real-time group chat application** built with **Flask** and **Flask-SocketIO**, featuring user login/signup, WebSocket messaging, and a modern responsive UI. Deployed on **Render** with HTTPS automatically handled.

---

## Features

- User authentication: **Login / Sign up**  
- Real-time group chat using **WebSockets**  
- Modern UI with responsive design  
- Online status tracking and system messages  
- Simple backend using **Flask + Flask-SocketIO**  
- No need for SSL certificates locally (Render handles HTTPS)  

---

## Screenshots

**Login Page**  
<img width="1898" height="872" alt="image" src="https://github.com/user-attachments/assets/264151e4-f5b5-40b8-8653-891d2656ffeb" />



**Sign Up Page**  
<img width="1898" height="869" alt="image" src="https://github.com/user-attachments/assets/05cb025c-6c78-444a-9aab-8abb48cf381c" />


**Chat Room**  
<img width="1919" height="856" alt="image" src="https://github.com/user-attachments/assets/31860121-a8cc-45ff-b696-bd11b47f6987" />



---

## Tech Stack

- **Backend:** Python, Flask, Flask-SocketIO  
- **Frontend:** HTML, CSS, JavaScript  
- **Real-time:** WebSockets (Socket.IO)  
- **Deployment:** Render.com  

---

## Installation (Local)

1. Clone the repo:

```bash
git clone https://github.com/YOUR_USERNAME/mini-group-chat.git
cd mini-group-chat
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
python app.py
```

4. Open your browser at http://localhost:5000.
    If running locally, you can optionally use SSL certificates and ssl_context for HTTPS.

## Deployment

The app is deployed on Render.com. 

https://mini-group-chat.onrender.com

Render handles HTTPS automatically, so no need for local SSL certificates.


