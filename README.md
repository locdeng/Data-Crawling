# Company Data Crawler (JobKorea, JobPlanet, Naver API)

This project collects and processes company information from three sources:  
- **JobKorea** (using BeautifulSoup)  
- **JobPlanet** (using Selenium)  
- **Naver Search API** (using requests)

The dataset includes **500+ South Korean companies name**

---

## Features

- Scrape company info (name, industry, capital, sale, established day, and CEO) from **JobKorea**  
- Extract employee reviews and ratings from **JobPlanet**  
- Validate and enrich company names using **Naver Open API**  
- Save final dataset to `.csv`   
- Headless browser automation using Selenium  
- Clean and efficient modular code  

---

## Tech Stack

| Tool        | Purpose                              |
|-------------|--------------------------------------|
| `Python 3.x`| Programming language                 |
| `BeautifulSoup` | HTML parsing (JobKorea)          |
| `Selenium`  | Dynamic content automation (JobPlanet)|
| `requests`  | API communication (Naver API)        |
| `pandas`    | Data processing and exporting        |
| `openpyxl`  | Excel file handling                  |


---

## Project Structure

company-crawler/

├── jobkorea_data_crawling_edited.py # Crawls JobKorea using BeautifulSoup

├── Crawling_Jobplanet_edited.py # Automates JobPlanet with Selenium

├── craling_news_naver_edited.py # Queries Naver Open API

├── companies.csv # expected a output dataset file

├── requirements.txt # Python dependencies

└── README.md # Project documentation

