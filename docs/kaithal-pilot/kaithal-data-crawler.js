// Kaithal Real Players Data Crawler
// Multi-lens parallel search implementation

const AlternativeSearchService = require('./search-implementation-example.js');
const fs = require('fs').promises;

class KaithalPlayersCrawler {
  constructor() {
    this.searchService = new AlternativeSearchService();
    this.results = {
      economic_networks: [],
      digital_footprints: [],
      regulatory_networks: [],
      infrastructure_services: [],
      resource_flows: []
    };
    this.discovered_players = new Map();
  }

  // Lens 1: Economic Transaction Networks
  async crawlEconomicNetworks() {
    console.log('🏦 Starting Economic Networks Crawl...');
    
    const economicQueries = [
      // Banking & Financial
      "Kaithal bank branches customer base",
      "microfinance Kaithal SHG loans",
      "cooperative banks Haryana Kaithal",
      "insurance agents Kaithal district",
      
      // Market & Trade
      "Kaithal mandi traders commission agents",
      "transport operators Kaithal goods movement",
      "wholesale markets Kaithal supply chain",
      "courier services Kaithal delivery network",
      "money transfer agents Kaithal"
    ];

    for (const query of economicQueries) {
      try {
        console.log(`Searching: ${query}`);
        const result = await this.searchService.searchWithFallback(query);
        this.results.economic_networks.push({
          query,
          results: result.results,
          source: result.source,
          timestamp: new Date().toISOString()
        });
        
        // Extract potential players
        this.extractPlayersFromResults(result.results, 'economic');
        
        // Rate limiting
        await this.delay(2000);
      } catch (error) {
        console.error(`Failed to search: ${query}`, error.message);
      }
    }
  }

  // Lens 2: Digital Footprint Analysis
  async crawlDigitalFootprints() {
    console.log('💻 Starting Digital Footprints Crawl...');
    
    const digitalQueries = [
      // Social Media
      'site:facebook.com "Kaithal organization"',
      'site:facebook.com "Kaithal business"',
      'site:linkedin.com "Kaithal professional"',
      'site:youtube.com "Kaithal local"',
      
      // Business Listings
      "Kaithal business directory online",
      "Google My Business Kaithal",
      "Kaithal sellers amazon flipkart",
      "digital payment merchants Kaithal",
      "app based services Kaithal delivery"
    ];

    for (const query of digitalQueries) {
      try {
        console.log(`Searching: ${query}`);
        const result = await this.searchService.searchWithFallback(query);
        this.results.digital_footprints.push({
          query,
          results: result.results,
          source: result.source,
          timestamp: new Date().toISOString()
        });
        
        this.extractPlayersFromResults(result.results, 'digital');
        await this.delay(2000);
      } catch (error) {
        console.error(`Failed to search: ${query}`, error.message);
      }
    }
  }

  // Lens 3: Regulatory & Compliance Networks
  async crawlRegulatoryNetworks() {
    console.log('📋 Starting Regulatory Networks Crawl...');
    
    const regulatoryQueries = [
      // Government Registrations
      "NGO registration Kaithal 12A 80G",
      "company registration Kaithal ROC",
      "cooperative society Kaithal registration",
      "professional associations Kaithal",
      
      // Licenses & Permits
      "trade license Kaithal business permit",
      "professional licenses Kaithal doctors lawyers",
      "educational institutions Kaithal affiliation",
      "industrial units Kaithal license",
      "organic certification Kaithal farmers"
    ];

    for (const query of regulatoryQueries) {
      try {
        console.log(`Searching: ${query}`);
        const result = await this.searchService.searchWithFallback(query);
        this.results.regulatory_networks.push({
          query,
          results: result.results,
          source: result.source,
          timestamp: new Date().toISOString()
        });
        
        this.extractPlayersFromResults(result.results, 'regulatory');
        await this.delay(2000);
      } catch (error) {
        console.error(`Failed to search: ${query}`, error.message);
      }
    }
  }

