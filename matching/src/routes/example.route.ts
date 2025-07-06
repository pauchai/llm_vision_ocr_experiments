import { Router } from 'express';
import { ExampleController } from '../controllers/example.controller';

export const exampleRouter = Router();

exampleRouter.get('/', ExampleController.getAll);
exampleRouter.post('/', ExampleController.create);
