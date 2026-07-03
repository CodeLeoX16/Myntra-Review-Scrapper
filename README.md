# 🛍️ Myntra Review Scraper

A web scraping application built using **Python**, **Selenium**, **BeautifulSoup**, and **Streamlit** that collects customer reviews from Myntra products and displays useful insights in an interactive dashboard.

The project stores scraped reviews in **MongoDB Atlas** and allows users to analyze customer feedback, ratings, and review patterns through simple visualizations.

---

## 🚀 Live Demo

**Live Application**

https://myntra-review-scrapper-h8ewjgrnqspobh5wcnkaxi.streamlit.app/generate_analysis

---

# 📌 Project Overview

Customer reviews play an important role in understanding product quality and customer satisfaction. Reading hundreds of reviews manually is difficult and time-consuming.

This project automates the process by scraping reviews from Myntra product pages, storing them in MongoDB, and presenting them in a clean dashboard for analysis.

The application extracts:

- Customer Reviews
- Product Ratings
- Reviewer Information
- Review Text
- Product Details

The collected data can be used for customer sentiment analysis, product evaluation, and market research.

---

# ✨ Features

- Scrape customer reviews from Myntra
- Extract product ratings
- Store reviews in MongoDB Atlas
- Interactive Streamlit interface
- Review analysis dashboard
- Cross-platform ChromeDriver support
- Automatic data storage
- Easy-to-use interface

---

# 🛠️ Tech Stack

### Programming Language

- Python

### Web Scraping

- Selenium
- BeautifulSoup4

### Dashboard

- Streamlit

### Database

- MongoDB Atlas
- PyMongo

### Data Processing

- Pandas

### Visualization

- Plotly

### Environment Management

- Python-dotenv

### Browser Driver

- chromedriver-binary

### Version Control

- Git
- GitHub

---

# 📂 Project Structure

```text
Myntra-Review-Scraper/
│
├── app.py
├── requirements.txt
├── setup.py
├── README.md
│
├── src/
│   ├── scraper/
│   ├── database/
│   ├── visualization/
│   └── utils/
│
├── templates/
│
├── static/
│
├── screenshots/
│
└── .env
```

---

# 🏗️ Project Architecture

Place your architecture image inside the `flowchart/` or `screenshots/` folder.

```text
                User
                  │
                  ▼
         Streamlit Web App
                  │
                  ▼
          Selenium Web Driver
                  │
                  ▼
        Myntra Product Website
                  │
                  ▼
        BeautifulSoup Parser
                  │
                  ▼
          Extract Review Data
                  │
                  ▼
          MongoDB Atlas Database
                  │
                  ▼
      Review Analysis Dashboard
```

If you have an architecture image:

```markdown
![Project Architecture](screenshots/project_architecture.png)
```

---

# 📊 How It Works

1. User enters a Myntra product URL.
2. Selenium opens the product page.
3. BeautifulSoup extracts customer reviews.
4. Review data is cleaned.
5. Reviews are stored in MongoDB Atlas.
6. Streamlit displays the collected reviews.
7. Charts and insights are generated for analysis.

---

# 📦 Dataset

The dataset is generated dynamically by scraping customer reviews from Myntra product pages.

Collected information includes:

- Product Name
- Rating
- Review Title
- Review Description
- Reviewer Name
- Date (if available)

---

# ⚙️ Installation

## Clone the Repository

```bash
git clone https://github.com/CodeLeoX16/Myntra-Review-Scraper.git
```

Move into the project folder.

```bash
cd Myntra-Review-Scraper
```

---

## Create a Conda Environment

```bash
conda create -n myntra python=3.10 -y
```

---

## Activate the Environment

Windows

```bash
conda activate myntra
```

Linux/macOS

```bash
conda activate myntra
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

Create a `.env` file in the project directory.

```env
MONGODB_URL=your_mongodb_connection_string
```

Example

```env
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/
```

---

# ▶️ Run the Application

```bash
streamlit run app.py
```

The application will start at

```
http://localhost:8501
```

Open the above URL in your browser.

---

# 🗄️ MongoDB Integration

MongoDB Atlas is used to store all scraped reviews.

The application:

- Connects using PyMongo
- Stores review data
- Retrieves stored reviews
- Displays review information in Streamlit

---

# 🌐 ChromeDriver Support

The project uses **chromedriver-binary** instead of manually downloading ChromeDriver.

Benefits:

- Automatic driver management
- Cross-platform support
- Easier setup
- No need to maintain separate executables

---

# 📊 Dashboard Features

The Streamlit dashboard provides:

- Customer review list
- Product ratings
- Review statistics
- Interactive charts
- Product insights

---


# 🧪 Future Improvements

Some features that can be added in future versions:

- Sentiment Analysis
- AI-based Review Summarization
- Word Cloud Generation
- Export Reviews to CSV
- Product Comparison
- Review Filtering
- REST API
- User Authentication

---

# 📚 What I Learned

While building this project, I gained practical experience with:

- Web scraping using Selenium
- HTML parsing using BeautifulSoup
- MongoDB Atlas integration
- Streamlit application development
- Data visualization using Plotly
- Environment variable management
- Python project structure
- Git and GitHub

---

# 🤝 Contributing

Contributions are welcome.

1. Fork the repository.

2. Create a new branch.

```bash
git checkout -b feature-name
```

3. Commit your changes.

```bash
git commit -m "Add new feature"
```

4. Push your branch.

```bash
git push origin feature-name
```

5. Open a Pull Request.

---

# 📄 License

This project is created for learning and educational purposes.

---

# 👨‍💻 Author

## Somnath Bhunia

Computer Science Engineering Student

**GitHub**

https://github.com/CodeLeoX16

**LinkedIn**

[https://www.linkedin.com/in/Connect Linkdin/](https://www.linkedin.com/in/somnath-bhunia-3b300b328/)

---

# ⭐ Support

If you found this project useful, please consider giving it a ⭐ on GitHub.

Thank you for visiting this repository!
