
from fastapi import FastAPI                                         #importing fast api 
                                                                    # used to define a schema a particular set format of da      
from. import models
from .database import engine                                                   
from .routers import post, user ,authentication , votes
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)                        # binding engine
app = FastAPI()  # instance 


origins =["https://www.google.com"] 


app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(post.router)                                     # routing the router to post file so we could use it as a replacement of app with router
app.include_router(user.router)                                     # for user file routing
app.include_router(authentication.router)
app.include_router(votes.router)



@app.get("/")                                                         # decorator that gives meaning to the given code 
                                                                       # "/" is the end point of the url it is the root path for url 
async def root():                                                      # async function with a http request we can have multiple http
                                                                     # requests like get , head , delete etc 
                                                                     # root is a function name we can change it 
                
    return {"message": "hi welcome to fast api"}

