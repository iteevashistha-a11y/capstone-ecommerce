# VS Code Quick Start - Running the Presentation App

## 🚀 3-Step Quick Start (Copy & Paste)

### Step 1: Open Terminal in VS Code
```
View → Terminal → New Terminal
(Or press: Ctrl + ` on Windows/Linux, Cmd + ` on Mac)
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

**Expected Output:**
```
Successfully installed streamlit-1.32.0 plotly-5.18.0 pandas-2.0.0 ...
```

### Step 3: Run the App
```bash
streamlit run presentation_app.py
```

**Expected Output:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

Your browser should automatically open. If not, **click the URL above**.

---

## 🎯 What You'll See

Once the app loads, you'll see:

1. **Left Sidebar**: Navigation menu with 8 sections
2. **Logo**: E-commerce icon
3. **Main Content**: Interactive presentation with charts and analysis

Navigate using the sidebar:
- 🏠 Home
- 📊 Market Analysis
- 💰 Financial Analysis
- 🔧 Technical Implementation
- 📝 Use Cases
- 🚀 Go-to-Market Strategy
- 📈 Competitive Analysis
- ✅ Success Metrics

---

## ✅ Troubleshooting in VS Code

### If you see: "command not found: streamlit"

**Solution:**
```bash
# Make sure pip is pointing to the right Python
python -m pip install streamlit

# Then run with:
python -m streamlit run presentation_app.py
```

### If you see: "ModuleNotFoundError: No module named 'plotly'"

**Solution:**
```bash
# Install all dependencies at once
pip install streamlit plotly pandas numpy streamlit-option-menu
```

### If the app loads but charts are blank

**Solution  1:** Hard refresh browser (Cmd+Shift+R or Ctrl+Shift+R)

**Solution 2:** Clear app cache
```bash
# Stop the app (Press Ctrl+C in terminal)
rm -rf ~/.streamlit/cache
streamlit run presentation_app.py
```

### If port 8501 is already in use

**Solution:**
```bash
# Use a different port
streamlit run presentation_app.py --server.port 8502
```

---

## 📁 File Structure in VS Code

You should see:
```
CAPSTONPROJECT-E-COMMERCEIMAGESGLT/
├── presentation_app.py              ← Main file to run
├── requirements.txt                 ← Dependencies
├── agents/
│   ├── market_agent.py
│   ├── financial_agent.py
│   ├── technical_agent.py
│   ├── usecase_agent.py
│   └── strategy_agent.py
├── utils/
│   ├── visualizations.py
│   └── data_processor.py
└── README_PRESENTATION_APP.md       ← Full documentation
```

---

## 🔄 How to Reload Changes

If you edit any `agents/` files:

1. **The app will auto-reload** - You'll see "Reloading script" in the browser
2. Check the browser for updates
3. If it doesn't work, press **R** in the terminal, or manually refresh the app

---

## 📊 Pro Tips

### Tip 1: View Multiple Tabs
- Run the app
- Open http://localhost:8501 in multiple browser tabs
- Keep one for exploring, one for presenting

### Tip 2: Share Live
Others can access:
- Same network: `http://[your-machine-ip]:8501`
- Remote: Use Streamlit Cloud or expose via ngrok

### Tip 3: Full Screen Mode
- F11 in browser for presentation mode
- Chrome: Click the square icon (top right) for full screen

### Tip 4: Dark Mode
- Settings (gear icon, top right) → Theme → Dark

---

## 🎨 Customizing the Presentation

### To Edit Market Data:
```
agents/market_agent.py
- Edit: get_market_analysis()
- Change TAM/SAM/SOM values
- Add/remove market segments
```

### To Edit Financial Projections:
```
agents/financial_agent.py
- Edit: get_financial_projections()
- Change revenue numbers
- Update pricing tiers
```

### To Edit Use Cases:
```
agents/usecase_agent.py
- Edit: get_use_cases()
- Add new customer scenarios
- Update financial impacts
```

