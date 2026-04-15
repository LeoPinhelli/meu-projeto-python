# meu-projeto-python

Pequena CLI para organizar o aprendizado de uma linguagem, framework ou ferramenta.

## Ideia do projeto

A proposta e ajudar a montar um plano simples de estudo, guardar os itens em um arquivo local e sugerir o proximo foco quando voce quiser continuar aprendendo.

## Como usar

```bash
py -3 main.py seed
py -3 main.py list
py -3 main.py add FastAPI framework 3
py -3 main.py done 1
py -3 main.py stats
py -3 main.py recommend
```

Se o comando `py` nao existir no seu computador, use o executavel Python que estiver instalado e acessivel no PATH.

## O que o projeto faz

- adiciona objetivos de estudo
- lista os objetivos salvos
- marca itens como concluidos
- mostra estatisticas basicas
- sugere o proximo foco de aprendizado

## Arquivo gerado

Os dados ficam em `learning_plan.json`, criado automaticamente na primeira escrita.
