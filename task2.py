from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import io
from task1 import ProcessExcel
app = FastAPI()

@app.post("/process_data")
async def create_upload_file(file: UploadFile):
    try:
        content = await file.read()
        obj = ProcessExcel(io.StringIO(content.decode("utf-8")))
        data = obj.read_csv()
        return JSONResponse(content=data, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
 

