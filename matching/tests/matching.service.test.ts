import { MatchingService } from '../src/services/matching.service';
import { ProductRepository } from '../src/repositories/product.repository';
import { Product } from '../src/models/product.model';

// Мокаем репозиторий
jest.mock('../src/repositories/product.repository');

const MockProductRepository = ProductRepository as jest.MockedClass<typeof ProductRepository>;

describe('MatchingService', () => {
  let service: MatchingService;
  let mockRepository: jest.Mocked<ProductRepository>;

  const mockProducts: Product[] = [
    { sku: 'APPL-IPH-14', description: 'Apple iPhone 14 Pro 128GB Deep Purple' },
    { sku: 'SAMS-GAL-S23', description: 'Samsung Galaxy S23 Ultra 256GB Phantom Black' },
    { sku: 'GOOG-PIX-7', description: 'Google Pixel 7 Pro 128GB Snow' }
  ];

  beforeEach(() => {
    mockRepository = new MockProductRepository() as jest.Mocked<ProductRepository>;
    mockRepository.getAllProducts.mockResolvedValue(mockProducts);
    service = new MatchingService(mockRepository);
    jest.clearAllMocks();
  });

  describe('findBestMatch', () => {
    test('должен находить точное совпадение', async () => {
      const result = await service.findBestMatch('Apple iPhone 14');
      
      expect(result).toEqual(mockProducts[0]);
      expect(mockRepository.getAllProducts).toHaveBeenCalled();
    });

    test('должен находить частичное совпадение', async () => {
      const result = await service.findBestMatch('Samsung Galaxy');
      
      expect(result).toEqual(mockProducts[1]);
    });

    test('должен возвращать null если совпадение ниже порога', async () => {
      const result = await service.findBestMatch('PlayStation', 90);
      
      expect(result).toBeNull();
    });

    test('должен работать с низким порогом', async () => {
      const result = await service.findBestMatch('iPhone', 30);
      
      expect(result).toEqual(mockProducts[0]);
    });

    test('должен обрабатывать ошибки репозитория', async () => {
      mockRepository.getAllProducts.mockRejectedValue(new Error('Repository error'));
      
      await expect(service.findBestMatch('iPhone')).rejects.toThrow('Repository error');
    });
/*
    test('должен возвращать null для пустого списка продуктов', async () => {
      mockRepository.getAllProducts.mockResolvedValue([]);
      
      const result = await service.findBestMatch('iPhone');
      expect(result).toBeNull();
    });
*/

    test('должен находить лучшее совпадение среди нескольких', async () => {
      const result = await service.findBestMatch('iPhone 14 Pro');
      
      // Должен найти iPhone, так как это наиболее точное совпадение
      expect(result).toEqual(mockProducts[0]);
    });
  });

  describe('findBestMatchWithScore', () => {
    test('должен находить продукт с score', async () => {
      const result = await service.findBestMatchWithScore('Apple iPhone 14');
      
      expect(result.product).toEqual(mockProducts[0]);
      expect(result.score).toBeGreaterThan(80);
      expect(mockRepository.getAllProducts).toHaveBeenCalled();
    });

    test('должен возвращать null продукт но показывать score', async () => {
      const result = await service.findBestMatchWithScore('PlayStation', 90);
      
      expect(result.product).toBeNull();
      expect(typeof result.score).toBe('number');
      expect(result.score).toBeGreaterThanOrEqual(0);
    });

    test('должен работать с низким порогом и возвращать score', async () => {
      const result = await service.findBestMatchWithScore('iPhone', 30);
      
      expect(result.product).toEqual(mockProducts[0]);
      expect(result.score).toBeGreaterThan(30);
    });

    test('должен обрабатывать ошибки репозитория в методе с score', async () => {
      mockRepository.getAllProducts.mockRejectedValue(new Error('Repository error'));
      
      await expect(service.findBestMatchWithScore('iPhone')).rejects.toThrow('Repository error');
    });
  });

  
});
