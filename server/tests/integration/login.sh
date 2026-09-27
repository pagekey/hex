#!/bin/bash

curl -X POST http://localhost:8000/sessions/seed
curl -X POST http://localhost:8000/sessions/new -H "Content-Type: application/json" -d '{"username": "admin", "password": "admin123456"}'
