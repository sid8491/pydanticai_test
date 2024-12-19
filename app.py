import yfinance as yf
from pydantic import BaseModel
from pydantic_ai import Agent


class StockPriceResult(BaseModel):
    symbol: str
    price: float
    currency: str = "USD"
    message: str


stock_agent = Agent(
    "groq:llama-3.3-70b-versatile",
    result_type=StockPriceResult,
    system_prompt="You are a helpful financial assistant that can look up stock prices. Use the get_stock_price tool to fetch current data.",
)


@stock_agent.tool_plain
def get_stock_price(symbol: str) -> dict:
    ticker = yf.Ticker(symbol)
    price = ticker.fast_info.last_price
    return {"price": round(price, 2), "currency": "USD"}


result = stock_agent.run_sync("What is Apple's current stock price?")

print(result.data)
print("*" * 80)
print(result.cost())
print("*" * 80)
print(result.data.model_dump_json())
