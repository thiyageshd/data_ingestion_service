from src.services.yahoo_finance import YahooFinanceService

def fetch_and_store_data(symbol, job_id):
    yahoo_service = YahooFinanceService()
    financial_data = yahoo_service.fetch_financial_data(symbol)
    news_data = yahoo_service.fetch_news_data(symbol)

    return {
        "job_id": job_id,
        "financial_data": financial_data,
        "news_data": news_data
    }
