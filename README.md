# FAST JSON XML Convertor

### Build it:
docker-compose up --build

### Run it:
docker-compose up

### Prepare DB:
python3 create_tables.py

### Create user
POST http://0.0.0.0:80/user?email=a.b@c.com
BODY {"text": "email text"}

### Get user
GET http://0.0.0.0:80/user?email=a.b@c.com

### Delete user
DELETE http://0.0.0.0:80/user?email=a.b@c.com

### Get all users
GET http://0.0.0.0:80/users
