import { Request, Response } from 'express';
import { MatchingController } from '../src/controllers/matching.controller';
import { MatchingService } from '../src/services/matching.service';
import { Product } from '../src/models/product.model';

// Мокаем сервис
jest.mock('../src/services/matching.service');

const MockMatchingService = MatchingService as jest.MockedClass<typeof MatchingService>;

describe('MatchingController', () => {
  let mockReq: Partial<Request>;
  let mockRes: Partial<Response>;
  let mockService: jest.Mocked<MatchingService>;

  const mockProduct: Product = {
    sku: 'APPL-IPH-14',
    description: 'Apple iPhone 14 Pro 128GB Deep Purple'
  };

  beforeEach(() => {
    mockReq = {
      body: {}
    };
    mockRes = {
      json: jest.fn().mockReturnThis(),
      status: jest.fn().mockReturnThis()
    };
    
    mockService = new MockMatchingService() as jest.Mocked<MatchingService>;
    MockMatchingService.mockImplementation(() => mockService);
    
    jest.clearAllMocks();
  });

  describe('do', () => {
    test('должен возвращать продукт при успешном поиске', async () => {
      mockReq.body = { query: 'iPhone', threshold: 80 };
      mockService.findBestMatch.mockResolvedValue(mockProduct);

      await MatchingController.do(mockReq as Request, mockRes as Response);

      expect(mockService.findBestMatch).toHaveBeenCalledWith('iPhone', 80);
      expect(mockRes.json).toHaveBeenCalledWith({
        query: 'iPhone',
        result: mockProduct,
        found: true
      });
    });

    test('должен возвращать null при отсутствии совпадений', async () => {
      mockReq.body = { query: 'PlayStation' };
      mockService.findBestMatch.mockResolvedValue(null);

      await MatchingController.do(mockReq as Request, mockRes as Response);

      expect(mockService.findBestMatch).toHaveBeenCalledWith('PlayStation', undefined);
      expect(mockRes.json).toHaveBeenCalledWith({
        query: 'PlayStation',
        result: null,
        found: false
      });
    });

    test('должен возвращать ошибку 400 при отсутствии query', async () => {
      mockReq.body = { threshold: 80 };

      await MatchingController.do(mockReq as Request, mockRes as Response);

      expect(mockRes.status).toHaveBeenCalledWith(400);
      expect(mockRes.json).toHaveBeenCalledWith({
        error: 'Параметр query обязателен и должен быть строкой'
      });
      expect(mockService.findBestMatch).not.toHaveBeenCalled();
    });

    test('должен возвращать ошибку 400 при неверном типе query', async () => {
      mockReq.body = { query: 123 };

      await MatchingController.do(mockReq as Request, mockRes as Response);

      expect(mockRes.status).toHaveBeenCalledWith(400);
      expect(mockRes.json).toHaveBeenCalledWith({
        error: 'Параметр query обязателен и должен быть строкой'
      });
    });

    test('должен обрабатывать ошибки сервиса', async () => {
      mockReq.body = { query: 'iPhone' };
      mockService.findBestMatch.mockRejectedValue(new Error('Service error'));

      const consoleSpy = jest.spyOn(console, 'error').mockImplementation();

      await MatchingController.do(mockReq as Request, mockRes as Response);

      expect(mockRes.status).toHaveBeenCalledWith(500);
      expect(mockRes.json).toHaveBeenCalledWith({
        error: 'Внутренняя ошибка сервера'
      });
      expect(consoleSpy).toHaveBeenCalledWith('Ошибка в MatchingController:', expect.any(Error));

      consoleSpy.mockRestore();
    });

    test('должен использовать threshold по умолчанию', async () => {
      mockReq.body = { query: 'iPhone' };
      mockService.findBestMatch.mockResolvedValue(mockProduct);

      await MatchingController.do(mockReq as Request, mockRes as Response);

      expect(mockService.findBestMatch).toHaveBeenCalledWith('iPhone', undefined);
    });

    test('должен передавать кастомный threshold', async () => {
      mockReq.body = { query: 'iPhone', threshold: 90 };
      mockService.findBestMatch.mockResolvedValue(mockProduct);

      await MatchingController.do(mockReq as Request, mockRes as Response);

      expect(mockService.findBestMatch).toHaveBeenCalledWith('iPhone', 90);
    });
  });
});
