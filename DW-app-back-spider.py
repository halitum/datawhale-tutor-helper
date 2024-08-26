from datetime import datetime
from fastapi import FastAPI, HTTPException
from spider import fetch_and_save_content_with_selenium

app = FastAPI()

@app.get("/fetch-content/")
def fetch_content(url: str):
    current_date = datetime.now().strftime("%Y-%m-%d")
    file_name = current_date + '.txt'
    fetch_and_save_content_with_selenium(url, file_name)
    with open(file_name, "r", encoding="utf-8") as file:
        content = file.read()
    return {"content": content}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)