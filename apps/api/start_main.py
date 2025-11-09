import uvicorn
import app.main as main

if __name__ == "__main__":
    uvicorn.run(main.app,port=8080)