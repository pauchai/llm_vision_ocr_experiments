import { Request, Response } from 'express';
import { ExampleService } from '../services/example.service';

export class ExampleController {
  static async getAll(req: Request, res: Response) {
    const data = await ExampleService.getAll();
    res.json(data);
  }

  static async create(req: Request, res: Response) {
    const newItem = await ExampleService.create(req.body);
    res.status(201).json(newItem);
  }
}
