from typing import List, Optional
from ..database import  get_db
from .. import database, models,schemas,utils
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from datetime import *

from .. import autho2

router = APIRouter(prefix='/projects',tags=["Tasks(specify the deadline (days) at the end of the create_task router)"])

@router.post('/{id}/tasks', response_model=schemas.Task_create_response)
def create_task(id: int, task: schemas.Task_request,db: Session = Depends(get_db), 
                                            admin = Depends(autho2.get_current_user)):
    project = db.query(models.Project).filter(models.Project.id == id).first()

    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No prject with id {id}")

    if admin.email not in project.admins:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Only an admin can create or assign a task")

    if task.assignedTo not in project.participants:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, 
                                                detail="The task should only be assigned to a participant in this project")

    expire = int(datetime.now().day) + task.deadline
    deadline_time = f"{datetime.now().year}/{datetime.now().month}/{expire}"
    new_deadline = utils.convert_month_day(deadline_time)

    new_task = models.Task(projectID = id,**task.dict())


    db.add(new_task)

    db.commit()

    db.refresh(new_task)

    task_query = db.query(models.Task).filter(models.Task.id == new_task.id)

    task_query.update({models.Task.deadline: new_deadline}, synchronize_session=False)

    db.commit()



    return {
        'Data': new_task,
        'Message': f"Task is successfully created and assigned to {task.assignedTo}"
    }

@router.get('/{id}/tasks', response_model=List[schemas.Tasks_response])
def get_tasks(id: int, db: Session = Depends(get_db),limit: int = 30, statuses: Optional[str] = "", skip: int = 0):

    project = db.query(models.Project).filter(models.Project.id == id).first()


    tasks = db.query(models.Task).filter(models.Task.projectID == id 
                                        and models.Task.status.contains(statuses)).limit(limit).offset(skip).all()

    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,detail=f"No prject with id {id}")

    if tasks == []:
        return "There is no task created assigned"


    return tasks


@router.put('/{id}/tasks/{taskid}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Task_create_response)
def update_status(id: int, taskid: int,task_status: schemas.Task_status ,db: Session = Depends(get_db), admin = Depends(autho2.get_current_user)):
    project = db.query(models.Project).filter(models.Project.id == id).first()
    task_query = db.query(models.Task).filter(models.Task.id == taskid and models.Task.projectID == id)

    task = task_query.first()

    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"no project with id {id}")

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No task with Id {taskid}") 

    if task.projectID != id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'This project doesnot have a task with id {taskid}')  

    if admin.email != task.assignedTo:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                                            detail=f"Only someone assigned this task can perform this operaton")



    task_query.update({models.Task.status: task_status.status}, synchronize_session=False)

    db.commit()

    return {
        "Data": task_query.first(),
        "Message": "Task status is successfully updated"
    }

@router.delete('/{id}/tasks/{taskid}', status_code=status.HTTP_204_NO_CONTENT)
def delete_task(taskid: int,id: int,db: Session = Depends(get_db),admin = Depends(autho2.get_current_user)):

    task_query = db.query(models.Task).filter(models.Task.id == taskid and models.Task.projectID == id)

    task = task_query.first()

    project = db.query(models.Project).filter(models.Project.id == id).first()

    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No project with id {id}")

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No task with id {taskid}")

    if task.projectID != id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'This project doesnot have a task with id {taskid}') 
        
    if admin.email not in project.admins:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f'Only an admin can perform this action!!')

     

    

    task_query.delete(synchronize_session=False)

    db.commit()

    return {
        'Message': "This task have been successfully deleted"
    }


    

