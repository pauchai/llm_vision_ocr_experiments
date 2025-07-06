import express from 'express';
import { json } from 'body-parser';
import { exampleRouter } from './routes/example.route';
import { matchingRouter } from './routes/matching.route';

export const app = express();

app.use(json());
app.use('/api/example', exampleRouter);
app.use('/api/matching', matchingRouter);

