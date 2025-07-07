import { Router } from 'express';
import { MatchingController } from '../controllers/matching.controller';

export const matchingRouter = Router();

/**
 * @swagger
 * /api/matching:
 *   post:
 *     summary: Поиск продукта по запросу
 *     description: Находит наиболее подходящий продукт используя алгоритм нечеткого поиска
 *     tags: [Product Matching]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             $ref: '#/components/schemas/MatchingRequest'
 *           examples:
 *             example1:
 *               summary: Поиск iPhone
 *               value:
 *                 query: "iPhone 14"
 *                 threshold: 80
 *             example2:
 *               summary: Поиск Samsung с низким порогом
 *               value:
 *                 query: "Samsung"
 *                 threshold: 60
 *             example3:
 *               summary: Поиск с высоким порогом
 *               value:
 *                 query: "Apple MacBook Pro"
 *                 threshold: 90
 *     responses:
 *       200:
 *         description: Успешный поиск
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/MatchingResponse'
 *             examples:
 *               found:
 *                 summary: Продукт найден
 *                 value:
 *                   query: "iPhone 14"
 *                   result:
 *                     sku: "APPL-IPH-14"
 *                     description: "Apple iPhone 14 Pro 128GB Deep Purple"
 *                   score: 95.5
 *                   found: true
 *               not_found:
 *                 summary: Продукт не найден
 *                 value:
 *                   query: "PlayStation 5"
 *                   result: null
 *                   score: 25.3
 *                   found: false
 *       400:
 *         description: Неверный запрос
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/ErrorResponse'
 *             examples:
 *               missing_query:
 *                 summary: Отсутствует параметр query
 *                 value:
 *                   error: "Параметр query обязателен и должен быть строкой"
 *               invalid_query_type:
 *                 summary: Неверный тип параметра query
 *                 value:
 *                   error: "Параметр query обязателен и должен быть строкой"
 *       500:
 *         description: Внутренняя ошибка сервера
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/ErrorResponse'
 *             example:
 *               error: "Внутренняя ошибка сервера"
 */
matchingRouter.post('/', MatchingController.do);

/**
 * @swagger
 * /api/matching/products:
 *   get:
 *     summary: Получить список всех продуктов
 *     description: Возвращает полный список продуктов из базы данных
 *     tags: [Product Matching]
 *     responses:
 *       200:
 *         description: Список продуктов
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 products:
 *                   type: array
 *                   items:
 *                     $ref: '#/components/schemas/Product'
 *                 total:
 *                   type: number
 *                   description: Общее количество продуктов
 *             example:
 *               products:
 *                 - sku: "APPL-IPH-14"
 *                   description: "Apple iPhone 14 Pro 128GB Deep Purple"
 *                 - sku: "SAMS-GAL-S23"
 *                   description: "Samsung Galaxy S23 Ultra 256GB Phantom Black"
 *               total: 32
 *       500:
 *         description: Внутренняя ошибка сервера
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/ErrorResponse'
 */
matchingRouter.get('/products', MatchingController.getAllProducts);
