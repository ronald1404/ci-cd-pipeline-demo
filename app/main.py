"""API de exemplo para demonstrar um pipeline CI/CD completo.

A aplicação é propositalmente pequena — o foco do projeto é a esteira de
qualidade, build e publicação em volta dela, não a complexidade do código.
"""
from fastapi import FastAPI

app = FastAPI(
    title="CI/CD Pipeline Demo",
    description="API mínima usada para demonstrar um pipeline CI/CD com GitHub Actions.",
    version="1.0.0",
)


@app.get("/health")
def health() -> dict[str, str]:
    """Health check usado pelo smoke test do pipeline e por orquestradores."""
    return {"status": "ok"}


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "CI/CD Pipeline Demo - veja /docs para a API interativa."}


@app.get("/sum")
def sum_numbers(a: int, b: int) -> dict[str, int]:
    """Endpoint simples com lógica testável (serve de alvo para os testes unitários)."""
    return {"result": a + b}
