import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import json

app = FastAPI(title="Node M Backend")

# 1. CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Replace this with the EXACT name of your PDF in the folder
PDF_FILENAME = "Credit_Agreement_Hallador.pdf" 

# 2. Endpoint: Serve the Audited JSON Payload
@app.get("/api/document-data")
def get_document_data():
    try:
        with open("final_compiled_payload_audited.json", "r") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return {"error": "JSON payload not found. Ensure the file is in the backend directory."}

# 3. Endpoint: Serve the Source PDF
@app.get("/api/pdf")
def get_source_pdf():
    # Grab the absolute path to ensure we are looking in the exact right folder
    file_path = os.path.abspath(PDF_FILENAME)
    
    # Guardrail: Check if the file actually exists before serving
    if not os.path.exists(file_path):
        # If it fails, this will print the exact path it tried to search on your screen
        raise HTTPException(status_code=404, detail=f"PDF not found. Server looked here: {file_path}")
        
    return FileResponse(file_path, media_type="application/pdf")