import swaggerJsdoc from 'swagger-jsdoc';
import swaggerUi from 'swagger-ui-express';
import { Express } from 'express';

const options = {
  definition: {
    openapi: '3.0.0',
    info: {
      title: 'Product Matching API',
      version: '1.0.0',
      description: 'API для поиска и сопоставления продуктов с использованием нечеткого поиска',
      contact: {
        name: 'API Support',
        email: 'support@example.com'
      }
    },
    servers: [
      {
        url: 'http://localhost:3000',
        description: 'Development server'
      }
    ],
    components: {
      schemas: {
        Product: {
          type: 'object',
          required: ['sku', 'description'],
          properties: {
            sku: {
              type: 'string',
              description: 'Уникальный код продукта',
              example: 'APPL-IPH-14'
            },
            description: {
              type: 'string',
              description: 'Описание продукта',
              example: 'Apple iPhone 14 Pro 128GB Deep Purple'
            }
          }
        },
        MatchingRequest: {
          type: 'object',
          required: ['query'],
          properties: {
            query: {
              type: 'string',
              description: 'Поисковый запрос для нахождения продукта',
              example: 'iPhone 14'
            },
            threshold: {
              type: 'number',
              minimum: 0,
              maximum: 100,
              default: 80,
              description: 'Порог совпадения (0-100). Чем выше значение, тем точнее должно быть совпадение',
              example: 80
            }
          }
        },
        MatchingResponse: {
          type: 'object',
          properties: {
            query: {
              type: 'string',
              description: 'Исходный поисковый запрос',
              example: 'iPhone 14'
            },
            result: {
              oneOf: [
                { $ref: '#/components/schemas/Product' },
                { type: 'null' }
              ],
              description: 'Найденный продукт или null если ничего не найдено'
            },
            score: {
              type: 'number',
              minimum: 0,
              maximum: 100,
              description: 'Оценка качества совпадения (0-100)',
              example: 95.5
            },
            found: {
              type: 'boolean',
              description: 'Указывает, был ли найден подходящий продукт',
              example: true
            }
          }
        },
        ErrorResponse: {
          type: 'object',
          properties: {
            error: {
              type: 'string',
              description: 'Описание ошибки',
              example: 'Параметр query обязателен и должен быть строкой'
            }
          }
        }
      }
    }
  },
  apis: ['./src/routes/*.ts', './src/controllers/*.ts'], // Пути к файлам с JSDoc комментариями
};

const specs = swaggerJsdoc(options);

export function setupSwagger(app: Express): void {
  app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(specs, {
    explorer: true,
    customCss: '.swagger-ui .topbar { display: none }',
    customSiteTitle: 'Product Matching API Documentation'
  }));
  
  // Эндпоинт для получения JSON спецификации
  app.get('/api-docs.json', (req, res) => {
    res.setHeader('Content-Type', 'application/json');
    res.send(specs);
  });
}

export { specs };