### To Add New Sections:
1. Create new agent module in `agents/`
2. Add `from agents import new_agent` at top of `presentation_app.py`
3. Find this section in `presentation_app.py`:
   ```python
   elif selected == "📈 Competitive Analysis":
   ```
4. Add your section before it:
   ```python
   elif selected == "📋 New Section":
       st.header("📋 New Section Title")
       # Your content here
   ```

---

## 🐍 Python Version Check

Make sure you have Python 3.8+:

```bash
python --version
```

If you have multiple Python versions:
```bash
python3 --version  # Try Python 3
```

---

## 📱 Responsive Design

The app works on:
- ✅ Desktop (optimized for 1920x1080+)
- ✅ Laptop (1366x768+)
- ✅ Tablet (in landscape mode)
- ⚠️ Mobile (limited)

For best experience, use on desktop/laptop.

---

## 🔐 No Internet Required

Once the app is running, you can:
1. Close the internet connection
2. Refresh your browser
3. The app still works (all data is local)

---

## 📚 Information Architecture

The entire presentation is organized as:

```
STRATEGY LAYER (Agent: Strategy)
├── Go-to-Market (3 phases)
├── Pricing Strategies
└── Success Metrics

MARKET LAYER (Agent: Market)
├── TAM/SAM/SOM Analysis
├── Segment Breakdown
└── Competitive Advantages

FINANCIAL LAYER (Agent: Financial)
├── Revenue Projections
├── Unit Economics
└── Customer Payback

TECHNICAL LAYER (Agent: Technical)
├── Technology Stack
├── Implementation Phases
└── Performance Specs

VALIDATION LAYER (Agent: Use Cases)
├── 5 Real Scenarios
├── ROI Analysis
└── Example Outputs
```

---

## 🎯 Next Steps After Viewing

1. **Export/Print**: Take screenshots of key sections
2. **Share**: Send the VS Code folder to others (they run same commands)
3. **Present**: Full screen mode for presentations
4. **Customize**: Edit agents/ files for your specific metrics
5. **Deploy**: Push to Streamlit Cloud for live sharing

---

## 🚨 Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| App won't start | `pip install --upgrade -r requirements.txt` |
| Blank charts | Refresh browser + clear cache |
| Terminal error | Check Python version (`python --version`) |
| Port in use | Use different port: `streamlit run ... --server.port 8502` |
| Slow performance | Close other apps, restart terminal |
| Can't find agents folder | Make sure you're in correct directory |

---

## 💾 Saving/Backing Up

The presentation is just code, so you can:

1. **Version control**: `git init` → `git add .` → `git commit -m "initial"`
2. **Cloud backup**: Push to GitHub, GitLab, etc.
3. **Share**: Email the folder to anyone with Python
4. **Update**: Edit any agent files locally, changes reflect on next run

---

## 🎓 Learning the Codebase

### Main Entry Point
- File: `presentation_app.py`
- Lines to understand: Look for `elif selected ==` statements (each is a section)

### Agent Modules
- Each agent is in `agents/` folder
- Each has a `get_*()` function that returns data
- Data is Python dicts/lists (easy to modify)

### Utilities
- Visualization helpers in `utils/visualizations.py`
- Data processing in `utils/data_processor.py`

### Easy Edits
- Change numbers in agent files
- Add new metrics to dataframes
- Modify chart colors (in visualizations.py)

---

## ✨ Advanced: Deploy to Streamlit Cloud

1. Push to GitHub
2. Go to streamlit.io
3. Click "Deploy" → Select your repo
4. App is live at `your-username.streamlit.app`

Anyone in the link can view (no installation needed!)

---

**Status**: ✅ Ready to Run
**Time to First Load**: ~30 seconds after `streamlit run`
**Last Tested**: March 28, 2026

---

**Questions?** Check README_PRESENTATION_APP.md for detailed documentation!
