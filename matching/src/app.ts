import express from 'express';
import { json } from 'body-parser';
import { exampleRouter } from './routes/example.route';
import { matchingRouter } from './routes/matching.route';
import { setupSwagger } from './config/swagger';

export const app = express();

app.use(json());

// Настройка Swagger документации
setupSwagger(app);

// Роуты API
app.use('/api/example', exampleRouter);
app.use('/api/matching', matchingRouter);

// Корневой роут с информацией об API
app.get('/', (req, res) => {
  res.json({
    message: 'Product Matching API',
    version: '1.0.0',
    documentation: '/api-docs',
    endpoints: {
      matching: '/api/matching',
      swagger_json: '/api-docs.json'
    }
  });
});

