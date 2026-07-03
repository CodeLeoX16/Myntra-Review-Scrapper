# Myntra Review Scraper Project

## Project Overview

The **Myntra Review Scraper** is a Streamlit-based web application that extracts customer reviews from Myntra products and provides meaningful insights through review analysis. It collects product ratings, review text, and customer feedback, helping users understand customer sentiment and product performance.

## Live Demo
**Live Application:** [https://your-live-link.com](https://myntra-review-scrapper-h8ewjgrnqspobh5wcnkaxi.streamlit.app/generate_analysis)

## Features

- Scrape customer reviews from Myntra
- Extract ratings and review content
- Store scraped data in MongoDB
- Interactive Streamlit dashboard
- Visualize review data for better insights
- Cross-platform ChromeDriver support using `chromedriver-binary`

---

## Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/PWskills-DataScienceTeam/myntra-review-scrapper.git
cd myntra-review-scrapper
```

### 2. Create and Activate a Conda Environment

```bash
conda create -p ./env python=3.10 -y
```

Activate the environment:

**Windows**

```bash
conda activate ./env
```

**Linux/macOS**

```bash
source activate ./env
```

---

### 3. Install Required Packages

```bash
pip install -r requirements.txt
```

---

### 4. Configure Environment Variables

Create a `.env` file in the project root and add your MongoDB connection string.

```env
MONGODB_URL=your_mongodb_connection_string
```

---

### 5. Run the Application

```bash
streamlit run app.py
```

Open your browser and navigate to:

```
http://localhost:8501
```

---

## Project Dependencies

The project is built using the following technologies:

- **Streamlit** – Interactive web application framework
- **Selenium** – Browser automation for web scraping
- **BeautifulSoup4** – HTML parsing
- **Pandas** – Data processing and analysis
- **Plotly** – Interactive data visualization
- **MongoDB** – NoSQL database for storing scraped reviews
- **PyMongo** – MongoDB database connectivity
- **chromedriver-binary** – Automatic ChromeDriver management
- **Python-dotenv** – Environment variable management

Install all dependencies with:

```bash
pip install -r requirements.txt
```

---

## ChromeDriver Support

Instead of maintaining a separate `chromedriver.exe`, this project uses the **chromedriver-binary** package. This automatically provides the appropriate ChromeDriver binary, improving compatibility across different operating systems and simplifying project setup.

---

## MongoDB Integration

MongoDB is used as the backend database to store scraped review data. The project connects to MongoDB using **PyMongo**, allowing efficient storage and retrieval of customer reviews for further analysis and visualization.

---

## Contributing

Contributions are welcome! Feel free to fork the repository, improve the project, and submit a pull request.

If you encounter any bugs or have feature suggestions, please open an issue in the repository.

---

## License

This project is intended for educational and learning purposes.

---

Happy Scraping! 🚀
