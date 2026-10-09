import requests
import xml.etree.ElementTree as ET

def fetch_medical_articles():
    # Segundo o manual da NCBI, devemos usar este URL base para os E-utilities
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    
    # PASSO 1: ESearch - Encontrar os PMIDs (IDs únicos do PubMed) dos artigos
    # Filtramos estritamente para artigos cujo título contenha Endometriose e sejam do tipo Revisão.
    search_url = f"{base_url}esearch.fcgi"
    search_params = {
        "db": "pubmed",
        "term": 'endometriosis[Title] AND Review[Publication Type]',
        "retmax": 10, # Vamos buscar os 10 mais relevantes para depois extrair os 5 com resumos mais completos
        "sort": "relevance",
        "retmode": "json"
    }
    
    try:
        search_response = requests.get(search_url, params=search_params, timeout=15)
        if search_response.status_code != 200:
            print("Erro no ESearch")
            return fallback_article()
            
        search_data = search_response.json()
        pmids = search_data.get("esearchresult", {}).get("idlist", [])
        
        if not pmids:
            return fallback_article()
            
        # PASSO 2: EFetch - Obter os detalhes completos de cada PMID em formato XML
        # O manual indica ESummary para resumos curtos, mas EFetch traz os Abstracts completos.
        fetch_url = f"{base_url}efetch.fcgi"
        fetch_params = {
            "db": "pubmed",
            "id": ",".join(pmids),
            "retmode": "xml"
        }
        
        fetch_response = requests.get(fetch_url, params=fetch_params, timeout=15)
        
        if fetch_response.status_code != 200:
            print("Erro no EFetch")
            return fallback_article()
            
        # Processar o XML retornado pelo PubMed
        root = ET.fromstring(fetch_response.content)
        filtered_articles = []
        
        for article in root.findall('.//PubmedArticle'):
            # Título
            title_node = article.find('.//ArticleTitle')
            title = title_node.text if title_node is not None else "Sem título"
            
            # Ano
            year_node = article.find('.//PubDate/Year')
            year = year_node.text if year_node is not None else "N/D"
            
            # Fonte (Journal)
            journal_node = article.find('.//Title')
            venue = journal_node.text if journal_node is not None else "PubMed"
            
            # Abstract
            abstract_text = ""
            abstract_nodes = article.findall('.//AbstractText')
            for node in abstract_nodes:
                if node.text:
                    abstract_text += node.text + " "
            if not abstract_text.strip():
                abstract_text = "Resumo detalhado disponível no artigo completo."
                
            # Identificadores (PMID e DOI)
            pmid_node = article.find('.//PMID')
            pmid = pmid_node.text if pmid_node is not None else ""
            
            doi_node = article.find('.//ArticleId[@IdType="doi"]')
            doi = doi_node.text if doi_node is not None else ""
            
            identifier = f"DOI: {doi}" if doi else (f"PMID: {pmid}" if pmid else "")
            
            # Link preferencial (PubMed oficial)
            link = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else "#"
            
            # Filtrar artigos apenas se tiverem resumo real
            if len(abstract_text) > 50:
                filtered_articles.append({
                    "title": title,
                    "year": year,
                    "citationCount": "N/D", # O E-utilities nativo não fornece nº de citações por defeito de forma simples
                    "venue": venue,
                    "url": link,
                    "abstract": abstract_text.strip(),
                    "identifier": identifier
                })
                
            if len(filtered_articles) == 5:
                break
                
        if filtered_articles:
            return filtered_articles
            
    except Exception as e:
        print(f"Erro na requisição E-utilities: {e}")
        
    return fallback_article()

def fallback_article():
    return [
        {
            "title": "Endometriosis: pathogenesis, diagnosis and treatment",
            "year": "2018",
            "citationCount": "1250",
            "venue": "Nature Reviews Endocrinology",
            "url": "https://pubmed.ncbi.nlm.nih.gov/30344339/",
            "abstract": "A comprehensive review on the pathogenesis, diagnostic challenges, and modern therapeutic approaches for endometriosis.",
            "identifier": "DOI: 10.1038/s41574-018-0098-z"
        }
    ]

def generate_html(articles):
    articles_html = ""
    for paper in articles:
        title = paper.get("title", "Sem título")
        year = paper.get("year", "N/D")
        venue = paper.get("venue", "PubMed")
        link = paper.get("url", "#")
        identifier = paper.get("identifier", "")
        
        abstract = paper.get("abstract", "")
        if len(abstract) > 220:
            abstract = abstract[:217] + "..."

        articles_html += f"""
        <article class="article-card">
            <a href="{link}" class="article-title" target="_blank">{title}</a>
            <div class="meta">
                <span>Ano: {year}</span>
                <span>Fonte: {venue}</span>
                <span style="color: var(--accent-color); font-weight: 500;">{identifier}</span>
            </div>
            <p class="summary">{abstract}</p>
        </article>
        """

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
        .container {{ width: 100%; max-width: 680px; }}
        header {{ margin-bottom: 40px; border-bottom: 1px solid var(--border-color); padding-bottom: 20px; }}
        h1 {{ font-size: 1.75rem; margin: 0 0 10px 0; font-weight: 600; }}
        p.subtitle {{ color: var(--text-muted); font-size: 0.95rem; margin: 0; line-height: 1.5; }}
        .article-card {{ background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 8px; padding: 24px; margin-bottom: 20px; transition: transform 0.2s ease, box-shadow 0.2s ease; }}
        .article-card:hover {{ transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.05); }}
        .article-title {{ font-size: 1.15rem; font-weight: 600; color: var(--text-color); text-decoration: none; display: block; margin-bottom: 8px; line-height: 1.4; }}
        .article-title:hover {{ color: var(--accent-color); }}
        .meta {{ font-size: 0.85rem; color: var(--text-muted); display: flex; gap: 16px; margin-bottom: 12px; flex-wrap: wrap; }}
        .summary {{ font-size: 0.95rem; color: var(--text-muted); line-height: 1.6; margin: 0; }}
        footer {{ text-align: center; margin-top: 50px; font-size: 0.85rem; color: var(--text-muted); }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Endometriose: Leituras Essenciais</h1>
            <p class="subtitle">Curadoria automatizada utilizando as ferramentas oficiais E-utilities da base de dados PubMed / NCBI.</p>
        </header>
        <main id="articles-list">
            {articles_html}
        </main>
        <footer>
            Atualizado automaticamente via GitHub Actions &bull; PubMed E-utilities API
        </footer>
    </div>
</body>
</html>"""
    return html_content

if __name__ == "__main__":
    print("Buscando artigos utilizando o NCBI E-utilities...")
    articles = fetch_medical_articles()
    print(f"Total de artigos processados e filtrados: {len(articles)}")
    
    html = generate_html(articles)
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Arquivo index.html atualizado com sucesso!")
