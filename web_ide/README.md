# Infrastructure DSL Compiler - Web IDE

A lightweight web-based IDE for the Infrastructure DSL compiler that allows you to write DSL code, compile it, and see the generated JSON output in real-time.

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Navigate to the web IDE directory:**
   ```bash
   cd web_ide
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the web server:**
   ```bash
   python app.py
   ```

4. **Open in browser:**
   ```
   http://localhost:5000
   ```

## 🎯 Features

### **Editor Panel (Left)**
- **Monaco Editor** with custom DSL syntax highlighting
- **Line numbers** and character count
- **Auto-resize** and word wrapping
- **Keyboard shortcuts** (Ctrl+Enter to compile)

### **Output Panel (Right)**
- **Formatted JSON** output display
- **Error messages** with detailed information
- **Copy to clipboard** functionality
- **Status indicators** (Ready/Compiling/Success/Error)

### **User Experience**
- **VS Code light theme** styling
- **Loading indicators** during compilation
- **Error modal** with detailed error analysis
- **Responsive design** for different screen sizes
- **Clean, minimal interface**

## 📝 Usage

### **Writing DSL Code**

The editor comes pre-loaded with an example DSL code:

```dsl
# Infrastructure DSL Example
server "web_server" {
    cpu = 4
    memory = "8GB"
    os = "ubuntu"
}

database "app_db" {
    engine = "mysql"
    storage = "100GB"
    version = "8.0"
}

network "vpc" {
    cidr_block = "10.0.0.0/16"
    public = true
}
```

### **Compiling**

1. **Click the "Compile" button** or press **Ctrl+Enter**
2. **Wait for compilation** (loading indicator shown)
3. **View results** in the right panel:
   - ✅ **Success**: Formatted JSON output
   - ❌ **Error**: Detailed error message with modal

### **Error Handling**

The IDE provides comprehensive error reporting:

- **Syntax Errors**: Line numbers and error descriptions
- **Semantic Errors**: Type mismatches and validation issues
- **Internal Errors**: Server-side problems
- **Network Errors**: Connection issues

## 🛠️ Technical Details

### **Backend Architecture**

- **Flask** web framework
- **RESTful API** endpoint `/compile`
- **Error handling** with proper HTTP status codes
- **CORS support** for cross-origin requests

### **Frontend Architecture**

- **Monaco Editor** for code editing
- **Vanilla JavaScript** (no heavy frameworks)
- **Responsive CSS** with VS Code light theme
- **Async/await** for API calls

### **API Endpoint**

```http
POST /compile
Content-Type: application/json

{
  "code": "<DSL_CODE>"
}
```

**Response:**
```json
{
  "success": true,
  "output": "<JSON_OUTPUT>",
  "message": "Compilation successful"
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Syntax analysis failed",
  "details": ["Line 5: Expected ASSIGN_OP, got INTEGER"],
  "phase": "syntax"
}
```

## 🎨 Customization

### **Adding DSL Syntax Highlighting**

The syntax highlighting is defined in `static/app.js` in the `setupDSLSyntaxHighlighting()` function. You can:

- **Add new keywords** to the tokenizer
- **Modify color schemes** using Monaco Editor themes
- **Add custom language rules** for better highlighting

### **Styling**

The CSS is in `static/style.css` and follows VS Code light theme conventions. You can:

- **Modify colors** in the CSS variables
- **Adjust layout** using flexbox properties
- **Add responsive breakpoints** for different devices

## 🔧 Development

### **Project Structure**

```
web_ide/
├── app.py                 # Flask backend
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Main HTML template
├── static/
│   ├── style.css         # CSS styling
│   └── app.js            # Frontend JavaScript
└── README.md            # This file
```

### **Running in Development**

```bash
# Development mode with auto-reload
python app.py

# The server runs on http://localhost:5000
# Debug mode is enabled by default
```

### **Health Check**

The IDE includes a health check endpoint:

```bash
curl http://localhost:5000/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "Infrastructure DSL Compiler Web IDE",
  "version": "1.0.0"
}
```

## 🐛 Troubleshooting

### **Common Issues**

1. **Port 5000 already in use:**
   ```bash
   # Kill any existing process on port 5000
   # On Windows:
   netstat -ano | findstr :5000
   taskkill /PID <PID> /F
   
   # On macOS/Linux:
   lsof -ti:5000 | xargs kill -9
   ```

2. **Module import errors:**
   ```bash
   # Make sure you're in the correct directory
   cd infrastructure-dsl-compiler/web_ide
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Compiler not working:**
   ```bash
   # Ensure the parent directory has the src/ folder
   ls ../src/
   
   # The backend imports from ../src/
   ```

### **Debug Mode**

The app runs in debug mode by default. You'll see:

- **Detailed error messages** in the terminal
- **Auto-reload** on file changes
- **Stack traces** for debugging

## 🚀 Production Deployment

For production use, consider:

1. **Use a production WSGI server:**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

2. **Disable debug mode:**
   ```python
   app.run(debug=False, host='0.0.0.0', port=5000)
   ```

3. **Add environment variables:**
   ```python
   import os
   port = int(os.environ.get('PORT', 5000))
   app.run(debug=False, host='0.0.0.0', port=port)
   ```

## 📄 License

This project is part of the Infrastructure DSL Compiler educational project.

## 🤝 Contributing

Feel free to contribute improvements:

- **Bug fixes** and **feature enhancements**
- **UI/UX improvements**
- **Performance optimizations**
- **Documentation updates**

---

**Happy coding with your Infrastructure DSL!** 🎉
