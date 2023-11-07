from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from vertexai.language_models import ChatModel, InputOutputTextPair
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

origin=["*"]

app.add_middleware(CORSMiddleware, allow_origins=origin, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/")
async def health_check():
    return {"status": "success"}

@app.websocket("/chat")
async def chat(websocket: WebSocket):
    await websocket.accept()

    chat_model = ChatModel.from_pretrained('chat-bison@001')

     # TODO developer - override these parameters as needed:
    parameters = {
        "temperature": 0.2,  # Temperature controls the degree of randomness in token selection.
        "max_output_tokens": 256,  # Token limit determines the maximum amount of text output.
        "top_p": 0.95,  # Tokens are selected from most probable to least until the sum of their probabilities equals the top_p value.
        "top_k": 40,  # A top_k of 1 means the selected token is the most probable among all tokens.
    }

    chat = chat_model.start_chat(
        context="You are a helpful assistant."
    )
    while(True):
        try:
            msg = await websocket.receive_text()
            response = chat.send_message(message=msg, **parameters)
            await websocket.send_text(response.text)
        except WebSocketDisconnect:
            break
