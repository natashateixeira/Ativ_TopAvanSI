from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_chatbot_responde_pergunta():
    resposta = client.post("/api/chat", json={"message": "Tem pastilha de freio para CG 160?"})
    assert resposta.status_code == 200
    dados = resposta.json()
    assert "reply" in dados
    assert len(dados["products"]) > 0