import { ProductRepository } from '../src/repositories/product.repository';
import { Product } from '../src/models/product.model';
import * as fs from 'fs';

// Мокаем файловую систему для тестов
jest.mock('fs', () => ({
  promises: {
    readFile: jest.fn()
  }
}));

const mockFs = fs as jest.Mocked<typeof fs>;

describe('ProductRepository', () => {
  let repository: ProductRepository;

  beforeEach(() => {
    repository = new ProductRepository();
    jest.clearAllMocks();
  });

  describe('getAllProducts', () => {
    test('должен загружать и парсить TSV файл', async () => {
      const mockTsvContent = 'sku\tdescription\nAPPL-IPH-14\tApple iPhone 14\nSAMS-GAL-S23\tSamsung Galaxy S23';
      (mockFs.promises.readFile as jest.Mock).mockResolvedValue(mockTsvContent);

      const products = await repository.getAllProducts();

      expect(products).toEqual([
        { sku: 'APPL-IPH-14', description: 'Apple iPhone 14' },
        { sku: 'SAMS-GAL-S23', description: 'Samsung Galaxy S23' }
      ]);
      expect(mockFs.promises.readFile).toHaveBeenCalledWith(
        expect.stringContaining('products.tsv'),
        'utf-8'
      );
    });

    test('должен обрабатывать пустой TSV файл', async () => {
      const mockTsvContent = 'sku\tdescription\n';
      (mockFs.promises.readFile as jest.Mock).mockResolvedValue(mockTsvContent);

      const products = await repository.getAllProducts();
      expect(products).toEqual([]);
    });

    test('должен игнорировать пустые строки', async () => {
      const mockTsvContent = 'sku\tdescription\nAPPL-IPH-14\tApple iPhone 14\n\nSAMS-GAL-S23\tSamsung Galaxy S23\n';
      (mockFs.promises.readFile as jest.Mock).mockResolvedValue(mockTsvContent);

      const products = await repository.getAllProducts();
      expect(products).toHaveLength(2);
    });

    test('должен выбрасывать ошибку при неверном формате TSV', async () => {
      const mockTsvContent = 'sku\tdescription\nAPPL-IPH-14\nSAMS-GAL-S23\tSamsung Galaxy S23';
      (mockFs.promises.readFile as jest.Mock).mockResolvedValue(mockTsvContent);

      await expect(repository.getAllProducts()).rejects.toThrow('Неверный формат строки в TSV');
    });

    test('должен обрабатывать ошибки чтения файла', async () => {
      (mockFs.promises.readFile as jest.Mock).mockRejectedValue(new Error('File not found'));

      await expect(repository.getAllProducts()).rejects.toThrow('Не удалось загрузить данные продуктов');
    });
  });

  describe('findProductsByQuery', () => {
    const mockProducts = [
      { sku: 'APPL-IPH-14', description: 'Apple iPhone 14 Pro' },
      { sku: 'SAMS-GAL-S23', description: 'Samsung Galaxy S23 Ultra' },
      { sku: 'GOOG-PIX-7', description: 'Google Pixel 7 Pro' }
    ];

    beforeEach(() => {
      const mockTsvContent = 'sku\tdescription\nAPPL-IPH-14\tApple iPhone 14 Pro\nSAMS-GAL-S23\tSamsung Galaxy S23 Ultra\nGOOG-PIX-7\tGoogle Pixel 7 Pro';
      (mockFs.promises.readFile as jest.Mock).mockResolvedValue(mockTsvContent);
    });

    test('должен находить продукты по SKU', async () => {
      const products = await repository.findProductsByQuery('APPL');
      expect(products).toEqual([mockProducts[0]]);
    });

    test('должен находить продукты по описанию', async () => {
      const products = await repository.findProductsByQuery('iPhone');
      expect(products).toEqual([mockProducts[0]]);
    });

    test('должен быть нечувствительным к регистру', async () => {
      const products = await repository.findProductsByQuery('apple');
      expect(products).toEqual([mockProducts[0]]);
    });

    test('должен возвращать все продукты при пустом запросе', async () => {
      const products = await repository.findProductsByQuery('');
      expect(products).toEqual(mockProducts);
    });

    test('должен возвращать пустой массив если ничего не найдено', async () => {
      const products = await repository.findProductsByQuery('PlayStation');
      expect(products).toEqual([]);
    });

    test('должен находить несколько продуктов', async () => {
      const products = await repository.findProductsByQuery('Pro');
      expect(products).toHaveLength(2); // Все три продукта содержат "Pro"
    });
  });
});
