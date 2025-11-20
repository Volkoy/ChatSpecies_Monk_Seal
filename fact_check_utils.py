"""
Fact-Check Tool - Intelligent Summarization and Verification
Generates summary text by combining knowledge base retrieval with optional web searches.
"""

import os
from langchain_community.llms import Tongyi
from dotenv import load_dotenv

load_dotenv()

def get_friendly_filename(source_file):
    """
    Convert technical source file names to user-friendly names
    """
    filename_mapping = {
        # Your Excel mappings
    '37_3_Adamantopoulou.pdf': 'Adamantopoulou et al 2011 - Movements of Mediterranean Monk Seals Monachus monachus in the Eastern Mediterranean Sea',
    'f0da61e8b1bd28b4546f409830e6ddd18257.pdf': 'Simopoulos et al 2013 - Social values of biodiversity conservation for Mediterranean monk seal Monachus monachus',
    'E-AC33-45-04.pdf': 'CITES Animals Committee 2024 - Periodic Review of Monachus tropicalis',
    '278-282-Vol19No2Erdem.pdf': 'Danyer et al 2013 - Preliminary report of a stranding case of Mediterranean Monk Seal Monachus monachus on Antalya coast Turkey',
    'Cave_habitats_used_by_Mediterranean_monk.pdf': 'Bundone 2010 - Cave habitats used by Mediterranean monk seals Monachus monachus in Sardinia',
    'the-mediterranean-monk-seal.pdf': 'Van Wijngaarden 1962 - The Mediterranean Monk Seal',
    'a-brief-note-on-mediterranean-monk-seal.pdf': 'Zareei 2021 - A Brief Note on Mediterranean Monk Seal',
    's41598-020-79712-1.pdf': 'Karamanlidis et al 2021 - Genetic and demographic history define a conservation strategy for earths most endangered pinniped the Mediterranean monk seal Monachus monachus',
    '2020 A Mediterranean Monk Seal Pup on the Apulian Coast (Southern Italy) Sign of an Ongoing Recolonisation.pdf': 'Fioravanti et al 2020 - A Mediterranean Monk Seal Pup on the Apulian Coast Southern Italy Sign of an Ongoing Recolonisation',
    'reestablishment_of_the_mediterranean_monk_seal_monachus_monachus_in_cyprus_priorities_for_conservation.pdf': 'Nicolaou et al 2021 - Re-establishment of the Mediterranean monk seal Monachus monachus in Cyprus priorities for conservation',
    'MA2379_lit180815.pdf': 'Mo et al 2004 - Habitat suitability and sightings of the Mediterranean monk seal in the National Park of Al Hoceima Morocco',
    'a4-flyer_270x194_marine-lifemonk-seal_eng_final.pdf': 'PPNEA undated - Mediterranean Monk Seal conservation flyer',
    '2013_Karamanlidisetal..pdf': 'Karamanlidis et al 2013 - Demographic Structure and Social Behavior of the Unique Mediterranean monk seal Monachus monachus colony of the Island of Gyaros',
    'Ilaria_Gradella.pdf': 'Gradella 2024 - The Mediterranean Monk Seal Monachus monachus Distribution Stranding and Major Threats',
    'mededelingen39_2008b.pdf': 'Johnson 2004 - Monk Seals in Post-Classical History Biography of the Mediterranean Monk Seal',
    '37_3_Adamantopoulou.pdf': 'Adamantopoulou et al 2010 - Movements of Mediterranean Monk Seals Monachus monachus in the Eastern Mediterranean Sea',
    'n045p315.pdf': 'Fernandez de Larrinoa et al 2021 - Age specific survival and reproductive rates of Mediterranean monk seals at the Cabo Blanco Peninsula West Africa',
    'AM-39.1-Alfaghi.pdf': 'Alfaghi et al 2013 - First Confirmed Sighting of the Mediterranean Monk Seal Monachus monachus in Libya Since 1972',
    'n053p341.pdf': 'Karamanlidis et al 2024 - Current status biology threats and conservation priorities of the Vulnerable Mediterranean monk seal',
    '44219.pdf': 'Bundone et al 2024 - Monitoring the Mediterranean monk seal in the central Mediterranean Sea',
    'guide.pdf': 'Johnson et al 1998 - The Mediterranean Monk Seal Conservation Guidelines',
    'the-mediterranean-monk-seal-karamanlidis-et-al-2015.pdf': 'Karamanlidis et al 2015 - The Mediterranean monk seal Monachus monachus status biology threats and conservation priorities',
    'strategie_phoque_en.pdf': 'UNEP-MAP SPA-RAC 2019 - Regional Strategy for the Conservation of Monk Seal in the Mediterranean',
    '2025-006-En.pdf': 'Quintana Martin-Montalvo et al 2025 - Mediterranean monk seal Monachus monachus A comprehensive set of monitoring and research techniques',
    'BDJ_article_120201.pdf': 'Valsecchi et al 2024 - An Observatory to monitor range extension of the Mediterranean monk seal based on its eDNA traces',
    'noaa_66431_DS1.pdf': 'Parsons 2024 - Mediterranean monk seal Monachus monachus 5 Year Review Summary and Evaluation',
        
        # Default fallback
        'unknown': 'Unknown Document'
    }
    
    base_name = os.path.basename(source_file) if source_file else 'unknown'
    return filename_mapping.get(base_name, base_name.replace('_', ' ').replace('-', ' ').title())


