# ✈️ Boarding Pass Generator


## Project Structure

```
boarding_pass/
├── main.py              # Guest list & entry point
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

1. Edit `guests.csv` with your passenger details.
2. Run the generator:

```bash
python main.py
```

Generated images are saved to the `outputs/` folder as `firstname_lastname.png`.