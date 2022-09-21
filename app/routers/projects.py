
from typing import List, Optional
from ..database import  get_db
from .. import models,schemas, utils
from fastapi import status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
import random

from .. import autho2

router = APIRouter(prefix='/projects',tags=["Projects"])

status_project = ["little devlopments have began", "we are at the finish stage", "we just started", "we are confused","there is progress "]


@router.post('/')
def create_project(project:schemas.Create_project, db:Session = Depends(get_db),
                                            logged_in_user = Depends(autho2.get_current_user)):
                               

    creator_email = logged_in_user.email
    project_status = "Newly created, no development yet!"

    new_project = models.Project(admins = [creator_email], participants = [creator_email],
                **project.dict(), project_status= project_status)


    db.add(new_project)

    db.commit()
    db.refresh(new_project)
    
    return {
        'Project': new_project,
        'Message': 'new project created!!'
    }

@router.get('/',status_code=status.HTTP_200_OK,response_model=List[schemas.Get_project])
def get_projects(db: Session = Depends(get_db),limit: int = 30, search: Optional[str] = "", skip: int = 0):
    projects = db.query(models.Project).filter(models.Project.description.contains(search)).limit(limit).offset(skip).all()

    return projects

@router.get('/{id}',response_model=schemas.Get_project)
def get_project(id:int,db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == id).first()

    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project with id {id} not found")

    return project


@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_project(id:int, db: Session = Depends(get_db),user_loggedin = Depends(autho2.get_current_user)):
    project_query = db.query(models.Project).filter(models.Project.id == id)

    project = project_query.first()

    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project with id {id} not found")

    
    if user_loggedin.email not in project.admins:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="you can't delete this project go back to ur admin")

    project_query.delete(synchronize_session=False)
    db.commit()

    return {
        'message': "this message has been successfully deleted"
    }


@router.post('/{id}/participants')
def add_participants(id: int,participant: schemas.User ,db: Session = Depends(get_db), 
                                    admin = Depends(autho2.get_current_user)):
    
    project = db.query(models.Project).filter(models.Project.id == id).first()

    users = db.query(models.User).all()
    emails = []

    for user in users:
        emails.append(user.email)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no project with id {id}")

    if admin.email not in project.admins:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you cant perform this operation,only admins can !!!")

    if participant.email not in emails:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"there is no user with this email {participant.email}")

    if participant.email in project.participants:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="this user is already a participant!!")
        
    project.participants  = project.participants + [participant.email]
    project.project_status = random.choice(status_project)

    db.commit()


    return "This user is now a participant in this project"


@router.post('/{id}/admins')
def add_admin(id: int,new_admin: schemas.User ,db: Session = Depends(get_db), 
                                                    admin = Depends(autho2.get_current_user)):

    project = db.query(models.Project).filter(models.Project.id == id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no project with id {id}")

    if admin.email not in project.admins:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you cant perform this operation,only admins can !!!")

    if new_admin.email not in project.participants:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only a partiicipant can become an admin")

    project.admins = project.admins + [new_admin.email]

    db.commit()

    return "This participant is sucessfully upgraded to an admin"

@router.delete('/{id}/admins')  
def admin_to_participant(id: int,participant: schemas.user_email ,db: Session = Depends(get_db), 
                                        admin = Depends(autho2.get_current_user)):

    project_query = db.query(models.Project).filter(models.Project.id == id)

    project = project_query.first()

    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no project with id {id}")

    if admin.email not in project.admins:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only an admin can perform this action")

    if participant.email not in project.admins:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                                                    detail=f"{participant.email} is not an admin in this project")

    removed = utils.removing(project.admins, participant.email)

    
    added = utils.adding(project.participants, participant.email)

    

    project_query.update({models.Project.admins: removed, models.Project.participants: added}, synchronize_session=False)

    db.commit()

    return {
        "Message": f"This user {participant.email} is sucessfully moved from admin to participant"
    }


    


@router.delete('/{id}/participant')
def remove_participant(id: int,user_email: schemas.user_email,db: Session = Depends(get_db),
                                             admin = Depends(autho2.get_current_user)):
    
    project_query = db.query(models.Project).filter(models.Project.id == id)

    project = project_query.first()

    users = db.query(models.User).all()
    emails = []

    for user in users:
        emails.append(user.email)

    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no project with id {id}")

    if user_email.email not in emails:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"NO user has this email ")


    if admin.email not in project.admins:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only an admin can perform this action")

    if user_email.email not in project.participants:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"{user_email.email} is not a valid participant in this project")

    removed = utils.removing(project.participants, user_email.email)
    project_query.update({models.Project.participants: removed}, synchronize_session=False)
    
    db.commit()
    
      
    return {"participants": project.participants,
            "message": f"participant {user_email.email} has successfully been removed from this project!"
                            }

