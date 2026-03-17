# SRrequests

This repository includes a simple Python script to fetch the current day's hourly weather forecast from the National Weather Service (`weather.gov`) API.

## Usage

```bash
python weather_forecast.py [--auto-location] [<latitude> <longitude>]
```

Provide a latitude and longitude to use those coordinates directly. If you omit the coordinates or pass `--auto-location`, the script will request approximate coordinates for your public IP address from the free [ipapi.co](https://ipapi.co/) geolocation service. When both manual coordinates and auto mode are supplied, the auto-detected values are preferred but the manual coordinates are used as a fallback if detection fails.

The script will query the weather.gov API for the resolved latitude and longitude, collect the hourly forecast, and display only the periods that fall on the current calendar day for the location's time zone.

> **Note:** The National Weather Service requires requests to include a custom `User-Agent` header with contact information. Update the `USER_AGENT` constant in `weather_forecast.py` with your details before making repeated requests.

> **Note:** Automatic location detection depends on the ipapi.co service, which enforces rate limits and may require a descriptive `User-Agent`. If you plan to rely on auto-detection heavily, review the provider's terms and configure the script's `USER_AGENT` accordingly.


## Waste sorting app

Run the Streamlit app:

```bash
pip install streamlit torch torchvision pillow
streamlit run waste_sorting_app.py
```

Upload a picture and the app will suggest recycling, compost, or trash using a pre-trained ResNet18 image model and keyword-based waste rules.
