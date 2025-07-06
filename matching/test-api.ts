import { Request, Response } from 'express';
import { MatchingController } from './src/controllers/matching.controller';

// Простой тест для проверки API
async function testAPI() {
  const mockReq = {
    body: {
      query: 'iPhone 14',
      threshold: 80
    }
  } as Request;

  let responseData: any;
  const mockRes = {
    json: (data: any) => {
      responseData = data;
      console.log('Response:', JSON.stringify(data, null, 2));
    },
    status: (code: number) => ({
      json: (data: any) => {
        responseData = { status: code, ...data };
        console.log('Error Response:', JSON.stringify(responseData, null, 2));
      }
    })
  } as any as Response;

  try {
    await MatchingController.do(mockReq, mockRes);
    
    if (responseData) {
      console.log('✅ API тест прошел успешно');
      console.log('📊 Score:', responseData.score);
      console.log('🔍 Найден продукт:', responseData.found);
    }
  } catch (error) {
    console.error('❌ Ошибка в API тесте:', error);
  }
}

testAPI();
