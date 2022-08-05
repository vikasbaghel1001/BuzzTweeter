
from typing_extensions import Concatenate
from sqlalchemy.util import contextmanager
from starlette.routing import Route
from .. import  models , schemas ,utils ,oauth2 ,database
from fastapi import FastAPI ,Response , status , Depends ,APIRouter      
from fastapi.exceptions import HTTPException 
from .. database import  get_db
from sqlalchemy.orm import Session 
from sqlalchemy import insert
from typing import List ,Optional

router = APIRouter(
  prefix="/posts" ,   # use to replace /posts in every @router
  tags=['posts']
)


# get all the posts
@router.get("/" ,response_model=list[schemas.Post2]  )   # we cannot have same endpoint if it have same endpoint it will run 
                     # run the first endpoint
  # cursor.execute(""" SELECT * FROM posts  """)      by using pure sql commands in posts
  # posts = cursor.fetchall()

def get_user( db : Session = Depends(get_db) ,  curent_user : int  =Depends(oauth2.get_current_user) , 
         limit :int = 10 , skip :int = 0 ,search : Optional[str] = "" ):
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    print(limit)
    return posts       # for list of posts we use diffrent response model



@router.post("/" , status_code= status.HTTP_201_CREATED , response_model=schemas.Post2) 
def create_posts( post : schemas.Post , db : Session = Depends(get_db) , current_user : int  =Depends(oauth2.get_current_user)): 

      # using sql commnads 
   # cursor.execute(""" INSERT INTO users ( title , price , content) VALUES ( %s , %s ,%s )
    #                  RETURNING *""" 
   #                           (post.tile , post.price , post.published))

   # new_link = cursor.fetchone()
   # conn.commit()
   # return { "data" :   new_link}



  new_posts = models.Post( owner_id=current_user.id , **post.dict()  )
  db.add(new_posts)
  db.commit()                      
  db.refresh(new_posts)
  return new_posts

# title string , content string    





@router.get("/{id}"  , response_model=list[schemas.Post2])
def getpost(id : int , db : Session = Depends(get_db) , current_user : int  =Depends(oauth2.get_current_user)):
   # cursor.execute(""" SELECT * FROM posts WHERE id = %s """ , (str(id)))
   # new_post23 = cursor.fetchone()       SQL commands 
    new_post23 = db.query(models.Post).filter(models.Post.owner_id== id ).all()
    print(new_post23)
    if not new_post23:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , 
                                    detail = f"post with id {id} was not found")                                
    return new_post23





# for deleteing a post using delte http response
@router.delete("/{id}" ,status_code=status.HTTP_204_NO_CONTENT)
def delete_post( id : int ,  db : Session = Depends(get_db) , current_user : int  =Depends(oauth2.get_current_user)):
    #cursor.execute(""" DELETE  FROM posts WHERE id = %s returning *""" , (str(id)))
   # delete_post = cursor.fetchone(),
   # conn.commit()                                        SQL CODE 
     
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    


    if post == None:
      raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , 
                                    detail = f"post with id {id} does not exit ")

    if post.owner_id != current_user.id:
      raise HTTPException(status_code= status.HTTP_403_FORBIDDEN ,
           detail = "Not authorised to do the current action")
                                
    

    post_query.delete( synchronize_session =False)  
    db.commit()    
    return Response(status_code=status.HTTP_204_NO_CONTENT)





# update the post 

@router.put("/{id}" , response_model=schemas.Post)
def updated_post( id : int , updated_post: schemas.Post,  db : Session = Depends(get_db) , current_user : int  =Depends(oauth2.get_current_user)):
    #cursor.execute(""" UPDATE posts SET title = %s , content =%s , published=%s WHERE id = %s returning *""" ,
    #      ( post.title , post.content , post.published , str(id)) )
   # update_post = cursor.fetchone(),
   # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
  
    if post == None:
      raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , 
                                    detail = f"post with id {id} does not exit ")

    if post.owner_id != current_user.id:
      raise HTTPException(status_code= status.HTTP_403_FORBIDDEN ,
           detail = "Not authorised to do the current action")
                                
    post_query.update(updated_post.dict() , synchronize_session=False)
    db.commit()
    return post_query.first()
    