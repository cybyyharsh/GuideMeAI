# 🌏 GuideMeAI - India Local AI Guide

Your personal AI-powered guide to explore India with local insights, powered by Ollama.

## 🚀 Quick Start (One Command!)

### Option 1: Python Script (Recommended)
```bash
python start.py
```

### Option 2: Windows Batch File (Double-Click)
Just double-click `START.bat` in Windows Explorer

### Option 3: Manual Start
```bash
python run_full_server.py
```

## ✅ What Happens When You Run `start.py`

The script automatically:
1. ✓ Checks Python version (requires 3.8+)
2. ✓ Verifies all dependencies are installed
3. ✓ Checks if Ollama is running
4. ✓ Validates project structure
5. ✓ Checks if port 5000 is available
6. ✓ Starts the integrated server (Frontend + Backend)
7. ✓ Opens on http://localhost:5000

## 📋 Prerequisites

### 1. Python 3.8+
Check your version:
```bash
python --version
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Ollama (Required for AI Chat)
- **Download**: https://ollama.ai/download
- **Start Ollama**: 
  - Windows: Start from Start Menu or run `ollama serve`
  - Mac/Linux: Run `ollama serve` in terminal
- **Pull the model**:
  ```bash
  ollama pull llama3
  ```

## 🎯 Features

✅ **AI-Powered Chat** - Get local insights about any place in India  
✅ **Interactive Map** - Visual exploration with location markers  
✅ **User Authentication** - Personalized experience with profiles  
✅ **Voice Interaction** - Speech-to-text and text-to-speech  
✅ **Multi-language Support** - Hindi, English, and more  
✅ **Premium UI** - Modern, responsive design with dark mode  

## 📁 Project Structure

```
guideme/
├── start.py              # 🚀 ONE-CLICK STARTUP SCRIPT
├── START.bat             # Windows batch file for easy startup
├── run_full_server.py    # Alternative startup script
├── backend/
│   ├── app.py           # Flask application factory
│   ├── routes/          # API endpoints (chat, auth, map)
│   ├── services/        # Business logic (AI, database, location)
│   └── utils/           # Helper functions
├── frontend/
│   ├── index.html       # Main application page
│   ├── js/              # JavaScript modules
│   └── css/             # Stylesheets
└── requirements.txt     # Python dependencies
```

## 🔧 Configuration

### Environment Variables (Optional)
Create a `.env` file in the root directory:
```env
FLASK_ENV=development
OLLAMA_MODEL=llama3
DATABASE_URL=mysql://user:password@localhost/guideme
```

### Database Setup (Optional)
For full user management features:
```bash
python backend/init_database.py
```

## 🧪 Testing

### Test the Full System
```bash
python start.py
```
Then open http://localhost:5000

### Test Individual Components

**Backend API Only:**
```bash
python backend/app.py
```

**Test Chat Endpoint:**
```bash
python test_chat.py
```

**Test Ollama Connection:**
```bash
python test_ollama_simple.py
```

## 🌐 Usage

1. **Start the server:**
   ```bash
   python start.py
   ```

2. **Open your browser:**
   Navigate to http://localhost:5000

3. **Start exploring:**
   - Click "Sign Up" to create an account (optional)
   - Or continue as guest
   - Ask questions about any place in India
   - Use voice input for hands-free interaction
   - Explore the interactive map

## 💡 Example Queries

- "Tell me about the Taj Mahal"
- "What are the best street foods in Delhi?"
- "Plan a 3-day trip to Rajasthan"
- "What's the weather like in Mumbai?"
- "Recommend temples in South India"

## 🛠️ Troubleshooting

### Server won't start
- **Check Python version**: Must be 3.8 or higher
- **Install dependencies**: `pip install -r requirements.txt`
- **Port 5000 in use**: Close other applications using port 5000

### Chat not working
- **Ollama not running**: Start Ollama with `ollama serve`
- **Model not found**: Pull the model with `ollama pull llama3`
- **Check Ollama**: Visit http://localhost:11434/api/tags

### Frontend not loading
- **Clear browser cache**: Hard refresh with Ctrl+F5
- **Check console**: Open browser DevTools (F12) for errors
- **Verify files**: Ensure `frontend/index.html` exists

### Database errors
- **Demo mode**: The app works without a database
- **Full setup**: Run `python backend/init_database.py`
- **Check credentials**: Verify `.env` file settings

## 📚 Documentation

- [Quick Start Guide](QUICK_START_GUIDE.md)
- [Database Setup](DATABASE_SETUP_GUIDE.md)
- [User Management](USER_MANAGEMENT_GUIDE.md)

## 🎨 Tech Stack

- **Backend**: Flask, Python 3.8+
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **AI**: Ollama (llama3)
- **Database**: MySQL (optional)
- **Maps**: Leaflet.js

## 🤝 Contributing

This is a personal project, but suggestions are welcome!

## 📄 License

MIT License - Feel free to use and modify

## 🙏 Acknowledgments

- Ollama for local AI capabilities
- OpenStreetMap for map data
- Flask community for excellent documentation

---

## 🎉 That's It!

Just run `python start.py` and you're ready to explore India with AI! 🚀

**Need help?** Check the troubleshooting section above or review the detailed guides in the docs folder.