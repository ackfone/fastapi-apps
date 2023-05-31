from typing import List, Optional
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from ..import util, schemas, models, oauth2, database

router = APIRouter(
    tags=['Likes']
)

#@get all data
@router.get('/likes')
def like(db:Session = Depends(database.get_db), 
            currentUser:int = Depends(oauth2.validate_current_user)):
    try:
        result = db.query(models.Like).all()
        return result
    except Exception as e:
        print(e)


#use schemas to get the kind of information we want from the user
@router.post('/likes', status_code=status.HTTP_201_CREATED)
def like(like:schemas.LikeData, db:Session = Depends(database.get_db),
         currentUser:int = Depends(oauth2.validate_current_user)):
    
    chk_post = db.query(models.Post).filter(models.Post.id == like.post_id)
    print(chk_post)
    if chk_post == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post not found")
    
    #check if vote with unique id of post n user exist
    like_query = db.query(models.Like).filter(models.Like.post_id == like.post_id, models.Like.user_id == currentUser.id)
    foundLike = like_query.first()

    if like.like_type == 1:
        if foundLike:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"{currentUser.username} has already like this post")
        
        add_like = models.Like(post_id=like.post_id, user_id=currentUser.id)
        db.add(add_like)
        db.commit()
        print(foundLike)
        return {'msg': f'{currentUser.username} like post with id {like.post_id}'}
    else:
        if not foundLike:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post not exist")
        
        like_query.delete()
        db.commit()
        return {"msg": f"{currentUser.username} unlike post"}