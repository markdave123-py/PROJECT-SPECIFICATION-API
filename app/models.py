
from email.policy import default

from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, PrimaryKeyConstraint,String,ForeignKey
from sqlalchemy.orm import relationship
from .database import base 
from sqlalchemy.dialects import postgresql

from sqlalchemy.sql.expression import  text



class User(base):
    __tablename__ = 'users'

    
    first_name = Column(String, nullable= False)
    last_name = Column(String, nullable= False)
    user_name = Column(String, nullable= False)
    email = Column(String, unique= True, nullable= False)
    password = Column(String, nullable = False)
    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default= text('now()'), nullable=False)



class Project(base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable= False)
    description = Column(String, nullable= False)
    admins = Column(postgresql.ARRAY(String), nullable= False)
    participants = Column(postgresql.ARRAY(String), nullable= False)
    created_at = Column(TIMESTAMP(timezone=True), server_default= text('now()'), nullable=False)
    project_status = Column(String, nullable= False)
    

class Task(base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, nullable=False)
    description = Column(String, nullable= False)
    projectID = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable = False)
    assignedTo = Column(String, nullable = False)
    status = Column(String, nullable = False)
    deadline = Column(String, nullable = False)

