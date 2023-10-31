import time
timestr = time.strftime("%Y%m%d-%H%M%S")
from fastapi import FastAPI, UploadFile
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse
from minio import Minio
from minio.error import S3Error
import uvicorn
import json
import os
import yaml

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR,"uploads")
client = Minio(
        "localhost:9000",
        access_key="pJRORdLuySfaAuKk",
        secret_key="o98yqy5OZ4TTf1fIPS8EqXbrpkRyq9KK",
        secure=False
    )
found = client.bucket_exists("moein")
if not found:
    client.make_bucket("moein")
else:
    print("Bucket 'moein' already exists")

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
      client.fput_object(
          "moein", new_filename, SAVE_FILE_PATH,
      )
      print(
          "'/Users/moein/Desktop/playGrounds/fastapi_minio/app/test.json' is successfully uploaded as "
          "object 'asiaphotos-2015.zip' to bucket 'moein'."
      )

      return FileResponse(path=SAVE_FILE_PATH, media_type = "application/cotet-stream", filename = new_filename)








if __name__ == '__main__':
  uvicorn.run("app:app", host='127.0.0.1', port=8000, reload=True)