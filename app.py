from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import boto3
import os
from dotenv import load_dotenv

load_dotenv()
#fastapi application build
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all origins.  For production, you'd specify your frontend URL.
    allow_methods=["*"], # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"], # Allows all headers
)

# Initialize the S3 client
translate = boto3.client(
    'translate',
    region_name=os.getenv("AWS_REGION")
)

@app.post("/translate")
async def translate_text(request: Request):
    #Endpoint to handle text translation requests. Expects a JSON body with 'text', 'source', and 'target' language codes

    try: 
        body = await request.json()
        text = body["text"]
        source = body["source"]
        target = body["target"]

        #getting the response after translate
        response = translate.translate_text(
            Text = text,
            SourceLanguageCode = source,
            TargetLanguageCode = target
        )

        return {"translated" : response["TranslatedText"]}
    except Exception as e:
        return {"error": str(e)}, 500
