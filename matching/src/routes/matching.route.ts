import { Router } from 'express';
import { MatchingController } from '../controllers/matching.controller';

export const matchingRouter = Router();

matchingRouter.post('/', MatchingController.do);