@router.get('/{id}/admins', response_model=List[schemas.User_response])
def get_admins(id: int, db: Session = Depends(get_db), user = Depends(autho2.get_current_user)):
    project = db.query(models.Project).filter(models.Project.id == id).first()
    
    users = db.query(models.User).all()

    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no project with id {id}")

    joined = project.participants + project.admins
    if user.email not in joined:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail='Only an admin or participant in this project can access this information')

    admins = []
    for user1 in users:
        if user1.email in project.admins:
            admins.append(user1)

    return admins

@router.get('/{id}/participants', response_model= List[schemas.User_response])
def get_participants(id: int, db: Session = Depends(get_db), user = Depends(autho2.get_current_user)):
    project = db.query(models.Project).filter(models.Project.id == id).first()

    
    users = db.query(models.User).all()

    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no project with id {id}")
    
    joined = project.participants + project.admins
    if user.email not in joined:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail='Only an admin or participant in this project can access this information')
    
    participants = []
    for user1 in users:
        if user1.email in project.participants:
            participants.append(user1)

    return participants

@router.get('/{id}/admins/{adminId}', response_model=schemas.User_response)
def get_adminById(id: int,adminId: int, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == id).first()

    user = db.query(models.User).filter(models.User.id == adminId).first()

    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no project with id {id}")

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no user with id {adminId}")

    if user.email not in project.admins:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'This user is not an Admin in this project ')
    
    return user

@router.get('/{id}/participants/{participantsId}', response_model=schemas.User_response)
def get_participantById(id: int, participantsId: int, db: Session = Depends(get_db)):

    project = db.query(models.Project).filter(models.Project.id == id).first()

    user = db.query(models.User).filter(models.User.id == participantsId).first()

    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no project with id {id}")

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no user with id {participantsId}")
    
    if user.email not in project.participants:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'This user is not a participant in this project ')

    return user

@router.delete('/{id}/participantLeave', status_code=status.HTTP_200_OK)
def leave_project(id: int, db: Session = Depends(get_db), loggedin_user =  Depends(autho2.get_current_user)):

    project_query = db.query(models.Project).filter(models.Project.id == id)

    project = project_query.first()

    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no project with id {id}")

    if loggedin_user.email not in project.participants:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='You are not a participant in this project')

    removed = utils.removing(project.participants, loggedin_user.email)

    

    project_query.update({models.Project.participants: removed}, synchronize_session=False)


    db.commit()


    return {
        "message": f"I don leave this project for who get am abegg "
    }


@router.delete('/{id}/adminLeave', status_code=status.HTTP_200_OK)
def leave_project(id: int, db: Session = Depends(get_db), loggedin_user =  Depends(autho2.get_current_user)):

    project_query = db.query(models.Project).filter(models.Project.id == id)

    project = project_query.first()

    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no project with id {id}")

    if loggedin_user.email not in (project.participants + project.admins):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='You are not a admin in this project')

    removed = utils.removing(project.participants, loggedin_user.email)

    removed_admin = utils.removing(project.admins, loggedin_user.email)

    project_query.update({models.Project.participants: removed,models.Project.admins: removed_admin}, synchronize_session=False)


    db.commit()


    return {
        "message": f"I don leave this project for who get am abegg i no do admin again"
    }

@router.post('/{id}/join')
def request_to_join(id: int, admin_email: schemas.Send,db: Session = Depends(get_db), 
                            requester = Depends(autho2.get_current_user)):
    
    project_query = db.query(models.Project).filter(models.Project.id == id)

    users = db.query(models.User).all()

    project = project_query.first()


    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no project with id {id}")


    if requester.email in (project.participants + project.admins):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                         detail="you are either an admin or a participants in this project")
    
    utils.sendEmail(sender_email=requester.email, sender_password= admin_email.google_authentication_password, 
                    receiver_email=admin_email.admin_email, subject="A Request to join your project", body=admin_email.body)

    return "your email would be reveiwed by an admin, look forward to recieving an email from us, thank you"




    

    
    



    





