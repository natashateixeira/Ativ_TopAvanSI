from fastapi.testclient import TestClient
from app.main import app


def test_chatbot_suporte_reembolso():
    with TestClient(app) as client:
        resposta = client.post("/api/chat", json={"message": "Como funciona o reembolso?"})
        assert resposta.status_code == 200
        dados = resposta.json()
        assert dados["category"] == "reembolso"
        assert "simulados" in dados["reply"].lower()


def test_chatbot_suporte_problema_pedido():
    with TestClient(app) as client:
        resposta = client.post("/api/chat", json={"message": "Tive um problema com meu pedido"})
        assert resposta.status_code == 200
        dados = resposta.json()
        assert dados["category"] == "suporte_pedido"


def test_chatbot_suporte_contato():
    with TestClient(app) as client:
        resposta = client.post("/api/chat", json={"message": "Quero entrar em contato com um atendente"})
        assert resposta.status_code == 200
        dados = resposta.json()
        assert dados["category"] == "contato"
        assert "suporte@rota2motopecas.example" in dados["reply"]


def test_chatbot_consulta_catalogo():
    with TestClient(app) as client:
        resposta = client.post("/api/chat", json={"message": "Tem pastilha de freio para CG 160?"})
        assert resposta.status_code == 200
        dados = resposta.json()
        assert dados["category"] == "catalogo"
        assert len(dados["products"]) > 0


def test_chatbot_rejeita_mensagem_vazia():
    with TestClient(app) as client:
        resposta = client.post("/api/chat", json={"message": "   "})
        assert resposta.status_code == 422


def test_chatbot_rejeita_campo_extra():
    with TestClient(app) as client:
        resposta = client.post("/api/chat", json={"message": "contato", "admin": True})
        assert resposta.status_code == 422