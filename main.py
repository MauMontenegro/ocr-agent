from fastapi import FastAPI,File, UploadFile
import easyocr
import os
import shutil

app=FastAPI()
reader = easyocr.Reader(["en"],gpu=True)
UPLOAD_FOLDER="uploads"
os.makedirs(UPLOAD_FOLDER,exist_ok=True)

@app.post("/process")
async def process_image(files:list[UploadFile]=File(...)):
    for file in files:
        file_path=os.path.join(UPLOAD_FOLDER,file.filename)

        with open(file_path,"wb") as buffer:
            shutil.copyfileobj(file.file,buffer)

        result=reader.readtext(file_path,detail=0)
        extracted_text= "\n".join(result)

        os.remove(file_path)

        return {"text":extracted_text}
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)