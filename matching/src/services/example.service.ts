export class ExampleService {
  static async getAll() {
    // Здесь может быть доступ к базе данных или логика
    return [{ id: 1, name: 'Example' }];
  }

  static async create(data: any) {
    return { id: 2, ...data };
  }
}
