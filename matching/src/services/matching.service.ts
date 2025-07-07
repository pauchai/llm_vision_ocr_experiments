import { FuzzyMatcher, MatchResult } from '../utils/matcher';
import { ProductRepository } from '../repositories/product.repository';
import { Product } from '../models/product.model';

export interface ProductMatch {
  product: Product | null;
  score: number;
}

export class MatchingService {
  private productRepository: ProductRepository;

  constructor(productRepository?: ProductRepository) {
    this.productRepository = productRepository || new ProductRepository();
  }

  async findBestMatch(
    query: string,
    threshold: number = 80
  ): Promise<Product | null> {
    const products = await this.productRepository.getAllProducts();
    
    // Создаем массив описаний для поиска
    const descriptions = products.map(product => product.description);
    
    // Находим лучшее совпадение по описанию
    const bestMatchDescription = FuzzyMatcher.match(query, descriptions, threshold);
    
    if (!bestMatchDescription) {
      return null;
    }

    // Находим продукт с соответствующим описанием
    return products.find(product => product.description === bestMatchDescription) || null;
  }

  async findBestMatchWithScore(
    query: string,
    threshold: number = 80
  ): Promise<ProductMatch> {
    const products = await this.productRepository.getAllProducts();
    
    // Создаем массив описаний для поиска
    const descriptions = products.map(product => product.description);
    
    // Находим лучшее совпадение по описанию с score
    const matchResult: MatchResult = FuzzyMatcher.matchWithScore(query, descriptions, threshold);
    
    if (!matchResult.match) {
      return {
        product: null,
        score: matchResult.score
      };
    }

    // Находим продукт с соответствующим описанием
    const product = products.find(product => product.description === matchResult.match) || null;
    
    return {
      product,
      score: matchResult.score
    };
  }

  async getAllProducts(): Promise<Product[]> {
    return await this.productRepository.getAllProducts();
  }
}
