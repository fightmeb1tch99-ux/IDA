"""
Weather Plugin for IDA OS v3.0
"""
import aiohttp
from plugins.base import BasePlugin
from logger import log_info, log_error

class WeatherPlugin(BasePlugin):
    def __init__(self):
        super().__init__("Weather", "Get current weather for a city")

    async def execute(self, args: dict = None) -> dict:
        city = args.get("city", "Moscow") if args else "Moscow"
        log_info(f"WeatherPlugin: Fetching weather for {city}")
        
        try:
            # Using a free weather API (example)
            async with aiohttp.ClientSession() as session:
                url = f"https://wttr.in/{city}?format=j1"
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        current = data['current_condition'][0]
                        temp = current['temp_C']
                        desc = current['weatherDesc'][0]['value']
                        return {
                            "status": "success",
                            "city": city,
                            "temperature": f"{temp}°C",
                            "description": desc
                        }
                    return {"status": "error", "message": "Weather service unavailable"}
        except Exception as e:
            log_error("WeatherPlugin failed", e)
            return {"status": "error", "message": str(e)}
