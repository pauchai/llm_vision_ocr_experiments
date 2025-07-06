import { ProductRepository } from './src/repositories/product.repository';

async function testTsvLoading() {
  try {
    console.log('🧪 Тестируем загрузку TSV файла...');
    
    const repository = new ProductRepository();
    const products = await repository.getAllProducts();
    
    console.log(`✅ Успешно загружено продуктов: ${products.length}`);
    console.log('\n📦 Первые 5 продуктов:');
    products.slice(0, 5).forEach((product, index) => {
      console.log(`${index + 1}. SKU: ${product.sku} | Описание: ${product.description}`);
    });
    
    // Тестируем поиск
    console.log('\n🔍 Тестируем поиск по запросу "iPhone":');
    const searchResults = await repository.findProductsByQuery('iPhone');
    console.log(`Найдено продуктов: ${searchResults.length}`);
    searchResults.forEach((product, index) => {
      console.log(`${index + 1}. SKU: ${product.sku} | Описание: ${product.description}`);
    });
    
  } catch (error) {
    console.error('❌ Ошибка при тестировании TSV:', error);
    if (error instanceof Error) {
      console.error('Stack trace:', error.stack);
    }
  }
}

testTsvLoading();
