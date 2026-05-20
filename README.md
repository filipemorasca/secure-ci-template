# 🔐 secure-ci-template

> **Template DevSecOps:** pipeline GitHub Actions pronto para uso, com SAST, scan de dependências, detecção de secrets e scan de filesystem. Use como ponto de partida para qualquer projeto Python que precise de segurança desde o dia 1.

[![Security Scan](https://github.com/filipemorasca/secure-ci-template/actions/workflows/security.yml/badge.svg)](https://github.com/filipemorasca/secure-ci-template/actions/workflows/security.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)

---

## 🎯 Problema

Times pequenos e desenvolvedores solo costumam **terceirizar segurança para "depois"** — quando "depois" geralmente significa "quando uma vulnerabilidade já foi explorada". A configuração inicial de scanners de segurança envolve juntar ferramentas, descobrir flags, integrar com CI, montar relatórios. Resultado: ninguém faz.

## 💡 Solução

Este repositório é um **template plug-and-play**. Você faz fork, e o pipeline já roda em todo push/PR/semanalmente:

| Camada | Ferramenta | O que faz |
|--------|-----------|-----------|
| 🐍 **SAST (código Python)** | [Bandit](https://github.com/PyCQA/bandit) | Detecta padrões inseguros no código (uso de `eval`, hashes fracos, SQL string concat, etc.) |
| 📦 **Dependências** | [pip-audit](https://github.com/pypa/pip-audit) | Cruza `requirements.txt` com a base PyPI Advisory e GHSA |
| 🔑 **Secrets** | [Gitleaks](https://github.com/gitleaks/gitleaks) | Varre o histórico do repo procurando chaves/tokens vazados |
| 📁 **Filesystem** | [Trivy](https://github.com/aquasecurity/trivy) | Scan de vulnerabilidades em arquivos, IaC e configs |

Cada job roda **independente** — se um quebrar, os outros continuam. Relatórios viram artefatos do GitHub Actions.

---

## 🚀 Quick start

### Usar como template

1. Clique em **"Use this template"** no topo deste repo
2. Crie seu novo repositório
3. Pronto. O workflow roda no primeiro push.

### Rodar localmente

```bash
git clone https://github.com/filipemorasca/secure-ci-template.git
cd secure-ci-template

python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Rodar a app demo
python src/app.py

# Rodar Bandit local
pip install bandit
bandit -r src -lll
```

---

## 📂 Estrutura

```
secure-ci-template/
├── .github/workflows/
│   └── security.yml          # Pipeline DevSecOps (este é o coração do projeto)
├── src/
│   └── app.py                # Flask app mínimo só para o pipeline ter o que escanear
├── docs/
│   ├── PIPELINE.md           # Detalhamento de cada job do workflow
│   └── FINDINGS-EXAMPLE.md   # Exemplos de findings reais que cada scanner pega
├── requirements.txt
├── LICENSE
└── README.md
```

---

## 🔍 O que cada scanner detecta (resumido)

> Para exemplos com input/output reais, veja [`docs/FINDINGS-EXAMPLE.md`](docs/FINDINGS-EXAMPLE.md).

- **Bandit**: `subprocess` com `shell=True`, `pickle.load` em dados externos, `hashlib.md5` para senhas, `assert` em código de produção, hardcoded passwords/keys, uso de `requests` sem verify SSL.
- **pip-audit**: Pacotes com CVEs publicados no PyPI Advisory Database (ex.: `Flask<2.2.5` com CVE-2023-30861).
- **Gitleaks**: AWS keys, GitHub tokens (`ghp_`, `gho_`), Slack tokens (`xox`), Stripe keys, JWT, chaves privadas (`-----BEGIN PRIVATE KEY-----`), arquivos `.env` commitados.
- **Trivy**: Vulnerabilidades em arquivos lock (`Pipfile.lock`, `poetry.lock`), Dockerfiles inseguros (uso de `latest`, `USER root`), Terraform mal configurado.

---

## 🛠 Customizando o pipeline

Para adicionar novas verificações, edite [`.github/workflows/security.yml`](.github/workflows/security.yml). Sugestões:

- **`semgrep`** — SAST multi-linguagem com regras configuráveis
- **`checkov`** — específico para Infrastructure as Code (Terraform, CloudFormation, Kubernetes)
- **`syft` + `grype`** — geração de SBOM e scan de container images
- **`cosign`** — assinatura de artefatos

---

## 🤔 Por que esse projeto existe

Este repo é parte do meu portfólio de transição para DevSecOps. Cibersegurança não é só pentest — é principalmente **integrar segurança ao ciclo de desenvolvimento sem virar gargalo**. Esse template materializa essa filosofia: o pipeline roda em segundos, não bloqueia o dev por padrão, e sobe os relatórios como artefato para revisão posterior.

A versão "bloqueante" (que falha o build em finding HIGH/CRITICAL) é fácil de habilitar — basta remover os `continue-on-error: true` no workflow.

---

## 📚 Referências

- [OWASP DevSecOps Guideline](https://owasp.org/www-project-devsecops-guideline/)
- [Bandit docs](https://bandit.readthedocs.io/)
- [pip-audit docs](https://pip-audit.readthedocs.io/)
- [Gitleaks](https://github.com/gitleaks/gitleaks)
- [Trivy](https://aquasecurity.github.io/trivy/)

---

## 🏷️ Topics sugeridos (configurar no GitHub)

`devsecops` · `sast` · `appsec` · `python` · `github-actions` · `security` · `cicd` · `bandit` · `pip-audit` · `gitleaks` · `trivy` · `template`

## 📜 Licença

MIT — veja [LICENSE](LICENSE).
