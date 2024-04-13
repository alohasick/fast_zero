from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fast_zero.schemas import Message, UserDB, UserList, UserPublic, UserSchema

app = FastAPI()
database = []


@app.get('/', status_code=200, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}


@app.get('/html', status_code=200, response_class=HTMLResponse)
def read_root_html():
    return HTMLResponse(content='Olá Mundo!')


@app.post('/users', status_code=201, response_model=UserPublic)
def create_user(user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), id=len(database) + 1)

    database.append(user_with_id)

    return user_with_id


@app.get('/users', status_code=200, response_model=UserList)
def get_users():
    return {'users': database}
