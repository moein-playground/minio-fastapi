import time
timestr = time.strftime("%Y%m%d-%H%M%S")
from fastapi import FastAPI, UploadFile
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse
import uvicorn
import json
import os
import yaml

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR,"uploads")


@app.get("/")
async def root():
  return {"Message":"Hello moein"}

@app.post("/file/upload")
async def uploadFile(file:UploadFile):
  if file.content_type != "application/json":
    print(f"content type: {file.content_type}")
    raise HTTPException(400, detail="Invalid document typeeee")
  else:
    data = json.loads(file.file.read())
    return {"content": data, "filename":file.filename}

@app.post("/file/uploadndownload")
def upload_n_download(file:UploadFile):
    """return a YML file for the upladed JSON file"""
    if file.content_type != "application/json":
      print(f"content type: {file.content_type}")
      raise HTTPException(400, detail="Invalid document typeeee")
    else:
      json_data = json.loads(file.file.read())
      new_filename = "{}_{}.yaml".format(os.path.splitext(file.filename)[0],timestr)
      SAVE_FILE_PATH = os.path.join(UPLOAD_DIR, new_filename)

      with open(SAVE_FILE_PATH, "w") as f:
        yaml.dump(json_data, f)


      return FileResponse(path=SAVE_FILE_PATH, media_type = "application/cotet-stream", filename = new_filename)








if __name__ == '__main__':
  uvicorn.run("app:app", host='127.0.0.1', port=8000, reload=True)