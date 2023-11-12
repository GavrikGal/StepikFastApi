from fastapi import FastAPI
from pydantic import BaseModel


class Feedback(BaseModel):
    name: str
    message: str


app = FastAPI()


fake_users = {
    1: {"username": "john_doe", "email": "john@example.com"},
    2: {"username": "jane_smith", "email": "jane@example.com"},
}


@app.get('/users/{user_id}')
def read_user(user_id: int):
    if user_id in fake_users:
        return fake_users[user_id]
    return {"error": "User not found"}


@app.get('/users/')
def read_users(limit: int = 10):
    return dict(list(fake_users.items())[:limit])


fake_feedback_storage = []


@app.post('/feedback')
async def take_feedback(feedback: Feedback):
    fake_feedback_storage.append({"username": feedback.name,
                                  "message": feedback.message})
    return {'message': f'Feedback received. Thank you, {feedback.name}!'}
