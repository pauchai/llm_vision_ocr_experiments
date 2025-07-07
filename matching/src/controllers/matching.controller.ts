import { Request, Response } from 'express';
import { MatchingService } from '../services/matching.service';

/**
 * @swagger
 * tags:
 *   name: Product Matching
 *   description: API для поиска и сопоставления продуктов
 */

export class MatchingController {
  /**
   * Выполняет поиск продукта по заданному запросу
   * 
   * @param req - Express запрос с телом, содержащим query и optional threshold
   * @param res - Express ответ с результатом поиска
   */
  static async do(req: Request, res: Response): Promise<void> {
    try {
      const { query, threshold } = req.body;
      
      if (!query || typeof query !== 'string') {
        res.status(400).json({ 
          error: 'Параметр query обязателен и должен быть строкой' 
        });
        return;
      }

      const matchingService = new MatchingService();
      const result = await matchingService.findBestMatchWithScore(query, threshold);
      
      res.json({ 
        query,
        result: result.product,
        score: result.score,
        found: !!result.product
      });
    } catch (error) {
      console.error('Ошибка в MatchingController:', error);
      res.status(500).json({ 
        error: 'Внутренняя ошибка сервера' 
      });
    }
  }

  /**
   * Возвращает список всех продуктов
   */
  static async getAllProducts(req: Request, res: Response): Promise<void> {
    try {
      const matchingService = new MatchingService();
      const products = await matchingService.getAllProducts();
      
      res.json({
        products,
        total: products.length
      });
    } catch (error) {
      console.error('Ошибка в MatchingController.getAllProducts:', error);
      res.status(500).json({
        error: 'Внутренняя ошибка сервера'
      });
    }
  }
}
