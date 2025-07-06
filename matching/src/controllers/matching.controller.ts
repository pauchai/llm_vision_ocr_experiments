import { Request, Response } from 'express';
import { MatchingService } from '../services/matching.service';

export class MatchingController {
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
}