def summarize_fact_check(question, retrieved_docs, ai_answer, language="English"):
    """
    Intelligent Summarization of Fact-Checked Content
    
    Args:
        question: User query
        retrieved_docs: List of retrieved documents
        ai_answer: AI response
        language: Language (English/Portuguese)
    
    Returns:
        str: Summary text
    """
    # Extract document content
    doc_contents = []
    sources = []
    
    for i, doc in enumerate(retrieved_docs[:3], 1):  # Use a maximum of 3 documents
        content = doc.page_content[:500]  # Each document is limited to 500 characters.
        source = doc.metadata.get('source_file', 'Unknown')
        page = doc.metadata.get('page', 'N/A')

        friendly_name = get_friendly_filename(source)
        
        doc_contents.append(f"[Source {i}: {friendly_name}, Page {page}]\n{content}")
        sources.append(f"{friendly_name} (p.{page})")
    
    combined_docs = "\n\n".join(doc_contents)
    
    # Prompt for Building Abstracts
    if language == "Portuguese":
        prompt = f"""
        Tu és um verificador de factos científico. Com base nos documentos fornecidos, cria um resumo claro e conciso.

        **Pergunta do utilizador:** {question}

        **Resposta da IA:** {ai_answer}

        **Documentos de referência:**
        {combined_docs}

        **Tua tarefa:**
        1. Resume os pontos-chave dos documentos que apoiam a resposta
        2. Menciona dados específicos (números, locais, datas) se disponíveis
        3. Mantém o resumo abaixo de 100 palavras
        4. Usa linguagem simples e clara
        5. Se os documentos não apoiam a resposta, indica isso

        **Resumo factual:**
        """
    else:
        prompt = f"""
        You are a scientific fact-checker. Based on the provided documents, create a clear and concise summary.

        **User's Question:** {question}

        **AI's Answer:** {ai_answer}

        **Reference Documents:**
        {combined_docs}

        **Your Task:**
        1. Summarize key points from the documents that support the answer
        2. Mention specific data (numbers, locations, dates) if available
        3. Keep the summary under 100 words
        4. Use simple, clear language
        5. If documents don't support the answer, indicate that

        **Factual Summary:**
        """
    
    # Generate summaries using Qwen LLM
    try:
        api_key = os.getenv("DASHSCOPE_API_KEY")
        llm = Tongyi(
            model_name=os.getenv("QWEN_MODEL_NAME", "qwen-turbo"),
            temperature=0.3,  # Lower temperatures ensure factual accuracy.
            dashscope_api_key=api_key
        )
        
        summary = llm.invoke(prompt)
        
        # Add source citation
        if language == "Portuguese":
            source_text = f"\n\n📚 **Fontes:** {', '.join(sources)}"
        else:
            source_text = f"\n\n📚 **Sources:** {', '.join(sources)}"
        
        return summary.strip() + source_text
    
    except Exception as e:
        print(f"[Fact-Check] Abstract generation failed: {str(e)}")
        # Downgrade: Return simplified document content
        source = retrieved_docs[0].metadata.get('source_file', 'Unknown')
        page = retrieved_docs[0].metadata.get('page', 'N/A')
        friendly_name = get_friendly_filename(source)
        
        if language == "Portuguese":
            return f"📄 Informação extraída dos documentos:\n\n{retrieved_docs[0].page_content[:200]}...\n\n📚 Fonte: {friendly_name} (p.{page})"
        else:
            return f"📄 Information from documents:\n\n{retrieved_docs[0].page_content[:200]}...\n\n📚 Source: {friendly_name} (p.{page})"


