# CI/CD Pipeline Demo

Pipeline de **CI/CD completo** com GitHub Actions para uma API em Python (FastAPI),
demonstrando a esteira de **qualidade → build → publicação** de uma imagem Docker.

O foco deste repositório **não é a aplicação** (que é mínima de propósito), e sim a
automação em volta dela: lint, testes, build de imagem com boas práticas e
publicação versionada no GitHub Container Registry (GHCR).

## Arquitetura do pipeline

```
 push / pull_request
         │
         ▼
   ┌──────────┐     ┌──────────┐
   │   lint   │     │   test   │      (rodam em paralelo)
   │  (ruff)  │     │ (pytest) │
   └────┬─────┘     └────┬─────┘
        └──────┬─────────┘
               ▼
        ┌──────────────┐
        │  build-push  │   needs: [lint, test]
        │  (Docker +   │   push para o GHCR só na branch main
        │    GHCR)     │   (em PR: builda mas não publica)
        └──────────────┘
```

- **lint** e **test** rodam em paralelo (portões baratos primeiro; falham rápido).
- **build-push** só executa se os dois passarem (`needs`), e só **publica** a imagem
  em push na `main` — em Pull Request a imagem é construída (valida o Dockerfile) mas
  não é publicada.
- Tags geradas automaticamente: `sha-<commit>` (rastreável) e `latest` na main.

## Stack

| Camada | Tecnologia |
|--------|-----------|
| Aplicação | Python 3.10 + FastAPI |
| Lint | ruff |
| Testes | pytest |
| Container | Docker (multi-stage-ready, usuário não-root, healthcheck) |
| CI/CD | GitHub Actions |
| Registry | GitHub Container Registry (ghcr.io) |

## Como rodar localmente

```bash
# 1. Ambiente e dependências
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt

# 2. Qualidade (o que o pipeline roda)
ruff check .
pytest -q

# 3. Rodar a API
uvicorn app.main:app --reload
# http://localhost:8000/docs  (Swagger)  |  /health  |  /sum?a=2&b=3
```

### Via Docker

```bash
docker build -t ci-cd-demo .
docker run -p 8000:8000 ci-cd-demo
curl http://localhost:8000/health   # {"status":"ok"}
```

## Decisões técnicas (por quê)

- **lint e test em jobs separados e paralelos:** feedback mais rápido e falhas isoladas
  (dá pra ver num relance se quebrou o estilo ou a lógica).
- **build-push com `needs`:** a imagem só é construída se a qualidade passar — não se
  publica código que não passou nos testes.
- **push só na `main`:** PRs validam o build sem poluir o registry; a publicação é um
  evento da branch principal.
- **tag por SHA do commit:** toda imagem é rastreável até o commit exato que a gerou
  (essencial para rollback e auditoria).
- **imagem com usuário não-root + healthcheck:** reduz superfície de ataque e permite
  que orquestradores saibam quando o container está saudável.
- **cache de pip e de build (`type=gha`):** builds mais rápidos reaproveitando camadas.

## Próximos passos (roadmap)

- [ ] Deploy contínuo para um ambiente real (ex.: `docker compose` num VPS, ou AWS ECS).
- [ ] Scan de segurança da imagem (Trivy) como gate no pipeline.
- [ ] Cobertura de testes publicada no PR.
