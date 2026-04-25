# ✈️ Boarding Pass Generator

A Python tool that generates personalized, print-ready boarding pass images for guests — perfect for events, weddings, or parties with a travel theme.

## Example Output

Each boarding pass includes:
- Airline name & route (origin → destination)
- Passenger name, flight number, seat, gate, departure & arrival times
- World map background with a translucent banner
- QR code linking to a custom URL
- Booking reference

## Project Structure

```
boarding_pass/
├── main.py              # Guest list & entry point
├── pass_generator.py    # (reserved for future refactor)
├── settings.py          # All visual & content configuration
├── assets/
│   ├── fonts/           # Roboto Condensed & Oswald font files
│   ├── plane.png        # Plane icon used on the pass
│   └── world_map.webp   # Background world map
├── outputs/             # Generated boarding pass PNGs saved here
└── guests.csv           # Guest data (name, destination, seat, etc.)
```

## Requirements

Install dependencies with pip:

```bash
pip install Pillow qrcode
```

## Usage

1. Edit the `guests` list in `main.py` with your passenger details.
2. Update `settings.py` to customise the airline name, colours, fonts, QR payload, etc.
3. Run the generator:

```bash
python main.py
```

Generated images are saved to the `outputs/` folder as `firstname_lastname.png`.

## Configuration (`settings.py`)

| Setting | Description |
|---|---|
| `AIRLINE_NAME` | Name displayed on the boarding pass |
| `ORIGIN_CITY` | Departure city (must be in `AIRPORT_CODES`) |
| `QR_PAYLOAD` | URL encoded in the QR code |
| `BACKGROUND_COLOR` | Canvas background RGB colour |
| `TOP_BANNER_COLOR` | Colour of the top banner |
| `AIRPORT_CODES` | Dict mapping city names to IATA-style codes |

## Guest Fields

Each guest entry in `guests` (and `guests.csv`) supports:

| Field | Example |
|---|---|
| `name` | `THOMAS KIENTZ` |
| `destination` | `KYOTO` |
| `flight` | `PK042` |
| `seat` | `1A` |
| `gate` | `B12` |
| `boarding` | `08:00` |
| `arrival` | `15:00` |
| `booking` | `ABC123xyz6a7b8c9d` |
