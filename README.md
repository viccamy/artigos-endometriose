# Artigos Relevantes sobre Endometriose

Um curador automatizado de artigos científicos. Este projeto busca e exibe os 5 artigos de revisão mais relevantes sobre endometriose utilizando a base de dados oficial do PubMed/NCBI.

🌍 **Acesse o site:** [viccamy.github.io/artigos-endometriose](https://viccamy.github.io/artigos-endometriose/)

## Como funciona

O repositório opera de forma totalmente automatizada e sem necessidade de manutenção manual:

- **Busca de Dados:** O script `update.py` consome a API oficial do PubMed (E-utilities) para encontrar as principais revisões sobre o tema, extraindo título, revista, resumo e DOI/PMID.
- **Automação Semanal:** O GitHub Actions (`update.yml`) executa o script toda segunda-feira para gerar um novo `index.html` atualizado e faz o commit automático.
- **Hospedagem:** O GitHub Pages hospeda o site estático gerado, com uma interface rápida e responsiva construída em HTML5 e CSS3 puros.

## Tecnologias

- Python 3 (Requests, XML ElementTree)
- PubMed E-utilities API
- GitHub Actions (CI/CD)
- GitHub Pages
- HTML/CSS
