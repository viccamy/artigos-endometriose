import os
import requests

def fetch_top_articles():
    # Consulta a API pública do Semantic Scholar por artigos de endometriose ordenados por relevância/citações
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": "endometriosis review",
        "limit": 5,
        "sort": "citationCount:desc",
        "fields": "title,year,citationCount,url,abstract,openAccessPdf"
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("data", [])
    except Exception as e:
        print(f"Erro ao buscar artigos: {e}")
        return []

def generate_html(articles):
    articles_html = ""
    
    if not articles:
        articles_html = """
        <article class="article-card">
            <p class="summary">Não foi possível carregar os artigos no momento. Tentando novamente na próxima atualização.</p>
        </article>
        """
    else:
        for paper in articles:
            title = paper.get("title", "Sem título")
            year = paper.get("year", "N/D")
            citations = paper.get("citationCount", 0)
            
            # Prioriza link do PDF gratuito se houver, caso contrário usa o link geral do Semantic Scholar
            oa_pdf = paper.get("openAccessPdf")
            link = oa_pdf.get("url") if oa_pdf and oa_pdf.get("url") else paper.get("url", "#")
            
            abstract = paper.get("abstract") or "Resumo não disponível diretamente na base de dados. Clique no título para ler o artigo completo."
            # Limita o resumo a 200 caracteres para manter o design limpo
            if len(abstract) > 200:
                abstract = abstract[:197] + "..."

            articles_html += f"""
            <article class="article-card">
                <a href="{link}" class="article-title" target="_blank">{title}</a>
                <div class="meta">
                    <span>Ano: {year}</span>
                    <span>Citações: {citations}</span>
                </div>
                <p class="summary">{abstract}</p>
            </article>
            """

    # Template HTML atualizado com os novos artigos
    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Artigos Essenciais sobre Endometriose</title>
    <style>
        :root {{
            --bg-color: #faf9f6;
            --card-bg: #ffffff;
            --text-color: #2c2c2c;
            --text-muted: #666666;
            --accent-color: #8b5cf6;
            --border-color: #e5e5e5;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0;
            padding: 40px 20px;
            display: flex;
            justify-content: center;
        }}
        .container {{
            width: 100%;
            max-width: 680px;
        }}
        header {{
            margin-bottom: 40px;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 20px;
        }}
        h1 {{
            font-size: 1.75rem;
            margin: 0 0 10px 0;
            font-weight: 600;
        }}
        p.subtitle {{
            color: var(--text-muted);
            font-size: 0.95rem;
            margin: 0;
            line-height: 1.5;
        }}
        .article-card {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 24px;
            margin-bottom: 20px;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
        .article-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        }}
        .article-title {{
            font-size: 1.15rem;
            font-weight: 600;
            color: var(--text-color);
            text-decoration: none;
            display: block;
            margin-bottom: 8px;
            line-height: 1.4;
        }}
        .article-title:hover {{
            color: var(--accent-color);
        }}
        .meta {{
            font-size: 0.85rem;
            color: var(--text-muted);
            display: flex;
            gap: 16px;
            margin-bottom: 12px;
        }}
        .summary {{
            font-size: 0.95rem;
            color: var(--text-muted);
            line-height: 1.6;
            margin: 0;
        }}
        footer {{
            text-align: center;
            margin-top: 50px;
            font-size: 0.85rem;
            color: var(--text-muted);
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Endometriose: Leituras Essenciais</h1>
            <p class="subtitle">Curadoria automatizada com os 5 artigos mais relevantes e citados disponíveis na literatura científica global.</p>
        </header>

        <main id="articles-list">
            {articles_html}
        </main>

        <footer>
            Atualizado automaticamente via GitHub Actions &bull; Focado em evidência científica
        </footer>
    </div>
</body>
</html>
"""
    return html_content

if __name__ == "__main__":
    print("Buscando artigos...")
    articles = fetch_top_articles()
    print(f"Encontrados {len(articles)} artigos.")
    
    html = generate_html(articles)
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Arquivo index.html atualizado com sucesso!")
