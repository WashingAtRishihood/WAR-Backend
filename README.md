# WAR Backend - Laundry Service API

A simplified Django REST API backend for the Rishihood University Laundry Service system.

## Features

- **Student Management**: Registration and login with bag tracking
- **Washerman Management**: Simple username/password authentication
- **Order Workflow**: Complete laundry order lifecycle
- **Dashboard**: Statistics for both students and washermen
- **Admin Interface**: Easy management through Django admin

## Setup Instructions

### 1. Install Dependencies
```bash
# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 2. Database Setup
```bash
# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### 3. Run Development Server
```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/api/`

## API Endpoints

### Authentication
- `POST /api/auth/student/signup/` - Student registration
- `POST /api/auth/student/login/` - Student login (email + enrollment_no)
- `POST /api/auth/washerman/signup/` - Washerman registration
- `POST /api/auth/washerman/login/` - Washerman login (username + password)

### Orders
- `POST /api/orders/create/` - Create new order
- `GET /api/orders/student/<bag_no>/` - Get student's orders
- `GET /api/orders/all/` - Get all orders (washerman view)
- `GET /api/orders/pending/` - Get pending orders
- `PUT /api/orders/<order_id>/status/` - Update order status

### Dashboard
- `GET /api/student/dashboard/<bag_no>/` - Student dashboard data
- `GET /api/washerman/dashboard/` - Washerman dashboard data

## Models

### Student Model
- **Fields**: 
  - `name` - Student's full name
  - `email` (unique) - Student's email address
  - `enrollment_no` (unique) - Student's enrollment number
  - `phone_no` - Student's phone number
  - `bag_no` (unique, auto-generated) - Format: BAG + enrollment_no
  - `residency_no` - Student's residency number

### Washerman Model
- **Fields**: 
  - `username` (unique) - Washerman's login username
  - `password` - Washerman's login password

### Order Model
- **Fields**: 
  - `bag_no` - Links to student's bag number
  - `number_of_clothes` - Number of clothes for laundry
  - `submission_date` - When order was submitted
  - `status` - Order status (pending, inprogress, complete)

## Workflow

### Student Side:
1. **Register** with name, email, enrollment_no, phone_no, residency_no
2. **Login** using email and enrollment_no
3. **Create Order** by providing bag_no and number_of_clothes
4. **Track Status** through dashboard

### Washerman Side:
1. **Login** using provided username and password
2. **View Pending Orders** in dashboard
3. **Click "Received"** → status changes to "inprogress"
4. **Click "Ready"** → status changes to "complete"

## Admin Interface

Access Django admin at `http://127.0.0.1:8000/admin/` to manage:
- Students and their bag numbers
- Washermen accounts
- Orders and status updates

## CORS Configuration

The backend is configured to allow requests from:
- `http://localhost:3000` (React default)
- `http://localhost:5173` (Vite default)
- `http://127.0.0.1:3000`
- `http://127.0.0.1:5173`

## Testing

Run the test script to verify API functionality:
```bash
python test_simplified_api.py
```

This will test:
- Student registration and login
- Washerman registration and login
- Order creation and status updates
- Dashboard functionality
- Complete workflow from order creation to completion

## Key Features

- **No Complex Authentication**: Simple email/enrollment for students, username/password for washermen
- **Bag-Based Tracking**: Each student has a unique bag number for order tracking
- **Status Workflow**: Clear progression from pending → inprogress → complete
- **No Pricing**: Focus purely on laundry workflow without payment complexity
