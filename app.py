from flask import Flask, render_template, request
from datetime import date, timedelta

app = Flask(__name__)

TOTAL_SEATS_PER_SHOW = 25

# Example show data for a Bengaluru venue
dramas_by_venue = {
    "Ranga Shankara": [
        {
          "name": "Parameshi Prema Prasanga",
          "time": "7:00 PM",
          "image": "static/images/parameshipremaprasanga.png",
          "genre": "Comedy"
        },
        {
          "name": "Shivoham",
          "time": "8:45 PM",
          "image": "static/images/shivoham.png",
          "genre": "Mythological"
        },
    ],
    "Medai - The Stage Bengaluru": [
        {"name": "Kamsayana", "time": "6:00 PM", "image": "static/images/kamsayana.png", "genre": "Mythological"},
        {"name": "Husband 360", "time": "8:00 PM", "image": "static/images/husband360.png", "genre": "Comedy"},
    ],
    "Dr. C Ashwath Kala Bhavana": [
        {"name": "Anumaanada Avaantara", "time": "6:15 PM", "image": "static/images/anumaanadaavaantara.png", "genre": "Comedy"},
        {"name": "Kaakadosha", "time": "7:45 PM", "image": "static/images/kaakadosha.png", "genre": "Horror"},
    ]
}
venue_locations = {
    "Ranga Shankara": "https://maps.app.goo.gl/jYxpxHJGjL1pU2Hu6",
    "Medai - The Stage Bengaluru": "https://maps.app.goo.gl/XpBT6zdqhVcbVVkU8",
    "Dr. C Ashwath Kala Bhavana": "https://maps.app.goo.gl/p9HZ1DWZbDAyLoPN8"
}

# Simulated storage for booked seats
booked_seats = {}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/shows', methods=['GET', 'POST'])
def shows():
    today = date.today()
    date_str = request.form.get('date', today.strftime("%Y-%m-%d"))

    # Generate calendar range (for limiting input)
    min_date = today.strftime("%Y-%m-%d")
    max_date = (today + timedelta(days=6)).strftime("%Y-%m-%d")

    # Combine shows from all venues
    all_shows = []
    for venue, shows in dramas_by_venue.items():
        for show in shows:
            show_key = (show['name'], date_str, show['time'])
            booked = booked_seats.get(show_key, [])
            sold_out = len(booked) >= TOTAL_SEATS_PER_SHOW
            all_shows.append({
                'name': show['name'],
                'time': show['time'],
                'image': show['image'],
                'genre': show['genre'],
                'venue': venue,
                'location_link': venue_locations.get(venue),
                'sold_out': sold_out
            })

    featured = all_shows

    return render_template(
        'shows.html',
        date=date_str,
        shows=featured,
        min_date=min_date,
        max_date=max_date
    )


@app.route('/book', methods=['POST'])
def book():
    show_info = {
        'venue': request.form['venue'],
        'date': request.form['date'],
        'show_name': request.form['show_name'],
        'time': request.form['time'],
        'price': 200  # ₹200 per seat
    }

    show_key = (show_info['show_name'], show_info['date'], show_info['time'])
    unavailable = booked_seats.get(show_key, [])

    return render_template("book.html", show=show_info, booked=unavailable)

@app.route('/confirm', methods=['POST'])

def confirm():
    selected_seats = request.form.getlist('seats')
    seat_count = len(selected_seats)
    price_per_seat = int(request.form['price'])
    total_price = seat_count * price_per_seat

    show_key = (request.form['show_name'], request.form['date'], request.form['time'])

    # Save booked seats
    if show_key not in booked_seats:
        booked_seats[show_key] = []
    booked_seats[show_key].extend(selected_seats)

    booking_details = {
        "show_name": request.form["show_name"],
        "venue": request.form["venue"],
        "date": request.form["date"],
        "time": request.form["time"],
        "selected_seats": selected_seats,
        "total_price": total_price
    }
    return render_template("confirm.html", booking=booking_details)

if __name__ == '__main__':
    app.run(debug=True)