  // Lens 4: Infrastructure & Service Networks
  async crawlInfrastructureServices() {
    console.log('🏥 Starting Infrastructure Services Crawl...');
    
    const infrastructureQueries = [
      // Healthcare
      "hospitals Kaithal healthcare facilities",
      "medical stores Kaithal pharmacy network",
      "diagnostic centers Kaithal pathology labs",
      
      // Education
      "schools Kaithal education network",
      "coaching centers Kaithal skill training",
      "libraries Kaithal study centers",
      "sports clubs Kaithal facilities"
    ];

    for (const query of infrastructureQueries) {
      try {
        console.log(`Searching: ${query}`);
        const result = await this.searchService.searchWithFallback(query);
        this.results.infrastructure_services.push({
          query,
          results: result.results,
          source: result.source,
          timestamp: new Date().toISOString()
        });
        
        this.extractPlayersFromResults(result.results, 'infrastructure');
        await this.delay(2000);
      } catch (error) {
        console.error(`Failed to search: ${query}`, error.message);
      }
    }
  }

  // Lens 5: Resource Flow Analysis
  async crawlResourceFlows() {
    console.log('🚛 Starting Resource Flows Crawl...');
    
    const resourceQueries = [
      // Supply Chains
      "agricultural inputs Kaithal dealer network",
      "construction materials Kaithal suppliers",
      "fuel stations Kaithal distribution",
      
      // Information Flows
      "local news Kaithal media outlets",
      "cable TV Kaithal operators",
      "internet service providers Kaithal",
      "printing press Kaithal publications"
    ];

    for (const query of resourceQueries) {
      try {
        console.log(`Searching: ${query}`);
        const result = await this.searchService.searchWithFallback(query);
        this.results.resource_flows.push({
          query,
          results: result.results,
          source: result.source,
          timestamp: new Date().toISOString()
        });
        
        this.extractPlayersFromResults(result.results, 'resource');
        await this.delay(2000);
      } catch (error) {
        console.error(`Failed to search: ${query}`, error.message);
      }
    }
  }

  // Extract potential players from search results
  extractPlayersFromResults(results, category) {
    results.forEach(result => {
      const player = this.parsePlayerFromResult(result, category);
      if (player) {
        const key = `${player.name}_${player.location}`;
        if (this.discovered_players.has(key)) {
          // Merge information
          const existing = this.discovered_players.get(key);
          existing.categories.add(category);
          existing.sources.push(result.url);
          existing.mentions++;
        } else {
          // New player
          player.categories = new Set([category]);
          player.sources = [result.url];
          player.mentions = 1;
          this.discovered_players.set(key, player);
        }
      }
    });
  }

  // Parse player information from search result
  parsePlayerFromResult(result, category) {
    const title = result.title.toLowerCase();
    const snippet = result.snippet.toLowerCase();
    const url = result.url;

    // Extract organization names, phone numbers, addresses
    const orgPatterns = [
      /([A-Z][a-z]+ (?:bank|hospital|school|college|cooperative|society|association|company|ltd|pvt))/gi,
      /([A-Z][a-z]+ (?:traders|suppliers|dealers|agents|services))/gi
    ];

    const phonePattern = /(\+91[\s-]?)?[6-9]\d{9}/g;
    const emailPattern = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g;

    let player = null;
    
    for (const pattern of orgPatterns) {
      const matches = title.match(pattern) || snippet.match(pattern);
      if (matches) {
        player = {
          name: matches[0].trim(),
          type: this.categorizeOrganization(matches[0], category),
          location: this.extractLocation(snippet),
          contact: {
            phones: snippet.match(phonePattern) || [],
            emails: snippet.match(emailPattern) || [],
            website: url
          },
          activities: this.extractActivities(snippet, category),
          discovered_via: category
        };
        break;
      }
    }

    return player;
  }

  // Categorize organization type
  categorizeOrganization(name, category) {
    const lowerName = name.toLowerCase();
    
    if (lowerName.includes('bank') || lowerName.includes('financial')) return 'Financial';
    if (lowerName.includes('hospital') || lowerName.includes('clinic')) return 'Healthcare';
    if (lowerName.includes('school') || lowerName.includes('college')) return 'Education';
    if (lowerName.includes('cooperative') || lowerName.includes('society')) return 'Cooperative';
    if (lowerName.includes('company') || lowerName.includes('ltd')) return 'Business';
    if (lowerName.includes('ngo') || lowerName.includes('trust')) return 'NGO';
    
    return category;
  }

