import requests
from jubber.config import HOROSCOPE_API_BASE_URL

def fetch_horoscope(url_suffix, params):
    try:
        url = f"{HOROSCOPE_API_BASE_URL}/{url_suffix}"
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching horoscope: {e}")
        return {}

def get_daily_horoscope(sign: str, day: str) -> dict:
    return fetch_horoscope("daily", {"sign": sign, "day": day})

def get_monthly_horoscope(sign: str) -> dict:
    return fetch_horoscope("monthly", {"sign": sign})

def get_weekly_horoscope(sign: str) -> dict:
    return fetch_horoscope("weekly", {"sign": sign})

# def get_daily_horoscope(sign: str, day: str) -> dict:
#     """Get daily horoscope for a zodiac sign.
#     Keyword arguments:
#     sign:str - Zodiac sign
#     day:str - TODAY OR TOMORROW OR YESTERDAY
#     Return:dict - JSON data
#     """
#     url = "https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily"
#     params = {"sign": sign, "day": day}
#     response = requests.get(url, params)

#     return response.json()


# def get_monthly_horoscope(sign) -> dict:
#     """Get daily horoscope for a zodiac sign.
#     Keyword arguments:
#     sign:str - Zodiac sign
#     day:str - *MONTH*
#     Return:dict - JSON data
#     """
#     url = "https://horoscope-app-api.vercel.app/api/v1/get-horoscope/monthly"
#     params = {"sign": sign}
#     response = requests.get(url, params)
#     return response.json()


# def get_weekly_horoscope(sign) -> dict:
#     """Get daily horoscope for a zodiac sign.
#     Keyword arguments:
#     sign:str - Zodiac sign
#     day:str - *WEEK*
#     Return:dict - JSON data
#     """
#     url = "https://horoscope-app-api.vercel.app/api/v1/get-horoscope/weekly"
#     params = {"sign": sign}
#     response = requests.get(url, params)
#     return response.json()

# would you like know your future
if __name__ == "__main__":
    print(get_daily_horoscope('Virgo', "WEEK"))