
#This program is a python written API that takes tasks.

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID, uuid4

#variable for efficiency
app = FastAPI()

# the class that will allow us to hold many different tasks.
class Task(BaseModel):
    id: Optional[UUID] = None
    title: str
    description: Optional[str] = None
    completed: bool = False


tasks = []


#This function posts a task by the user (CREATE)
@app.post("/tasks/", response_model=Task)
def create_taske(task: Task):
    '''
    This function creates a task
    param: task: Task
    return: task
    '''

    task.id = uuid4()
    tasks.append(task)
    return task

#This function allows the user to read from a selected ID.
@app.get("/tasks/", response_model=List[Task])
def read_tasks():
    '''
    This function allows you to read a task
    return: tasks
    '''
    return tasks


#This function gets a new task from the user (READ)
@app.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: UUID):
    '''
    This function allows the user to read tasks from the class id.
    param: task_id: UUID
    return: task
    '''

    for task in tasks:
        if task.id == task_id:
            return task

    raise HTTPException(status_code=404, detail="Task not found")


#This function puts in a new task by the user (UPDATE)
@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: UUID, task_update: Task):
    '''
    This function allows the user to update a task.
    param: task_id, task_update
    return updated_task
    '''

    for idx, task in enumerate(tasks):
        if task.id == task_id:
            updated_task = task.copy(update=task_update.dict(exclude_unset=True))
            tasks[idx] = updated_task
            return updated_task
        
    raise HTTPException(status_code=404, detail="Task Not found")
    

#This function Deletes a task.
@app.delete("/tasks/{task_id}", response_model=Task)
def delete_task(task_id: UUID):
    '''
    This function allows the user to delete a task.
    Param: task_id
    return: tasks.pop(idx)
    '''

    for idx, task in enumerate(tasks):
        if task.id == task_id:
            return tasks.pop(idx)
    
    raise HTTPException(status_code=404, detail="Task Not found")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