def optimize_search_query(question, retrieved_docs):
    """
    Optimize Search Queries Based on User Questions and RAG-Retrieved Content
    
    Args:
        question: User's original question
        retrieved_docs: Documents retrieved by RAG
    
    Returns:
        str: Optimized search query
    """
    # Extract key concepts from RAG documentation
    rag_keywords = set()
    for doc in retrieved_docs[:2]:  # Only view the top 2 most relevant documents
        content = doc.page_content.lower()
        # Extract key biological/conservation-related vocabulary
        bio_keywords = ['monk seal', 'mediterranean monk seal', 'seal', 'endemic', 'madeira', 'conservation', 
                        'endangered', 'breeding', 'pup', 'habitat', 'species', 'population', 'marine',
                        'monachus', 'monachus monachus', 'coastal', 'ocean', 'marine mammal']
        for keyword in bio_keywords:
            if keyword in content:
                rag_keywords.add(keyword)
    
    # Build Precise Search Queries
    base_query = "Mediterranean monk seal"
    
    # Add relevant contextual keywords
    if 'conservation' in rag_keywords or 'endangered' in rag_keywords:
        base_query += " conservation status"
    elif 'breeding' in rag_keywords or 'nesting' in rag_keywords:
        base_query += " breeding habitat"
    elif 'madeira' in rag_keywords:
        base_query += " Madeira island"
    else:
        base_query += " marine mammal biology"
    
    # Add English keywords to ensure search quality.
    base_query += " seal species"
    
    return base_query



def filter_search_results(results, question):
    """
    Intelligently filter search results to exclude irrelevant content
    
    Args:
        results: Raw list of search results
        question: User query
    
    Returns:
        list: Filtered list of relevant results
    """
    filtered = []
    
    # Related Keywords (Biology/Conservation)
    relevant_keywords = [
        'monk seal', 'seal', 'marine mammal', 'species', 'madeira', 'conservation', 
        'endangered', 'breeding', 'habitat', 'marine biology', 'wildlife',
        'monachus', 'mediterranean', 'endemic', 'biodiversity', 'coastal',
        'pup', 'colony', 'protected', 'marine', 'ocean'
    ]
    
    # Irrelevant Keywords (Technology/Programming Related)
    irrelevant_keywords = [
        'framework', 'programming', 'code', 'software', 'api', 'rust',
        '编程', '框架', '开发', '代码', 'github', 'npm', 'cargo'
    ]
    
    for result in results:
        title = result.get('title', '').lower()
        body = result.get('body', '').lower()
        combined = title + ' ' + body
        
        # Check if it contains irrelevant keywords
        has_irrelevant = any(keyword in combined for keyword in irrelevant_keywords)
        if has_irrelevant:
            print(f"[Fact-Check] Filter out irrelevant results: {result.get('title', 'Unknown')[:50]}...")
            continue
        
        # Check if it contains relevant keywords
        has_relevant = any(keyword in combined for keyword in relevant_keywords)
        if has_relevant:
            filtered.append(result)
        else:
            # Additional check: If the title explicitly includes the name of a key species, retain it as well.
            title_lower = title.lower()
            if any(name in title_lower for name in ['monk seal', 'madeira monk seal', 'mediterranean monk seal']):
                filtered.append(result)
    
    
    return filtered


