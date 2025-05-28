// Practical Search API Implementation
// Ready-to-use examples for alternative search solutions

class AlternativeSearchService {
  constructor() {
    this.cache = new Map();
    this.cacheTimeout = 5 * 60 * 1000; // 5 minutes
  }

  // 1. DuckDuckGo Search (Free, No API Key Required)
  async duckDuckGoSearch(query) {
    const cacheKey = `ddg_${query}`;
    if (this.cache.has(cacheKey)) {
      const cached = this.cache.get(cacheKey);
      if (Date.now() - cached.timestamp < this.cacheTimeout) {
        return cached.data;
      }
    }

    try {
      const response = await fetch(
        `https://api.duckduckgo.com/?q=${encodeURIComponent(query)}&format=json&no_html=1&skip_disambig=1`
      );
      const data = await response.json();
      
      const results = {
        query: query,
        results: data.RelatedTopics?.map(topic => ({
          title: topic.Text?.split(' - ')[0] || '',
          snippet: topic.Text || '',
          url: topic.FirstURL || ''
        })).filter(r => r.url) || [],
        instant_answer: data.Answer || data.AbstractText || '',
        source: 'DuckDuckGo'
      };

      this.cache.set(cacheKey, { data: results, timestamp: Date.now() });
      return results;
    } catch (error) {
      console.error('DuckDuckGo search failed:', error);
      throw error;
    }
  }

  // 2. Bing Web Search API (Requires API Key)
  async bingSearch(query, apiKey) {
    if (!apiKey) {
      throw new Error('Bing API key required');
    }

    const cacheKey = `bing_${query}`;
    if (this.cache.has(cacheKey)) {
      const cached = this.cache.get(cacheKey);
      if (Date.now() - cached.timestamp < this.cacheTimeout) {
        return cached.data;
      }
    }

    try {
      const response = await fetch(
        `https://api.bing.microsoft.com/v7.0/search?q=${encodeURIComponent(query)}&count=10`,
        {
          headers: {
            'Ocp-Apim-Subscription-Key': apiKey
          }
        }
      );

      if (!response.ok) {
        throw new Error(`Bing API error: ${response.status}`);
      }

      const data = await response.json();
      
      const results = {
        query: query,
        results: data.webPages?.value?.map(page => ({
          title: page.name,
          snippet: page.snippet,
          url: page.url
        })) || [],
        total_results: data.webPages?.totalEstimatedMatches || 0,
        source: 'Bing'
      };

      this.cache.set(cacheKey, { data: results, timestamp: Date.now() });
      return results;
    } catch (error) {
      console.error('Bing search failed:', error);
      throw error;
    }
  }

  // 3. SerpAPI (Google Proxy - Requires API Key)
  async serpApiSearch(query, apiKey) {
    if (!apiKey) {
      throw new Error('SerpAPI key required');
    }

    const cacheKey = `serp_${query}`;
    if (this.cache.has(cacheKey)) {
      const cached = this.cache.get(cacheKey);
      if (Date.now() - cached.timestamp < this.cacheTimeout) {
        return cached.data;
      }
    }

    try {
      const response = await fetch(
        `https://serpapi.com/search.json?engine=google&q=${encodeURIComponent(query)}&api_key=${apiKey}`
      );

      if (!response.ok) {
        throw new Error(`SerpAPI error: ${response.status}`);
      }

      const data = await response.json();
      
      const results = {
        query: query,
        results: data.organic_results?.map(result => ({
          title: result.title,
          snippet: result.snippet,
          url: result.link
        })) || [],
        total_results: data.search_information?.total_results || 0,
        source: 'Google (via SerpAPI)'
      };

      this.cache.set(cacheKey, { data: results, timestamp: Date.now() });
      return results;
    } catch (error) {
      console.error('SerpAPI search failed:', error);
      throw error;
    }
  }

  // 4. News API Search
  async newsSearch(query, apiKey) {
    if (!apiKey) {
      throw new Error('News API key required');
    }

    try {
      const response = await fetch(
        `https://newsapi.org/v2/everything?q=${encodeURIComponent(query)}&sortBy=relevancy&pageSize=10&apiKey=${apiKey}`
      );

      if (!response.ok) {
        throw new Error(`News API error: ${response.status}`);
      }

      const data = await response.json();
      
      return {
        query: query,
        results: data.articles?.map(article => ({
          title: article.title,
          snippet: article.description,
          url: article.url,
          published: article.publishedAt,
          source_name: article.source.name
        })) || [],
        total_results: data.totalResults || 0,
        source: 'NewsAPI'
      };
    } catch (error) {
      console.error('News search failed:', error);
      throw error;
    }
  }

