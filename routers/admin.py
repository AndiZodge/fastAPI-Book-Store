from fastapi import APIRouter, HTTPException, Request
from database import db_dependency
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from model import User, UserBook, Book
from BaseModel.BookBase import BookBase
from utils import check_admin_token, get_logger

log = get_logger(logger_name="admin router", module="admin router")

router = APIRouter()

@router.get('/user_list', tags=['admin'])
async def get_user_list(db: db_dependency, request: Request):
    try:
        if not (is_admin :=await check_admin_token(request)):
            return JSONResponse(content={'msg':'UNAUTHORIZED'}, status_code=401)  
        return db.query(User).all()
    except Exception as exx:
        log.error(str(exx))
        return JSONResponse(content={'msg': str(exx)}, status_code=400)
    
@router.get('/user_book_list', tags=['admin'])
async def get_all_user_book_list(db: db_dependency, request:Request):
    try:
        if not (is_admin :=await check_admin_token(request)):
            return JSONResponse(content={'msg':'UNAUTHORIZED'}, status_code=401)  
        user_books_details =  db.query(UserBook).all()
        for user_book in user_books_details:
            book_id = user_book.book_id
            user_id = user_book.user_id
            book_details = db.query(Book).filter(Book.id == book_id).first()
            user_details = db.query(User).filter(User.id == user_id).first()
            user_book.username = user_details.username
            user_book.email_id = user_details.email_id
            user_book.is_admin = user_details.is_admin
            user_book.book_name = book_details.book_name
        return user_books_details
    except Exception as exx:
        log.error(str(exx))
        return JSONResponse(content={'msg': str(exx)}, status_code=400)
    
@router.get('/user_book_list', tags=['admin'])
async def get_all_user_book_list(db: db_dependency, request:Request):
    try:
        if not (is_admin :=await check_admin_token(request)):
            return JSONResponse(content={'msg':'UNAUTHORIZED'}, status_code=401)
        user_books_details =  db.query(UserBook).all()
        for user_book in user_books_details:
            book_id = user_book.book_id
            user_id = user_book.user_id
            book_details = db.query(Book).filter(Book.id == book_id).first()
            user_details = db.query(User).filter(User.id == user_id).first()
            user_book.username = user_details.username
            user_book.email_id = user_details.email_id
            user_book.is_admin = user_details.is_admin
            user_book.book_name = book_details.book_name
            
        serialized_book = jsonable_encoder(user_books_details)
        return JSONResponse(content={'data': serialized_book}, status_code=200)

    except Exception as exx:
        log.error(str(exx))
        return JSONResponse(content={'msg': str(exx)}, status_code=400)
    
@router.post('/add_book', tags=['admin'])
async def add_book(db: db_dependency, request:Request):
    try:
        if not (is_admin :=await check_admin_token(request)):
            return JSONResponse(content={'msg':'UNAUTHORIZED'}, status_code=401) 
        body = await request.body()
        body_str = body.decode('utf-8')
        book_details = BookBase.parse_raw(body_str)
        db_transaction = Book(**book_details.model_dump())
        db.add(db_transaction)
        db.commit()
    except Exception as exx:
        log.error(str(exx))
        return JSONResponse(content={'msg': str(exx)}, status_code=400)
    
@router.put("/update_book/{item_id}", tags=['admin'])
async def update_item(item_id: int, request: Request, db: db_dependency):
    try:
        if not (is_admin :=await check_admin_token(request)):
            return JSONResponse(content={'msg':'UNAUTHORIZED'}, status_code=401)  
        body = await request.body()
        body_str = body.decode('utf-8')
        book_details = BookBase.parse_raw(body_str)
        db_item = db.query(Book).filter(Book.id == item_id).first()
        if db_item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        for key, value in book_details.dict().items():
            setattr(db_item, key, value)
        db.commit()
    
    except Exception as exx:
        log.error(str(exx))
        return JSONResponse(content={'msg': str(exx)}, status_code=400)

