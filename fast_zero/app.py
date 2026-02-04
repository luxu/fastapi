from http import HTTPStatus

from fastapi import FastAPI
from starlette.responses import HTMLResponse

from fast_zero.schemas import Message

app = FastAPI()


@app.get('/',
         status_code=HTTPStatus.OK,
         response_model=Message,
)
def read_root():
    return {'message': 'Olá mundo'}
