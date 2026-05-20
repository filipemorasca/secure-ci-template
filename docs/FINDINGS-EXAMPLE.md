# Exemplos de findings

Este documento mostra **inputs vulneráveis** e **o que cada scanner reportaria**. Útil para entender o valor do pipeline antes de integrar em um projeto real.

> ⚠️ Os snippets abaixo **NÃO estão no código deste repo**. São exemplos didáticos do que os scanners detectariam se estivessem.

---

## Bandit (SAST)

### Caso 1 — Command injection

```python
import subprocess
def run_user_input(cmd):
    subprocess.call(cmd, shell=True)  # ❌ injeção
```

**Bandit:**
```
>> Issue: [B602:subprocess_popen_with_shell_equals_true]
   subprocess call with shell=True identified, security issue.
   Severity: High   Confidence: High
   Location: app.py:3
```

### Caso 2 — Hash fraco para senha

```python
import hashlib
hashed = hashlib.md5(password.encode()).hexdigest()  # ❌ MD5 quebrado
```

**Bandit:**
```
>> Issue: [B303:blacklist] Use of insecure MD2, MD4, MD5, or SHA1 hash function.
   Severity: Medium   Confidence: High
```

### Caso 3 — Assert em código sensível

```python
def admin_only(user):
    assert user.is_admin  # ❌ removido em produção com python -O
    do_admin_stuff()
```

**Bandit:**
```
>> Issue: [B101:assert_used] Use of assert detected.
```

---

## pip-audit

### `requirements.txt` vulnerável

```
Flask==2.2.2
```

**pip-audit:**
```
Found 1 known vulnerability in 1 package
Name   Version  ID                   Fix Versions
----   -------  ----                 ------------
flask  2.2.2    PYSEC-2023-62        2.2.5
                                     (CVE-2023-30861 — cookie leakage)
```

**Como corrigir:** bump para versão fixada e revalidar.

---

## Gitleaks

### Commit com `.env`

```
# .env
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

**Gitleaks:**
```
finding: aws-access-token
secret:  AKIAIOSFODNN7EXAMPLE
file:    .env
commit:  a1b2c3d (HEAD)
author:  user <user@example.com>
date:    2026-01-15T10:23:00Z
```

**Ação correta:** revogar a key imediatamente na AWS, criar nova, atualizar consumidores. Apenas remover do repo NÃO resolve — o histórico (e qualquer fork) ainda tem.

---

## Trivy

### Dockerfile inseguro

```dockerfile
FROM python:latest          # ❌ tag mutável
RUN pip install requests    # ❌ sem versão fixa
USER root                   # ❌ rodando como root
```

**Trivy:**
```
HIGH: Image using mutable tag 'latest'
HIGH: Container running as root user (DS002)
MEDIUM: requests installed without version pin
```

---

## Como usar esse documento

Em entrevista técnica, esses casos servem como **resposta concreta** a perguntas tipo:
- "O que sua pipeline pega?"
- "Como você integra segurança no fluxo de dev?"
- "Cite um exemplo de finding que você tratou."

Saber **explicar o que cada scanner faz, com input/output**, vale mais do que ter integrado 20 ferramentas e não saber explicar nenhuma.
