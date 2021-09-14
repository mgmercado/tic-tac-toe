from fastapi import APIRouter

router = APIRouter(prefix='/default', tags=['Default'])


@router.get('/', status_code=200, tags=['Default'])
async def ping() -> dict:
    return {'message': 'pong!'}
