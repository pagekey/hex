#!/bin/bash

curl -X POST http://localhost:8000/sessions/seed
curl -X POST http://localhost:8000/sessions -H "Content-Type: application/json" -d '{"username": "admin", "password": "admin123456"}' -i

curl http://localhost:8000/sessions/check

SESSION_ID=TfbscSf9  # TODO: parse this from the response somehow
curl -H "Cookie: session_id=$SESSION_ID" http://localhost:8000/sessions/check

# Check workflow creation
curl -X POST -H "Cookie: session_id=$SESSION_ID" http://localhost:8000/workflows -H "Content-Type: application/json" -d '{"id":"my-workflow", "operations": [{"name":"do thing", "command": "echo hi"}]}'

# List workflows
curl -H "Cookie: session_id=$SESSION_ID" http://localhost:8000/workflows -H "Content-Type: application/json"

# Run a workflow
curl -X POST -H "Cookie: session_id=$SESSION_ID" http://localhost:8000/workflows/run -H "Content-Type: application/json" -d '{"id":"my-workflow"}'
