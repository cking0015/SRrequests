"""Fetch hourly weather forecast for the current day using weather.gov."""
from __future__ import annotations

import argparse
import datetime as dt
import json
from typing import Any, Dict, Iterable, List
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

USER_AGENT = "SRrequestsWeather/1.0 (contact@example.com)"
POINTS_URL = "https://api.weather.gov/points/{lat},{lon}"

def _request_json(url: str) -> Dict[str, Any]:
    """Perform a GET request and parse the JSON response."""
    req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/geo+json"})
    with urlopen(req, timeout=10) as resp:  # type: ignore[arg-type]
        charset = resp.headers.get_content_charset("utf-8")
        payload = resp.read().decode(charset)
    return json.loads(payload)

def _parse_datetime(value: str) -> dt.datetime:
    """Parse ISO8601 timestamp returned by the weather.gov API."""
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    return dt.datetime.fromisoformat(value)

def _filter_today(periods: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    today_periods: List[Dict[str, Any]] = []
    for period in periods:
        start = _parse_datetime(period["startTime"])
        today = dt.datetime.now(start.tzinfo).date()
        if start.date() == today:
            today_periods.append(period)
    return today_periods

def fetch_hourly_forecast(lat: float, lon: float) -> List[Dict[str, Any]]:
    """Fetch the hourly forecast periods for the current day for a latitude/longitude."""
    metadata_url = POINTS_URL.format(lat=lat, lon=lon)
    points_data = _request_json(metadata_url)

    try:
        hourly_url = points_data["properties"]["forecastHourly"]
    except KeyError as exc:
        raise RuntimeError("Hourly forecast URL missing from API response") from exc

    hourly_data = _request_json(hourly_url)
    periods = hourly_data.get("properties", {}).get("periods", [])
    return _filter_today(periods)

def format_forecast(periods: Iterable[Dict[str, Any]]) -> str:
    lines = []
    for period in periods:
        start = _parse_datetime(period["startTime"])
        temperature = period.get("temperature")
        unit = period.get("temperatureUnit", "F")
        short_forecast = period.get("shortForecast", "")
        wind_speed = period.get("windSpeed", "")
        wind_direction = period.get("windDirection", "")
        lines.append(
            f"{start:%Y-%m-%d %H:%M %Z}: {temperature}°{unit} | "
            f"{short_forecast} | Wind {wind_speed} {wind_direction}"
        )
    return "\n".join(lines)

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("latitude", type=float, help="Latitude for the forecast")
    parser.add_argument("longitude", type=float, help="Longitude for the forecast")
    return parser.parse_args()

def main() -> None:
    args = parse_args()
    try:
        periods = fetch_hourly_forecast(args.latitude, args.longitude)
    except (HTTPError, URLError, RuntimeError, ValueError) as exc:
        raise SystemExit(f"Failed to retrieve forecast: {exc}")

    if not periods:
        print("No hourly forecast data available for today.")
        return

    print(format_forecast(periods))

if __name__ == "__main__":
    main()
