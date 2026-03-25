#!/usr/bin/env bash
set -euo pipefail

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Erro: esta pasta nao e um repositorio Git."
  exit 1
fi

if [[ $# -eq 0 ]]; then
  echo "Uso: ./git-flow.sh \"mensagem do commit\""
  exit 1
fi

COMMIT_MSG="$*"

if [[ -z "$(git status --porcelain)" ]]; then
  echo "Nada para commitar. O repositorio esta limpo."
  exit 0
fi

BRANCH_NAME="$(git branch --show-current)"
if [[ -z "$BRANCH_NAME" ]]; then
  echo "Erro: nao foi possivel identificar a branch atual."
  exit 1
fi

echo "Adicionando arquivos..."
git add .

echo "Criando commit..."
git commit -m "$COMMIT_MSG"

echo "Enviando para origin/$BRANCH_NAME..."
git push -u origin "$BRANCH_NAME"

echo "Fluxo concluido com sucesso."