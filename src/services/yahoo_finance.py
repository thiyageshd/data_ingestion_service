from src.config import Config

class YahooFinanceService:
    def __init__(self):
        self.api_url = Config.YAHOO_FINANCE_API_URL
        self.api_key = Config.YAHOO_API_KEY

    def fetch_financial_data(self, symbol: str):
        financial_data_mock = {"id": 1, "company": "yahoo", "year": 2025, "revenue": 1000000, "profit": 200000} 
        return financial_data_mock

    def fetch_news_data(self, symbol: str):
        news_data_mock = [
            {
                "title": "Yashoo Reports Record Earnings in Q2 2023",
                "date": "2024-07-25",
                "summary": "Yashoo has announced a record revenue growth of 35% year over year..."
            },
            {
                "title": "Yashoo Expands Production Amid Market Growth",
                "date": "2024-03-15",
                "summary": "Yashoo's expansion into new markets is driving significant revenue growth..."
            },
            {
                "title": f"News article about {symbol}", 
                "date": "2024-09-20", 
                "summary": "Summary of the news article"
            }
        ]  
        return news_data_mock