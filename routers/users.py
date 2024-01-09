from fastapi import APIRouter, HTTPException, Request, Response, status
from database import db_dependency
from model import User, UserBook, Book
from BaseModel.BookGenreBase import BookGenreBase
from BaseModel.UserLoginBase import UserLoginBase
from BaseModel.UserBase import UserBase
from BaseModel.BuyBookBase import BuyBookBase
from sqlalchemy import desc
from fastapi.responses import JSONResponse
from utils import create_jwt, validate_token, get_logger

log = get_logger(logger_name="admin router", module="admin router")

### CHECK:
'''
Validation logic can be removed from each function call and put into a decorator 
'''

router = APIRouter()

@router.get('/get_books', tags=['user'])
async def get_books(db:db_dependency):
    try:
        return db.query(Book).all()
    except Exception as exx:
        log.error(str(exx))
        return JSONResponse(content={'msg': str(exx)}, status_code=400)

@router.get('/get_book/{id}', tags=['user'])
async def get_books(id: int, db:db_dependency):
    try:
        return db.query(Book).filter(Book.id == id).first()
    except Exception as exx:
        log.error(str(exx))
        return JSONResponse(content={'msg': str(exx)}, status_code=400)
    
@router.post('/get_books_by_genre', tags=['user'])
async def get_books_by_genre(request:Request, db:db_dependency):
    try:
        if not(token := await validate_token(request)):
            return JSONResponse(content={'msg':'UNAUTHORIZED'}, status_code=401) 
        body = await request.body()
        body_str = body.decode('utf-8')
        book_details = BookGenreBase.parse_raw(body_str)
        if book_details.genre != "All":
            data = db.query(Book).filter(Book.genre == book_details.genre).all()
        else:
            data = db.query(Book).order_by(desc(Book.id)).all()
        return data
    except Exception as exx:
        log.error(str(exx))
        return JSONResponse(content={'msg': str(exx)}, status_code=400)

## NOTE:
'''
    User related APIS should be grouped together and same for books
'''
@router.get('/my_books', tags=['user'])
async def get_my_books(request: Request, db: db_dependency):
    try:
        if not (token := await validate_token(request)):
            return JSONResponse(content={'msg':'UNAUTHORIZED'}, status_code=401) 
        user_id = token.get('sub')
        user_books_details = db.query(UserBook).filter(UserBook.user_id==user_id).all()
        # if isinstance(user_books_details, list): #NO NEED TO CHECK I GUESS
        for user_book in user_books_details:
            book_id = user_book.book_id
            _book_details = db.query(Book).filter(Book.id == book_id).first()
            user_book.book_name = _book_details.book_name
        return user_books_details
    except Exception as exx:
        log.error(str(exx))
        return JSONResponse(content={'msg': str(exx)}, status_code=400)

@router.post('/buy_book', tags=['user'])
async def buy_book( request:Request, db:db_dependency):
    try:
        if not (token := await validate_token(request)):
            return JSONResponse(content={'msg':'UNAUTHORIZED'}, status_code=401) 
        user_id = token.get('sub')
        body = await request.body()
        body_str = body.decode('utf-8')
        book_details = BuyBookBase.parse_raw(body_str)
        book_details.user_id = user_id
        data = db.query(UserBook).filter(UserBook.book_id == book_details.book_id,
                                            UserBook.user_id == user_id).all()
        if isinstance(data, list) and data:
            data = data[0]
        if not data:
            db_transaction = UserBook(**book_details.model_dump())
            db.add(db_transaction)
        else:
            book_details.quantity = data.quantity + 1
            book_details.total_cost += data.total_cost
            for key, value in book_details.dict().items():
                setattr(data, key, value)
        db.commit()
        _book_details = db.query(Book).filter(Book.id==book_details.book_id).first()
        _book_details.quantity_available -= 1
        db.commit()
    except Exception as exx:
        log.error(str(exx))
        return JSONResponse(content={'msg': str(exx)}, status_code=400)

@router.post('/create_user', status_code=status.HTTP_201_CREATED, tags=['user'])
async def create_user(user: UserBase, db: db_dependency):
    try:
        db_transaction = User(**user.model_dump())
        db.add(db_transaction)
        db.commit()
    except Exception as exx:
        log.error(str(exx))
        return JSONResponse(content={'msg': str(exx)}, status_code=400)

@router.post('/user_login', tags=['user'])
async def login(user:UserLoginBase, db: db_dependency, resp:Response):
    try:
        data = db.query(User).filter(User.username == user.username).first()
        if not data:
            resp.status_code = status.HTTP_404_NOT_FOUND
            return HTTPException( detail="Invalid user name")
        if data.password == user.password:
            # CHECK: instead of sending fields from data send data itself to create JWT
            return {'jwt': create_jwt(data)}
        else:
            resp.status_code = 401  
            return HTTPException( detail="Wrong password")
    except Exception as exx:
        log.error(str(exx))
        return JSONResponse(content={'msg': str(exx)}, status_code=400)
