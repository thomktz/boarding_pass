# ✈️ Boarding Pass Generator


## Project Structure

```
boarding_pass/
├── main.py              # Guest list & entry point
├── settings.py          # All visual & content configuration
├── requirements.txt     # Python dependencies
├── assets/
│   ├── fonts/           # Roboto Condensed & Oswald font files
│   ├── plane.png        # Plane icon used on the pass
│   └── world_map.webp   # Background world map
├── outputs/             # Generated boarding pass PNGs saved here
└── guests.csv           # Guest data (name, destination, seat, etc.)
```

## Requirements

Install dependencies manually with pip:

```bash
pip install Pillow qrcode
```

You can also install from the requirements file:

```bash
pip install -r requirements.txt
```

## Usage

1. Edit `guests.csv` with your passenger details.
2. Run the generator:

```bash
python main.py
```

Generated images are saved to the `outputs/` folder as `firstname_lastname.png`.