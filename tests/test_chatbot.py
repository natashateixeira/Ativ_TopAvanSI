from fastapi.testclient import TestClient
from app.main import app


def test_chatbot_responde_pergunta_compativel():
    with TestClient(app) as client:
        resposta = client.post("/api/chat", json={"message": "Tem pastilha de freio para CG 160?"})
        assert resposta.status_code == 200
        dados = resposta.json()
        assert "reply" in dados
        assert len(dados["products"]) > 0


def test_chatbot_item_inexistente():
    with TestClient(app) as client:
        resposta = client.post("/api/chat", json={"message": "Tem turbina de aviao para foguete?"})
        assert resposta.status_code == 200
        dados = resposta.json()
        assert dados["products"] == []


def test_chatbot_rejeita_mensagem_vazia():
    with TestClient(app) as client:
        resposta = client.post("/api/chat", json={"message": "   "})
        assert resposta.status_code == 422


def test_chatbot_rejeita_campo_extra():
    with TestClient(app) as client:
        resposta = client.post("/api/chat", json={"message": "oleo", "admin": True})
        assert resposta.status_code == 422