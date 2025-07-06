import { Product } from '../models/product.model';
import * as fs from 'fs';
import * as path from 'path';

export interface IProductRepository {
  getAllProducts(): Promise<Product[]>;
  findProductsByQuery(query: string): Promise<Product[]>;
}

export class ProductRepository implements IProductRepository {
  private tsvPath: string;

  constructor(tsvPath?: string) {
    this.tsvPath = tsvPath || '/data/products.tsv';
  }

  async getAllProducts(): Promise<Product[]> {
    try {
      const tsvContent = await fs.promises.readFile(this.tsvPath, 'utf-8');
      return this.parseTsvContent(tsvContent);
    } catch (error) {
      console.error('Ошибка при чтении TSV файла:', error);
      throw new Error('Не удалось загрузить данные продуктов');
    }
  }

  async findProductsByQuery(query: string): Promise<Product[]> {
    const allProducts = await this.getAllProducts();
    
    if (!query || query.trim() === '') {
      return allProducts;
    }

    const queryLower = query.toLowerCase();
    return allProducts.filter(product => 
      product.sku.toLowerCase().includes(queryLower) ||
      product.description.toLowerCase().includes(queryLower)
    );
  }

  private parseTsvContent(tsvContent: string): Product[] {
    const lines = tsvContent.split('\n').filter(line => line.trim() !== '');
    
    if (lines.length === 0) {
      return [];
    }

    // Пропускаем заголовок (первую строку)
    const dataLines = lines.slice(1);
    
    return dataLines.map(line => {
      const [sku, description] = line.split('\t').map(field => field.trim());
      
      if (!sku || !description) {
        throw new Error(`Неверный формат строки в TSV: ${line}`);
      }

      return { sku, description };
    });
  }
}
