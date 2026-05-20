# Pipeline DevSecOps — detalhamento

O workflow [`.github/workflows/security.yml`](../.github/workflows/security.yml) executa quatro jobs em paralelo. Cada um cobre uma camada diferente da pirâmide de DevSecOps.

## Quando o pipeline roda

- **`push` para `main`** — proteção do branch principal
- **`pull_request` para `main`** — feedback antes do merge
- **`schedule` semanal** — pega CVEs novos descobertos em deps antigas

## Jobs

### 1. SAST — Bandit
Análise estática de código Python. Procura padrões inseguros no próprio código (não em deps).

**Severidade configurada**: `-lll` (apenas HIGH).

**Exemplos de findings que pega**:
- `subprocess.call(cmd, shell=True)` — injeção de comando
- `hashlib.md5(password)` — hash fraco para senha
- `pickle.loads(data)` — desserialização insegura
- `assert user.is_admin` — `assert` é removido com `python -O`

### 2. Deps — pip-audit
Cruza `requirements.txt` com PyPI Advisory Database e GHSA.

**Quando isso importa**: 90% das vulnerabilidades exploradas em apps modernos vêm de bibliotecas, não do código próprio. Esse scanner é o que pega Log4Shell-class de problema (mas no ecossistema Python).

### 3. Secrets — Gitleaks
Varre o **histórico inteiro** do repo procurando credenciais vazadas.

**Por que `fetch-depth: 0`**: precisa do histórico completo. Senão, gitleaks só olha o último commit.

**O que pega**: AWS keys, GitHub tokens, Stripe keys, Slack webhooks, JWT, RSA/PGP private keys, padrões customizados (configuráveis em `.gitleaks.toml`).

### 4. Filesystem — Trivy
Scan polivalente: vulnerabilidades em lock files, problemas em Dockerfiles, misconfigurations em Terraform/Kubernetes, secrets (sobreposto ao Gitleaks).

**Output em SARIF**: o passo `upload-sarif` joga os findings na aba **Security → Code scanning alerts** do GitHub, integrado com o resto da plataforma.

## Modo bloqueante vs informativo

O pipeline está em modo **informativo** por default: ele reporta mas não falha o build em finding. Para virar **bloqueante**:

1. Em `bandit` e `pip_audit`, remova os `|| true` dos comandos
2. Em `trivy`, adicione `exit-code: 1` no input do action

Recomendação: começar informativo, ler os relatórios por uma semana, ir promovendo para bloqueante por job conforme o backlog de findings é zerado.

## Limites conhecidos

- **Bandit** não pega tudo. SAST tem alto falso-negativo. Complemente com revisão manual em código sensível (auth, crypto, deserialization).
- **pip-audit** depende do PyPI Advisory ser atualizado. CVEs muito novos podem demorar a aparecer.
- **Gitleaks** só pega o que está no histórico. Se você commitou e fez `force-push` para remover, o secret pode ainda estar em fork/cache. Sempre **rotacione** após vazamento, não apenas remova.
