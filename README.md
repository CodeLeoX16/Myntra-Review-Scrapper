# 🛍️ Myntra Review Scraper System

A powerful, intelligent web scraping and analytics platform that extracts customer reviews from Myntra and provides comprehensive sentiment analysis and insights. Built with Streamlit, Selenium, and MongoDB.

## 📚 Table of Contents
- [Features](#features)
- [Project Overview](#project-overview)
- [System Requirements](#system-requirements)
- [Installation Guide](#installation-guide)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)

---

## ✨ Features

### 🔍 **Smart Scraping**
- Extract reviews directly from Myntra with just a product name
- Handle multiple products in a single scraping session
- Intelligent pagination and dynamic content loading
- Automatic headless browser management

### 📊 **Advanced Analytics**
- **Rating Distribution Charts** - Visualize customer sentiments
- **Product Comparison** - Compare ratings and prices across products
- **User Analytics** - Track top reviewers and their patterns
- **Comment Analysis** - Statistical analysis of review lengths
- **Interactive Dashboards** - Drill down into review details

### 💾 **Data Management**
- Automatic MongoDB integration for data persistence
- CSV export functionality for offline analysis
- Session-based local storage fallback (when DB unavailable)
- Structured data format for easy analysis

### 🎨 **Beautiful UI**
- Modern, responsive Streamlit interface
- Dark-themed sidebar with high contrast buttons
- Interactive Plotly charts and visualizations
- Smooth, intuitive user experience

---

## 📖 Project Overview

This project provides a complete end-to-end solution for:

1. **Data Collection** - Scrape Myntra reviews using Selenium + BeautifulSoup
2. **Data Storage** - Store reviews in MongoDB or local session
3. **Data Analysis** - Generate instant analytics and insights
4. **Data Visualization** - Beautiful interactive dashboards

### What Makes It Special?
- ✅ No manual data entry required
- ✅ Real-time analysis and charts
- ✅ Handles network/DNS issues gracefully
- ✅ Production-ready error handling
- ✅ Professional UI with dark theme support

---

## 🖥️ System Requirements

### Minimum Requirements
- **Python:** 3.10+
- **RAM:** 4GB
- **Storage:** 500MB free space
- **OS:** Windows, macOS, or Linux

### Required Tools
- Git (for cloning repository)
- Chrome/Chromium browser (for web scraping)
- MongoDB account (free tier: atlas.mongodb.com)

---

## 🚀 Installation Guide

### Step 1: Clone the Repository
```bash
git clone https://github.com/PWskills-DataScienceTeam/myntra-review-scrapper.git
cd myntra-review-scrapper
```

### Step 2: Create Python Virtual Environment

**Using Conda (Recommended):**
```bash
conda create -p ./MyntraVenv python=3.10 -y
conda activate ./MyntraVenv
```

**Or Using venv:**
```bash
python -m venv MyntraVenv
# On Windows:
MyntraVenv\Scripts\activate
# On macOS/Linux:
source MyntraVenv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

**Main Dependencies Installed:**
- `streamlit==1.28.0` - Web framework for the dashboard
- `selenium==4.15.2` - Browser automation for scraping
- `bs4==0.0.1` - HTML parsing
- `pandas` - Data manipulation
- `plotly==5.18.0` - Interactive charts
- `pymongo` - MongoDB connection (via database-connect)
- `python-dotenv==1.0.1` - Environment variable management

### Step 4: Configure Environment Variables

Create a `.env` file in the project root directory:
```bash
cp .env.example .env
```

Edit `.env` and add your MongoDB connection string:
```env
MONGODB_URL="mongodb+srv://username:password@cluster0.mongodb.net/"
```

**How to get MongoDB connection string:**
1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a free account and cluster
3. Click "Connect" → "Drivers" → Copy the Python connection string
4. Replace `<password>` with your actual password
5. Paste into `.env` file

**IMPORTANT:** Keep your `.env` file secure and never commit it to Git!

### Step 5: Run the Application
```bash
streamlit run app.py
```

The application will open automatically at `http://localhost:8501`

---

## ⚙️ Configuration

### MongoDB Setup (Important!)

#### Option A: Using MongoDB Atlas (Cloud - Recommended)
1. Create account at [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
2. Create a free cluster
3. Create database user with strong password
4. Get connection string from "Connect" button
5. Add to `.env`: `MONGODB_URL="mongodb+srv://user:password@cluster.mongodb.net/"`

#### Option B: Using Local MongoDB
If you have MongoDB installed locally:
```env
MONGODB_URL="mongodb://localhost:27017/"
```

### .env File Template
```env
# MongoDB Connection String
MONGODB_URL="mongodb+srv://username:password@cluster0.h3tiakx.mongodb.net/"

# Optional: Fallback URI if primary fails
MONGODB_FALLBACK_URL=""
```

---

## 📱 Usage Guide

### Search & Scrape Reviews

1. **Open the application** at `http://localhost:8501`
2. **Enter product name** (e.g., "blue shirt", "running shoes")
3. **Set number of products** to scrape (1-20)
4. **Click "🚀 Start Scraping"**
5. **Watch the progress bar** as reviews are collected
6. **View statistics** - Total reviews, average rating, unique users
7. **Download CSV** - Export data for offline use

### Analyze Reviews

1. Go to **"Analysis"** page in sidebar
2. Select from tabs:
   - **📋 Full Data** - See all reviews in table format
   - **🔍 Detailed View** - Search and filter individual reviews
   - **📊 Analytics** - Charts and visualizations
   - **🎯 Analysis** - Generate comprehensive reports

### Key Features

**Search Function:**
- Filter reviews by product name, user name, rating, or comment text
- Expandable cards for easy reading
- Quick access to review details

**Analytics Dashboard:**
- Interactive Plotly charts
- Rating distribution histogram
- Product comparison
- Top users leaderboard
- Comment length statistics

**Full Analysis Report:**
- Average pricing by product
- Rating comparisons
- Top positive/negative reviews
- Rating category breakdown

---

## 📁 Project Structure

```
MyntraReviewScrapperSystem/
├── app.py                          # Main Streamlit application
├── .env                            # Environment variables (CREATE THIS)
├── .env.example                    # Example env file
├── requirements.txt                # Python dependencies
├── README.md                       # This file
│
├── pages/
│   └── generate_analysis.py        # Analysis dashboard page
│
├── src/
│   ├── __init__.py
│   ├── constants/                  # Configuration constants
│   │   └── __init__.py
│   ├── exception.py                # Custom exception handling
│   ├── scrapper/
│   │   └── scrape.py              # Web scraping logic
│   ├── cloud_io/
│   │   └── __init__.py            # MongoDB operations
│   ├── utils/
│   │   └── __init__.py            # Helper functions
│   └── data_report/
│       └── generate_data_report.py # Analysis report generation
│
├── static/
│   └── css/                        # Custom styling
│
└── templates/                      # Flask HTML templates (legacy)
```

---

## 🐛 Troubleshooting

### Problem: "Environment key: MONGODB_URL is not set"
**Solution:**
1. Create `.env` file in project root
2. Add: `MONGODB_URL="your_connection_string_here"`
3. Restart Streamlit

### Problem: "DNS operation timed out"
**Solution:**
1. Check your internet connection
2. MongoDB Atlas may be down - try again later
3. Or add standard connection URI (non-SRV) to `.env`:
   ```env
   MONGODB_FALLBACK_URL="mongodb://user:password@host1,host2,host3/"
   ```

### Problem: "list index out of range"
**Solution:**
1. The search product might not have enough reviews
2. Try searching with different keywords
3. Check Myntra website to confirm product exists

### Problem: Chrome browser doesn't open
**Solution:**
1. Ensure Chrome/Chromium is installed
2. Update Selenium: `pip install --upgrade selenium`
3. Run with: `streamlit run app.py`

### Problem: "Unable to display rating distribution"
**Solution:**
1. Make sure you have at least 1 review scraped
2. Check Plotly is installed: `pip install plotly==5.18.0`
3. Restart Streamlit

### Can't connect to MongoDB?
**Possible causes:**
- Wrong connection string
- MongoDB cluster not running
- IP not whitelisted (Atlas)
- Network firewall blocking access

**Fix:**
1. Test connection string in MongoDB Compass
2. Ensure cluster is active in Atlas
3. Add your IP to IP whitelist in Atlas
4. Check network connectivity

---

## 🛠️ Technologies Used

| Technology | Purpose | Version |
|-----------|---------|---------|
| **Python** | Core language | 3.10+ |
| **Streamlit** | Web framework/UI | 1.28.0 |
| **Selenium** | Browser automation | 4.15.2 |
| **BeautifulSoup** | HTML parsing | 4.0+ |
| **Pandas** | Data processing | Latest |
| **Plotly** | Interactive charts | 5.18.0 |
| **MongoDB** | Database | Cloud Atlas |
| **python-dotenv** | Env variable management | 1.0.1 |

---

## 📊 Sample Data Schema

Reviews are stored with this structure:
```json
{
  "Product Name": "Blue Cotton Shirt",
  "Over_All_Rating": 4.5,
  "Price": "₹899",
  "Date": "2024-02-15",
  "Rating": "5★",
  "Name": "John Doe",
  "Comment": "Great quality and perfect fit!"
}
```

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 Important Notes

⚠️ **Ethical Scraping:**
- Only scrape data for legitimate analysis purposes
- Respect Myntra's terms of service
- Don't overload servers with too many requests
- Consider using Myntra's official API if available

⚠️ **Security:**
- Never commit `.env` file to Git
- Keep MongoDB credentials safe
- Use strong passwords for MongoDB
- Use IP whitelisting in MongoDB Atlas

⚠️ **Legal Disclaimer:**
- Web scraping may violate Terms of Service
- Use this tool responsibly and legally
- Project is for educational purposes only
- Always check website's robots.txt and terms

---

## 📧 Support & Feedback

- **Issues:** Open an issue on GitHub
- **Questions:** Check existing issues first
- **Suggestions:** Feel free to contribute improvements

---

## 📄 License

This project is for educational purposes.

---

## 👏 Acknowledgments

- **Myntra** - Data source
- **Streamlit** - Web framework
- **MongoDB** - Database solution
- **PWskills** - Project template foundation

---

## 🚀 Quick Start Checklist

- [ ] Clone repository
- [ ] Create virtual environment
- [ ] Install dependencies with `pip install -r requirements.txt`
- [ ] Create `.env` file with MongoDB URL
- [ ] Run `streamlit run app.py`
- [ ] Open browser to `http://localhost:8501`
- [ ] Enter a product name and start scraping!

---

**Happy Scraping!** 🕵️‍♂️🛍️📊

*For the latest updates and documentation, visit the GitHub repository.*