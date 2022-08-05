from typing import Optional                 # none 
from warnings import simplefilter
from fastapi import FastAPI ,Response , status , Depends      
from fastapi.exceptions import HTTPException           # for raising the exception 
from fastapi.params import Body         #importing fast api 
from pydantic import BaseModel       # used to define a schema a particular set format of data
from random import randrange         # for random value 
import psycopg2
from  psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from sqlalchemy.sql.sqltypes import Integer
from . import  models , schema 
from .database import  engine , get_db

models.Base.metadata.create_all(bind=engine)




app = FastAPI()  # instance 






while True :

 try:
  conn = psycopg2.connect(host ='localhost' , database='FASTAPI' , user='postgres' ,
  password ='naruto512#LM10' , cursor_factory=RealDictCursor)
     
  cursor =conn.cursor() 
  print("database conncetion was succesfull")
  break


 except Exception as error:
   print("connecting failed ")
   print("Error :" , error)
   time.sleep(3)




@app.get("/")   # decorator that gives meaning to the given code 
                # "/" is the end point of the url it is the root path for url 
async def root():    # async function with a http request we can have multiple http
                    # requests like get , head , delete etc 
                    # root is a function name we can change it 
                
    return {"message": "hi welcome to fast api"}


@app.get("/users")
def create_user( db : Session = Depends(get_db)):
    posts = db.query(models.User).all()

     
    return { "data" : posts}

@app.get("/posts")   # we cannot have same endpoint if it have same endpoint it will run 
                     # run the first endpoint
  # cursor.execute(""" SELECT * FROM posts  """)      by using pure sql commands in posts
  # posts = cursor.fetchall()

def get_user( db : Session = Depends(get_db)):
    posts = db.query(models.User).all()

    return{"data" : posts}




@app.post("/posts" , status_code= status.HTTP_201_CREATED) 
# below method is used by using raw json from the body without any schema

#def create_posts(payload : dict =Body(...)):   # create a variable to acces the raw json informtion
                                                 # using post request
                                                            
    #print(payload)
   # return{"new_post" : f"title : {payload['title']}  , content : {payload['content']}"} 




def create_posts( post : schema.PostCreate , db : Session = Depends(get_db)): 
    #print(post)     # pidentantic model check it with the post class 
   # print(post.dict())  # converts to dictionary 

  # post_dict= post.dict()
   #post_dict['id'] = randrange(0 , 1000000000)
  # my_posts.append(post_dict)
  # return{"data" : post_dict }    # thats how we create a schema for a particular type of data
                                     # that we need from the user


      # using sql commnads 




   # cursor.execute(""" INSERT INTO users ( title , price , content) VALUES ( %s , %s ,%s )
    #                  RETURNING *""" 
   #                           (post.tile , post.price , post.published))

   # new_link = cursor.fetchone()
   # conn.commit()
   # return { "data" :   new_link}




  posts = models.User( **post.dict()  )
  db.add(posts)
  db.commit()                      
  db.refresh(posts)
  return{ "data" : posts}

# title string , content string    


# this is one of the method to to give http response like 404 , 402, etc

#@app.get("/posts/{id}")
#def etpost(id : int , response : Response):
 #  post = find_post(id)
  #  if not post:
   #     response.status_code = status.HTTP_404_NOT_FOUND
   #     return {"message" : f"post with id {id} was not found"}
   # return{ "data" : post}



@app.get("/posts/{id}")
def etpost(id : int , db : Session = Depends(get_db) ):
   # cursor.execute(""" SELECT * FROM posts WHERE id = %s """ , (str(id)))
   # new_post23 = cursor.fetchone()       SQL commands 
    new_post23 = db.query(models.User).filter(models.User.id == id ).first()
    print(new_post23)
    if not new_post23:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , 
                                    detail = f"post with id {id} was not found")                                
    return{ "data" : new_post23}



# for deleteing a post using delte http response
@app.delete("/posts/{id}" ,status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int , db : Session = Depends(get_db) ):
    #cursor.execute(""" DELETE  FROM posts WHERE id = %s returning *""" , (str(id)))
   # delete_post = cursor.fetchone(),
   # conn.commit()                                        SQL CODE 
     

    post = db.query(models.User).filter(models.User.id == id )


    if post.first() ==None:
      raise HTTPException(status_code= status.HTTP_404_NOT_FOUND ,
           detail = f"post with id {id} does not exit")

    post.delete( synchronize_session =False)  
    db.commit()    
    return Response(status_code=status.HTTP_204_NO_CONTENT)



# update the post 
@app.put("/posts/{id}")
def updated_post( id : int , updated_post:schema.PostCreate ,  db : Session = Depends(get_db) ):
    #cursor.execute(""" UPDATE posts SET title = %s , content =%s , published=%s WHERE id = %s returning *""" ,
    #      ( post.title , post.content , post.published , str(id)) )
   # update_post = cursor.fetchone(),
   # conn.commit()
    post_query = db.query(models.User).filter(models.User.id == id)
    post = post_query.first()

    if post == None:
      raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , 
                                    detail = f"post with id {id} does not exit ")
    
   # post_dict = post.dict()
   # post_dict['id'] = id
   # my_posts[index] = post_dict

    post_query.update(updated_post.dict() , synchronize_session=False)
    db.commit()
    return{"data" : post_query.first()}
    
