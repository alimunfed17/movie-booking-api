# Movie Booking API

A comprehensive Django REST API for movie ticket booking with JWT authentication, built with Django REST Framework for AlignTurtle.

## Features

- **User Authentication**: JWT-based signup and login
- **Movie Management**: List movies and their shows
- **Seat Booking**: Book seats with double-booking prevention
- **Booking Management**: View and cancel bookings
- **API Documentation**: Complete Swagger documentation
- **Security**: User-specific booking access control

## Setup Instructions

### Prerequisites
- Python 3.8+
- pip

### Installation

- 1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd movie-booking-api
   ```

- 2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

- 3. **Run migrations**
   ```bash
   python manage.py migrate
   ```

- 4. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

- 5. **Start the server**
   ```bash
   python manage.py runserver
   ```

- The API will be available at `http://127.0.0.1:8000/`

## API Documentation

Access the complete API documentation at:
- **Swagger UI**: `http://127.0.0.1:8000/swagger/`

## API Endpoints

### Authentication
- `POST /signup/` - Register a new user
- `POST /login/` - Login and returns JWT tokens

### Movies & Shows
- `GET /movies/` - List all movies
- `GET /movies/<id>/shows/` - List shows for a specific movie

### Bookings
- `POST /shows/<id>/book/` - Book a seat (requires JWT)
- `POST /bookings/<id>/cancel/` - Cancel a booking (requires JWT)
- `GET /my-bookings/` - List user's bookings (requires JWT)

## How to Use JWT Authentication

### 1. Register a User
```bash
curl -X POST http://127.0.0.1:8000/signup/ \
  -H "Content-Type: application/json" \
  -d '{ "username": "testuser", "email": "testuser@example.com", "password": "password123" }'

```

### 2. Login to access JWT Token
```bash
curl -X POST http://127.0.0.1:8000/login/ \
  -H "Content-Type: application/json" \
  -d '{ "username": "testuser", "password": "password123" }'

```

Response:
```json
{ "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...", "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..." }
```

### 3. Use Access Token for Protected Endpoints
```bash
curl -X POST http://127.0.0.1:8000/shows/3/book/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"seat_number": 5}'
```

## Example API Flow

- 1. **Register**: `POST /signup/`
  2. **Login**: `POST /login/` → returns JWT tokens
  3. **View Movies**: `GET /movies/`
  4. **View Shows**: `GET /movies/3/shows/`
  5. **Book Seat**: `POST /shows/3/book/` (with JWT)
  6. **View Bookings**: `GET /my-bookings/` (with JWT)
  7. **Cancel Booking**: `POST /bookings/3/cancel/` (with JWT)

## Business Rules

- **Double Booking Prevention**: A seat cannot be booked twice for the same show
- **Overbooking Prevention**: Cannot book seats beyond the show's capacity
- **Seat Liberation**: Cancelled bookings free up the seat for others
- **User Security**: Users can only cancel their own bookings

## Testing

Run the test suite:
```bash
python manage.py test
```

## Project Structure

```
movie-booking-api/
├── moviebooking/           # Main app
│   ├── models.py           # Movie, Show, Booking models
│   ├── serializers.py      # DRF serializers
│   ├── views.py            # API views
│   ├── urls.py             # URL patterns
│   ├── admin.py            # Admin interface
│   └── tests.py            # Unit tests
├── moviebookingapi/        # Project settings
│   ├── settings.py         # Django settings
│   └── urls.py             # Main URL config
├── requirements.txt        # Dependencies
└── README.md               # This file
```

## Technologies Used

- **Django 4.2.7**: Web framework
- **Django REST Framework 3.14.0**: API framework
- **djangorestframework-simplejwt 5.3.0**: JWT authentication
- **drf-yasg 1.21.7**: Swagger documentation
- **SQLite**: Database (default)

## Security Features

- JWT token-based authentication
- User-specific booking access control
- Input validation and sanitization
- Proper error handling
- Database constraints for data integrity

## Admin Interface

Access the Django admin at `http://127.0.0.1:8000/admin/` to manage:
- Movies
- Shows
- Bookings
- Users

## Testing

Run the test suite:
```bash
python manage.py test
```