  // 5. Web Scraping with Puppeteer (Alternative Search Engines)
  async scrapeSearch(query, engine = 'duckduckgo') {
    const puppeteer = require('puppeteer');
    
    try {
      const browser = await puppeteer.launch({ 
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
      });
      const page = await browser.newPage();

      // Set user agent to avoid detection
      await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36');

      let searchUrl;
      let resultSelector;
      let titleSelector;
      let snippetSelector;
      let urlSelector;

      switch (engine) {
        case 'duckduckgo':
          searchUrl = `https://duckduckgo.com/?q=${encodeURIComponent(query)}`;
          resultSelector = '[data-result="result"]';
          titleSelector = 'h2 a';
          snippetSelector = '.result__snippet';
          urlSelector = 'h2 a';
          break;
        case 'startpage':
          searchUrl = `https://www.startpage.com/sp/search?query=${encodeURIComponent(query)}`;
          resultSelector = '.w-gl__result';
          titleSelector = '.w-gl__result-title';
          snippetSelector = '.w-gl__description';
          urlSelector = '.w-gl__result-title';
          break;
        case 'searx':
          searchUrl = `https://searx.org/search?q=${encodeURIComponent(query)}`;
          resultSelector = '.result';
          titleSelector = 'h3 a';
          snippetSelector = '.content';
          urlSelector = 'h3 a';
          break;
      }

      await page.goto(searchUrl, { waitUntil: 'networkidle2' });

      const results = await page.evaluate((selectors) => {
        const results = [];
        const resultElements = document.querySelectorAll(selectors.resultSelector);
        
        resultElements.forEach(element => {
          const titleElement = element.querySelector(selectors.titleSelector);
          const snippetElement = element.querySelector(selectors.snippetSelector);
          const urlElement = element.querySelector(selectors.urlSelector);

          if (titleElement && urlElement) {
            results.push({
              title: titleElement.textContent?.trim() || '',
              snippet: snippetElement?.textContent?.trim() || '',
              url: urlElement.href || urlElement.getAttribute('href') || ''
            });
          }
        });

        return results;
      }, { resultSelector, titleSelector, snippetSelector, urlSelector });

      await browser.close();

      return {
        query: query,
        results: results.filter(r => r.url && r.title),
        source: `${engine} (scraped)`
      };

    } catch (error) {
      console.error('Scraping search failed:', error);
      throw error;
    }
  }

  // 6. Multi-Source Aggregated Search
  async multiSearch(query, options = {}) {
    const {
      bingApiKey,
      serpApiKey,
      newsApiKey,
      includeScraping = false,
      sources = ['duckduckgo', 'bing', 'news']
    } = options;

    const searchPromises = [];

    // Add available sources
    if (sources.includes('duckduckgo')) {
      searchPromises.push(
        this.duckDuckGoSearch(query).catch(error => ({ error: error.message, source: 'duckduckgo' }))
      );
    }

    if (sources.includes('bing') && bingApiKey) {
      searchPromises.push(
        this.bingSearch(query, bingApiKey).catch(error => ({ error: error.message, source: 'bing' }))
      );
    }

    if (sources.includes('serp') && serpApiKey) {
      searchPromises.push(
        this.serpApiSearch(query, serpApiKey).catch(error => ({ error: error.message, source: 'serp' }))
      );
    }

    if (sources.includes('news') && newsApiKey) {
      searchPromises.push(
        this.newsSearch(query, newsApiKey).catch(error => ({ error: error.message, source: 'news' }))
      );
    }

    if (includeScraping) {
      searchPromises.push(
        this.scrapeSearch(query).catch(error => ({ error: error.message, source: 'scraping' }))
      );
    }

    const results = await Promise.all(searchPromises);
    
    // Combine and deduplicate results
    const combinedResults = [];
    const seenUrls = new Set();

    results.forEach(result => {
      if (result.error) {
        console.warn(`Search source failed: ${result.source} - ${result.error}`);
        return;
      }

      result.results?.forEach(item => {
        if (!seenUrls.has(item.url)) {
          seenUrls.add(item.url);
          combinedResults.push({
            ...item,
            source: result.source
          });
        }
      });
    });

    return {
      query: query,
      results: combinedResults,
      sources_used: results.filter(r => !r.error).map(r => r.source),
      sources_failed: results.filter(r => r.error).map(r => r.source),
      total_results: combinedResults.length
    };
  }

  // 7. Fallback Search with Retry Logic
  async searchWithFallback(query, options = {}) {
    const fallbackOrder = [
      () => this.duckDuckGoSearch(query),
      () => options.bingApiKey ? this.bingSearch(query, options.bingApiKey) : null,
      () => options.serpApiKey ? this.serpApiSearch(query, options.serpApiKey) : null,
      () => options.includeScraping ? this.scrapeSearch(query) : null
    ].filter(Boolean);

    for (const searchMethod of fallbackOrder) {
      try {
        const result = await searchMethod();
        if (result && result.results && result.results.length > 0) {
          return result;
        }
      } catch (error) {
        console.warn('Search method failed, trying next:', error.message);
        continue;
      }
    }

    throw new Error('All search methods failed');
  }
}

// Usage Examples
async function examples() {
  const searchService = new AlternativeSearchService();

  // Example 1: Simple DuckDuckGo search (free)
  try {
    const results = await searchService.duckDuckGoSearch('climate change solutions');
    console.log('DuckDuckGo Results:', results);
  } catch (error) {
    console.error('Search failed:', error);
  }

  // Example 2: Multi-source search
  try {
    const results = await searchService.multiSearch('renewable energy India', {
      bingApiKey: 'YOUR_BING_API_KEY', // Optional
      newsApiKey: 'YOUR_NEWS_API_KEY', // Optional
      sources: ['duckduckgo', 'bing', 'news']
    });
    console.log('Multi-source Results:', results);
  } catch (error) {
    console.error('Multi-search failed:', error);
  }

  // Example 3: Fallback search
  try {
    const results = await searchService.searchWithFallback('sustainable agriculture', {
      bingApiKey: 'YOUR_BING_API_KEY',
      includeScraping: true
    });
    console.log('Fallback Results:', results);
  } catch (error) {
    console.error('All searches failed:', error);
  }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = AlternativeSearchService;
}

// Browser usage
if (typeof window !== 'undefined') {
  window.AlternativeSearchService = AlternativeSearchService;
}
