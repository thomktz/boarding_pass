# main.py

import csv
from PIL import Image, ImageDraw, ImageFont
import settings
import qrcode
import urllib.parse

def load_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)

def draw_world_map(img: Image.Image) -> None:
    world = Image.open(settings.WORLD_MAP_PATH).convert("RGBA")

    world = world.resize(
        (
            int(settings.CANVAS_W * settings.SIDE_PANNEL_RATIO), 
            settings.CANVAS_H,
        ),
        Image.Resampling.LANCZOS,
    )
    alpha = world.getchannel("A")
    alpha = alpha.point(lambda p: int(p * settings.WORLD_MAP_OPACITY))
    world.putalpha(alpha)
    img.paste(world, (0, 0), world)

def draw_top_banner(img: Image.Image, draw: ImageDraw.ImageDraw, booking: str) -> None:
    split_x = int(settings.CANVAS_W * settings.SIDE_PANNEL_RATIO)

    left_overlay = Image.new(
        "RGBA",
        (split_x, settings.TOP_BANNER_H),
        (*settings.TOP_BANNER_COLOR, int(255 * settings.TOP_BANNER_OPACITY)),
    )

    right_overlay = Image.new(
        "RGBA",
        (settings.CANVAS_W - split_x, settings.TOP_BANNER_H),
        (*settings.SIDE_PANEL_TOP_BANNER_COLOR, int(255 * settings.TOP_BANNER_OPACITY)),
    )

    img.paste(left_overlay, (0, 0), left_overlay)
    img.paste(right_overlay, (split_x, 0), right_overlay)

    title_font = load_font(settings.FONT_BOLD, 80)
    subtitle_font = load_font(settings.FONT_REGULAR, 50)
    subsubtitle_font = load_font(settings.FONT_REGULAR, 35)

    draw.text((120, 15), "BOARDING PASS", font=title_font, fill="white")
    draw.text((1280, 145), f"Booking ref: {booking}", font=subsubtitle_font, fill="white")
    draw.text((120, 125), settings.AIRLINE_NAME, font=subtitle_font, fill="white")
    
def draw_side_panel_dots(draw: ImageDraw.ImageDraw) -> None:
    x = int(settings.CANVAS_W * settings.SIDE_PANNEL_RATIO)

    for y in range(0, settings.CANVAS_H + settings.DOT_SPACING, settings.DOT_SPACING):
        draw.ellipse(
            [
                (x - settings.DOT_RADIUS, y - settings.DOT_RADIUS),
                (x + settings.DOT_RADIUS, y + settings.DOT_RADIUS),
            ],
            fill=settings.DOT_COLOR,
        )

def draw_destination(draw: ImageDraw.ImageDraw, origin: str, destination: str) -> None:
    city_font = load_font(settings.FONT_BOLD, 115)

    y = 425
    draw.text(
        (435, y),
        origin.upper(),
        font=city_font,
        fill="black",
    )
    plane = Image.open(settings.PLANE_PATH).convert("RGBA")

    # rotate 90° (counter-clockwise). Use -90 for clockwise
    plane = plane.rotate(-90, expand=True)

    plane_w = 250
    plane_h = 250
    plane_x = 915
    plane_y = 390

    plane = plane.resize((plane_w, plane_h), Image.Resampling.LANCZOS)

    # optional: make plane black if source is not already black
    alpha = plane.getchannel("A")
    black_plane = Image.new("RGBA", plane.size, (0, 0, 0, 255))
    black_plane.putalpha(alpha)

    draw._image.paste(black_plane, (plane_x, plane_y), black_plane)

    draw.text(
        (1150, y),
        destination.upper(),
        font=city_font,
        fill="black",
    )

def draw_side_panel(
    img: Image.Image, 
    draw: ImageDraw.ImageDraw, 
    origin_code: str, 
    destination_code: str,
    name: str = "ANNE-SOPHIE BRISSET",
    flight: str = "PK042",
    date: str = "27 JUN 2026",
    seat: str = "12A",
    gate: str = "B12",
) -> None:
    split_x = int(settings.CANVAS_W * settings.SIDE_PANNEL_RATIO)
    x = split_x + settings.SIDE_PANEL_X_PAD

    label_font = load_font(settings.FONT_REGULAR, 34)
    value_font = load_font(settings.FONT_BOLD, 45)
    title_font = load_font(settings.FONT_BOLD, 54)

    label_color = settings.PASSENGER_LABEL_COLOR
    value_color = settings.SIDE_PANEL_TEXT_COLOR

    # Top right banner route
    plane = Image.open(settings.PLANE_PATH).convert("RGBA")
    plane = plane.rotate(-90, expand=True)
    plane = plane.resize((85, 85), Image.Resampling.LANCZOS)

    alpha = plane.getchannel("A")
    black_plane = Image.new("RGBA", plane.size, (255, 255, 255, 255))
    black_plane.putalpha(alpha)

    draw.text((x, 66), origin_code, font=title_font, fill="white")
    img.paste(black_plane, (x + 120, 70), black_plane)
    draw.text((x + 230, 66), destination_code, font=title_font, fill="white")

    def field(label: str, value: str, y: int, *, value_size=None):
        vf = value_font if value_size is None else load_font(settings.FONT_BOLD, value_size)
        draw.text((x-100, y), label.upper(), font=label_font, fill=label_color)
        draw.text((x-100, y + 34), value.upper(), font=vf, fill=value_color)

    field("Passenger", name, 255, value_size=38)

    # Flight / seat on same row
    draw.text((x-100, 385), "FLIGHT", font=label_font, fill=label_color)
    draw.text((x-100, 419), flight, font=value_font, fill=value_color)
    draw.text((x-100 + 220, 385), "SEAT", font=label_font, fill=label_color)
    draw.text((x-100 + 220, 419), seat, font=value_font, fill=value_color)

    field("Date", date, 530, value_size=38)
    field("Gate", gate, 670)

     