  // Extract location information
  extractLocation(text) {
    const locationPatterns = [
      /kaithal/gi,
      /(siwan|guhla|kalayat|pundri|rajaund)/gi,
      /haryana/gi
    ];

    for (const pattern of locationPatterns) {
      const match = text.match(pattern);
      if (match) return match[0];
    }
    
    return 'Kaithal';
  }

  // Extract activities
  extractActivities(text, category) {
    const activityKeywords = {
      economic: ['banking', 'trading', 'finance', 'loan', 'insurance'],
      digital: ['website', 'online', 'digital', 'app', 'e-commerce'],
      regulatory: ['registration', 'license', 'permit', 'certification'],
      infrastructure: ['healthcare', 'education', 'training', 'facility'],
      resource: ['supply', 'distribution', 'transport', 'media']
    };

    const activities = [];
    const keywords = activityKeywords[category] || [];
    
    keywords.forEach(keyword => {
      if (text.toLowerCase().includes(keyword)) {
        activities.push(keyword);
      }
    });

    return activities;
  }

  // Delay function for rate limiting
  delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  // Run all crawling operations
  async crawlAll() {
    console.log('🚀 Starting Kaithal Players Discovery Crawl...');
    const startTime = Date.now();

    try {
      await this.crawlEconomicNetworks();
      await this.crawlDigitalFootprints();
      await this.crawlRegulatoryNetworks();
      await this.crawlInfrastructureServices();
      await this.crawlResourceFlows();

      const endTime = Date.now();
      console.log(`✅ Crawl completed in ${(endTime - startTime) / 1000} seconds`);
      
      await this.saveResults();
      await this.generateReport();
      
    } catch (error) {
      console.error('❌ Crawl failed:', error);
    }
  }

  // Save results to files
  async saveResults() {
    try {
      // Save raw search results
      await fs.writeFile(
        'kaithal-raw-search-results.json',
        JSON.stringify(this.results, null, 2)
      );

      // Save discovered players
      const playersArray = Array.from(this.discovered_players.entries()).map(([key, player]) => ({
        id: key,
        ...player,
        categories: Array.from(player.categories)
      }));

      await fs.writeFile(
        'kaithal-discovered-players.json',
        JSON.stringify(playersArray, null, 2)
      );

      console.log('💾 Results saved to files');
    } catch (error) {
      console.error('Failed to save results:', error);
    }
  }

  // Generate summary report
  async generateReport() {
    const totalPlayers = this.discovered_players.size;
    const categoryStats = {};
    const locationStats = {};

    this.discovered_players.forEach(player => {
      // Category statistics
      player.categories.forEach(category => {
        categoryStats[category] = (categoryStats[category] || 0) + 1;
      });

      // Location statistics
      locationStats[player.location] = (locationStats[player.location] || 0) + 1;
    });

    const report = {
      summary: {
        total_players_discovered: totalPlayers,
        crawl_timestamp: new Date().toISOString(),
        total_searches_performed: Object.values(this.results).reduce((sum, arr) => sum + arr.length, 0)
      },
      category_breakdown: categoryStats,
      location_breakdown: locationStats,
      top_players: Array.from(this.discovered_players.values())
        .sort((a, b) => b.mentions - a.mentions)
        .slice(0, 20)
        .map(player => ({
          name: player.name,
          type: player.type,
          location: player.location,
          mentions: player.mentions,
          categories: Array.from(player.categories)
        }))
    };

    await fs.writeFile(
      'kaithal-discovery-report.json',
      JSON.stringify(report, null, 2)
    );

    console.log('📊 Discovery Report Generated:');
    console.log(`Total Players Found: ${totalPlayers}`);
    console.log('Category Breakdown:', categoryStats);
    console.log('Location Breakdown:', locationStats);
  }
}

// Execute the crawler
async function main() {
  const crawler = new KaithalPlayersCrawler();
  await crawler.crawlAll();
}

// Run if called directly
if (require.main === module) {
  main().catch(console.error);
}

module.exports = KaithalPlayersCrawler;
