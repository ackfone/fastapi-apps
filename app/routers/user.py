from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from ..import util, schemas, models, oauth2
from ..database import get_db
from typing import List

router = APIRouter(
    tags=['Users']
)

#get all users
@router.get("/users", response_model = List[schemas.UserExistResponse])
def all_users(db:Session=Depends(get_db), 
            currentUser:int = Depends(oauth2.validate_current_user)):
    result = db.query(models.User).all()
    return result

#add users
@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserRegistraionResponse)
def add_user(user:schemas.CreateUser, db:Session=Depends(get_db)):
    try:
        user.password = util.hash_password(user.password)
        result = models.User(**user.dict())
        db.add(result)
        db.commit()
        db.refresh(result)
        return result
    except Exception as e:
        print(e)


#chk user login
@router.get("/login")
def add_user(user:schemas.UserLogin, db:Session=Depends(get_db)):
    result = db.query(models.User).filter(models.User.email == user.email).first()
    if not result or result == None:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail="Invalid Credential")
    else:
        if not util.verify_password(user.password, result.password):
            raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail="Invalid Credential")
        #create and return token
        access_token = oauth2.create_access_token(data={"user_id":result.email})
        return {"token":access_token, "token_type":"bearer", "msg":"Login Sucessful"}
        # return {"msg":"Login Sucessful"}
    


#serachuser profile
@router.get("/users/{username}", response_model=schemas.UserExistResponse)
def finduser(username:str, db:Session=Depends(get_db), 
                currentUser:int = Depends(oauth2.validate_current_user)):
    result = db.query(models.User).filter(models.User.username == username).first()
    if not result or result == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="user not found")
    else:
        return result

#@delete
@router.delete("/users/{userid}")
def delete_post(userid: int, db:Session = Depends(get_db), 
            currentUser:int = Depends(oauth2.validate_current_user)):
    
    result = db.query(models.User).filter(models.User.id == userid)
    if not result.first() or result.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post not found")
    if userid != currentUser.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"unable to delete account! please login as the user of the account")
    
    # con.commit()
    result.delete()
    db.commit()
    return {"msg": "user deleted sucessfully"}