def add_passenger_info(
    draw: ImageDraw.ImageDraw,
    *,
    name: str,
    flight: str,
    date: str,
    seat: str,
    boarding: str,
    gate: str,
    arrival: str,
) -> None:
    label_font = load_font(settings.FONT_REGULAR, settings.PASSENGER_LABEL_FONT_SIZE)
    value_font = load_font(settings.FONT_BOLD, settings.PASSENGER_VALUE_FONT_SIZE)

    label_color = settings.PASSENGER_LABEL_COLOR
    value_color = settings.PASSENGER_VALUE_COLOR

    def draw_field(label: str, value: str, x: int, y: int) -> None:
        draw.text(
            (x, y),
            label.upper(),
            font=label_font,
            fill=label_color,
        )
        draw.text(
            (x, y + 30),
            value.upper(),
            font=value_font,
            fill=value_color,
        )

    draw_field("Passenger", name, 120, 275)
    draw_field("Flight", flight, 830, 275)
    draw_field("Date", date, 1100, 275)
    draw_field("Seat", seat, 1500, 275)
    draw_field("Gate", gate, 1100, 650)
    draw_field("Departure", boarding, 1300, 650)
    draw_field("Arrival", arrival, 1550, 650)
    
def draw_qr_code(img: Image.Image, x=120, y=520, size=settings.QR_SIZE, name: str = "") -> None:
    qr = qrcode.QRCode(
        version=None,  # let it pick smallest possible
        error_correction=qrcode.constants.ERROR_CORRECT_M,  # lower than H → smaller
        box_size=6,   # smaller modules
        border=1,     # default is 4 → this saves a LOT of space
    )
    qr.add_data(settings.QR_PAYLOAD+f"/?name={urllib.parse.quote(name)}")
    qr.make(fit=True)

    qr_img = qr.make_image(
        fill_color="black",
        back_color=settings.BACKGROUND_COLOR,
    ).convert("RGBA")

    qr_img = qr_img.resize(
        (size, size),
        Image.Resampling.NEAREST,
    )
    img.paste(qr_img, (x, y), qr_img)

def render_boarding_pass(
    name: str = "ANNE-SOPHIE BRISSET",
    destination: str = "LOS ANGELES",
    flight: str = "PK042",
    seat: str = "12A",
    gate: str = "B12",
    boarding: str = "08:00",
    arrival: str = "15:00",
    origin: str = "BORDEAUX",
    date: str = "27 JUN 2026",
    booking: str = "ABC123xyz6a7b8c9d"
) -> Image.Image:
    img = Image.new(
        "RGB",
        (settings.CANVAS_W, settings.CANVAS_H),
        settings.BACKGROUND_COLOR,
    )

    draw = ImageDraw.Draw(img)
    draw_world_map(img)
    draw_top_banner(img, draw, booking=booking)
    draw_side_panel_dots(draw)
    draw_destination(draw, origin, destination)
    draw_qr_code(img, name=name.split(" ")[0])
    draw_side_panel(
        img, 
        draw,
        name=name,
        origin_code=settings.AIRPORT_CODES[origin],
        destination_code=settings.AIRPORT_CODES[destination],
        flight=flight,
        date=date,
        seat=seat,
        gate=gate,
    )
    draw_qr_code(img, x=2150, y=620, size=150)
    
    add_passenger_info(
        draw,
        name=name,
        flight=flight,
        date=date,
        seat=seat,
        boarding=boarding,
        arrival=arrival,
        gate=gate,
    )
    return img

def load_guests(csv_path: str = "guests.csv") -> list[dict]:
    with open(csv_path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

if __name__ == "__main__":
    guests = load_guests()
    for guest in guests:
        name = guest["name"]
        boarding_pass = render_boarding_pass(origin=settings.ORIGIN_CITY, **guest)
        boarding_pass.save(f"outputs/{name.replace(' ', '_').lower()}.png")
        print(f"Boarding pass for {name} saved.")
        # boarding_pass.show()