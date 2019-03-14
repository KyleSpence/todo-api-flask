# todo-api-flask

> A RESTful API for managing a todo list. Written in Flask and Python

## Running 
### Locally (Development Mode)
```bash
python app.py
```

### Production
```bash
./run.sh
```

## Environment Variables
You'll need the following environment variables to be defined
- MONGODB_HOST (MongoDB host)
- MONGODB_PORT (MongoDB port)

## Endpoints
### Health
Checks to see if the API is alive and connect to mongo
```bash
curl --request GET \
  --url http://localhost:5000/health
```

### List all tasks
Gets all the tasks
```bash
curl --request GET \
  --url http://localhost:5000/todo/api/tasks
```

### List task with specific task ID
Lists a task with given task ID
```bash
curl --request GET \
  --url http://localhost:5000/todo/api/tasks/1
```

### Create a task
Create a task
```bash
curl --request POST \
  --url http://localhost:5000/todo/api/tasks \
  --header 'content-type: application/json' \
  --data '{ \
	"title": "Buy Milk", \
	"description": "Buy some milk" \
  }'
```

### Update task with specific task ID
Update a task with given task ID
```bash
curl --request PUT \
  --url http://localhost:5000/todo/api/tasks/1 \
  --header 'content-type: application/json' \
  --data '{ \
	"title": "Bleh", \
	"description": "Bleh bleh bleh", \
	"done": true \
}'
```

### Delete Task
Delete a task with a given ID
```bash
curl --request DELETE \
  --url http://localhost:5000/todo/api/tasks/1
```