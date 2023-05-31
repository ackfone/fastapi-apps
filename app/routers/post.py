from typing import List, Optional
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..import util, schemas, models, oauth2
from ..database import get_db

router = APIRouter(
    tags=['Posts']
)

#@get all data
#, response_model=List[schemas.PostResponse]
@router.get('/posts')
def getpost(db:Session = Depends(get_db),
            currentUser:int = Depends(oauth2.validate_current_user),
            limit:int = 10, search:Optional[str]=""):
    try:
        # result = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).all()
        result = db.query(models.Post, func.count(models.Like.post_id).label('likes')
        ).join(models.Like, models.Like.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()
        # print(result)
        return result
    except Exception as e:
        print(e)


# creating or addig post
@router.post('/posts', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(postdata:schemas.CreatePost, db:Session = Depends(get_db), 
                currentUser:int = Depends(oauth2.validate_current_user)):
    try:
        # print(f"{currentUser.id}\n{currentUser.username}")
        result = models.Post(user_id=currentUser.id, username=currentUser.username, **postdata.dict())
        db.add(result)
        db.commit()
        db.refresh(result)
        return result
    except Exception as e:
        print(e)


# retriving post base on post id
@router.get("/posts/{username}")
def get_post_byid(username: str, db:Session = Depends(get_db), 
                currentUser:int = Depends(oauth2.validate_current_user)):
    result = db.query(models.Post).filter(models.Post.username == username).all()
    if not result or result == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="post not found")
    else:
        return result


#@delete
@router.delete("/posts/{id}")
def delete_post(id: int, db:Session = Depends(get_db), 
            currentUser:int = Depends(oauth2.validate_current_user)):
    
    result = db.query(models.Post).filter(models.Post.id == id)

    if not result.first() or result.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post not found")
    if result.first().user_id != currentUser.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"unable to delete post")
    result.delete()
    db.commit()
    return {"msg": "post deleted sucessfully"}

#updating enitre post
@router.put("/posts/{id}")
def update_single_post(id: int, post:schemas.CreatePost, db:Session = Depends(get_db), 
                currentUser:int = Depends(oauth2.validate_current_user)):
    
    result = db.query(models.Post).filter(models.Post.id == id)

    post_exist = result.first()
    if not post_exist or post_exist == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post not found")
    if post_exist.user_id != currentUser.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"unable to update post")
    result.update(post.dict())
    db.commit()
    return {"msg": "sucessfully updated"}
    