def web_search_supplement(question, retrieved_docs=None, language="English"):
    """
    Smart Web Search Supplement
    Supports DuckDuckGo (free) and Tavily (requires API Key)
    
    Args:
        question: User query
        retrieved_docs: Documents retrieved by RAG (for query optimization)
        language: Language
    
    Returns:
        str: Web search result summary (if enabled)
    """
    # Check if network search is enabled
    use_web_search = os.getenv("USE_WEB_SEARCH", "false").lower() == "true"
    
    if not use_web_search:
        return None
    
    # Optimizing Search Queries (Based on RAG Context)
    if retrieved_docs and len(retrieved_docs) > 0:
        optimized_query = optimize_search_query(question, retrieved_docs)
        print(f"[Fact-Check] Optimize Search Queries: {optimized_query}")
    else:
        optimized_query = f"Mediterranean monk seal {question} marine mammal"
    
    # Get Search Provider (Default: DuckDuckGo)
    provider = os.getenv("WEB_SEARCH_PROVIDER", "duckduckgo").lower()
    
    # Option 1: DuckDuckGo (Completely free, no API key required)
    results = []  # Initialize the results variable
    
    if provider == "duckduckgo":
        try:
            from ddgs import DDGS
            
            # Use the new API (no context manager required)
            ddgs = DDGS()
            # New API: The parameter name is query instead of keywords.
            raw_results = list(ddgs.text(
                query=optimized_query,
                max_results=5  # Get more results and filter them later.
            ))
            
            # Smart Filtered Results
            results = filter_search_results(raw_results, question)
            print(f"[Fact-Check] raw results: {len(raw_results)} → After filtering: {len(results)}")
            
            if results:
                if language == "Portuguese":
                    summary = "🌐 **Informação da Internet:**\n\n"
                else:
                    summary = "🌐 **Internet Information:**\n\n"
                
                # Show only the top 2 most relevant results
                for i, result in enumerate(results[:2], 1):
                    title = result.get('title', 'Unknown')
                    body = result.get('body', '')[:150]
                    url = result.get('href', '')
                    
                    summary += f"{i}. **{title}**\n   {body}...\n   🔗 {url}\n\n"
                
                return summary.strip()
        
        except ImportError:
            print("[Fact-Check] DDGS Not installed, running: pip install ddgs")
        except Exception as e:
            print(f"[Fact-Check] DuckDuckGo Search failed: {str(e)}")
            print(f"[Fact-Check] Try downgrading to Tavily...")
    
    # Option 2: Tavily (Requires API Key, 1000 free requests/month)
    # If DuckDuckGo fails or the provider is set to tavily, try Tavily
    if provider == "tavily" or (provider == "duckduckgo" and len(results) == 0):
        try:
            tavily_key = os.getenv("TAVILY_API_KEY")
            if tavily_key and tavily_key != "tvly-your-api-key":
                from tavily import TavilyClient
                
                client = TavilyClient(api_key=tavily_key)
                response = client.search(
                    query=f"Mediterranean monk seal {question}",
                    max_results=2,
                    search_depth="basic"
                )
                
                if response and 'results' in response:
                    results = response['results'][:2]
                    
                    if language == "Portuguese":
                        summary = "🌐 **Informação da Internet:**\n\n"
                    else:
                        summary = "🌐 **Internet Information:**\n\n"
                    
                    for i, result in enumerate(results, 1):
                        title = result.get('title', 'Unknown')
                        content = result.get('content', '')[:150]
                        url = result.get('url', '')
                        
                        summary += f"{i}. **{title}**\n   {content}...\n   🔗 {url}\n\n"
                    
                    return summary.strip()
        
        except ImportError:
            print("[Fact-Check] Tavily Not installed, running: pip install tavily-python")
        except Exception as e:
            print(f"[Fact-Check] Tavily Search failed: {str(e)}")
    
    return None


def generate_fact_check_content(question, retrieved_docs, ai_answer, language="English"):
    """
    Generate complete fact-check content (intelligent optimization version)
    
    Args:
        question: User question
        retrieved_docs: Retrieved documents
        ai_answer: AI response
        language: Language
    
    Returns:
        str: Fact-check content in HTML format
    """
    # 1. Generate a knowledge base summary
    kb_summary = summarize_fact_check(question, retrieved_docs, ai_answer, language)
    
    # 2. Optional: Intelligent Network Search Supplement (Passing RAG documents to optimize search queries)
    web_summary = web_search_supplement(
        question=question, 
        retrieved_docs=retrieved_docs,  # Passing RAG Context to Optimize Search
        language=language
    )
    
    # 3. Combined Content
    if language == "Portuguese":
        header = "📋 **Verificação de Factos Baseada em Conhecimento Científico**\n\n"
    else:
        header = "📋 **Fact-Check Based on Scientific Knowledge**\n\n"
    
    content = header + kb_summary
    
    if web_summary:
        content += f"\n\n---\n\n{web_summary}"
    
    return content

