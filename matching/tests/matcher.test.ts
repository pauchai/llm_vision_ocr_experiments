import { FuzzyMatcher } from '../src/utils/matcher';

describe('FuzzyMatcher', () => {
  describe('match', () => {
    const candidates = ['apple', 'banana', 'orange', 'grape', 'pineapple'];

    test('должен найти точное совпадение', () => {
      const result = FuzzyMatcher.match('banana', candidates);
      expect(result).toBe('banana');
    });

    test('должен найти частичное совпадение', () => {
      const result = FuzzyMatcher.match('bana', candidates);
      expect(result).toBe('banana');
    });

    test('должен найти совпадение с опечаткой', () => {
      const result = FuzzyMatcher.match('bannana', candidates);
      expect(result).toBe('banana');
    });

    test('должен найти совпадение независимо от регистра', () => {
      const result = FuzzyMatcher.match('APPLE', candidates);
      expect(result).toBe('apple');
    });

    test('должен вернуть null если совпадение ниже порога', () => {
      const result = FuzzyMatcher.match('xyz', candidates, 70);
      expect(result).toBeNull();
    });

    test('должен работать с низким порогом', () => {
      const result = FuzzyMatcher.match('app', candidates, 30);
      expect(result).toBe('apple');
    });
/*

    test('должен работать с высоким порогом', () => {
      const result = FuzzyMatcher.match('appl', candidates, 90);
      expect(result).toBe('apple');
    });

    test('должен выбрать лучшее совпадение из нескольких подходящих', () => {
      const testCandidates = ['apple pie', 'apple juice', 'apple'];
      const result = FuzzyMatcher.match('apple', testCandidates);
      expect(result).toBe('apple');
    });

    test('должен обрабатывать пустой запрос', () => {
      const result = FuzzyMatcher.match('', candidates);
      expect(result).toBeNull();
    });

    test('должен обрабатывать пробелы в запросе', () => {
      const testCandidates = ['apple juice', 'orange juice', 'grape juice'];
      const result = FuzzyMatcher.match('apple juice', testCandidates);
      expect(result).toBe('apple juice');
    });

    test('должен обрабатывать частичные совпадения с пробелами', () => {
      const testCandidates = ['apple juice', 'orange juice', 'grape juice'];
      const result = FuzzyMatcher.match('apple', testCandidates, 60);
      expect(result).toBe('apple juice');
    });

    test('должен выбросить ошибку для пустого массива кандидатов', () => {
      expect(() => {
        FuzzyMatcher.match('banana', []);
      }).toThrow('Invalid candidates list');
    });

    test('должен выбросить ошибку для null кандидатов', () => {
      expect(() => {
        FuzzyMatcher.match('banana', null as any);
      }).toThrow('Invalid candidates list');
    });

    test('должен выбросить ошибку для undefined кандидатов', () => {
      expect(() => {
        FuzzyMatcher.match('banana', undefined as any);
      }).toThrow('Invalid candidates list');
    });

    test('должен работать с массивом из одного элемента', () => {
      const result = FuzzyMatcher.match('apple', ['apple']);
      expect(result).toBe('apple');
    });

    test('должен работать с массивом из одного элемента, который не совпадает', () => {
      const result = FuzzyMatcher.match('banana', ['apple'], 70);
      expect(result).toBeNull();
    });

    test('должен использовать значение порога по умолчанию (70)', () => {
      // Тест, который проходит с порогом 70, но не проходит с более высоким
      const result = FuzzyMatcher.match('appl', ['apple']);
      expect(result).toBe('apple');
    });

    test('должен обрабатывать специальные символы', () => {
      const testCandidates = ['apple-pie', 'apple_juice', 'apple.cake'];
      const result = FuzzyMatcher.match('apple pie', testCandidates, 60);
      expect(result).toBe('apple-pie');
    });

    test('должен обрабатывать числа в строках', () => {
      const testCandidates = ['apple1', 'apple2', 'apple3'];
      const result = FuzzyMatcher.match('apple2', testCandidates);
      expect(result).toBe('apple2');
    });

    test('должен обрабатывать длинные строки', () => {
      const testCandidates = [
        'very long apple description with many words',
       'another long banana description',
        'short apple'
      ];
      const result = FuzzyMatcher.match('apple description', testCandidates, 50);
      expect(result).toBe('very long apple description with many words');
    });
*/
  });

  describe('matchWithScore', () => {
    const candidates = ['apple', 'banana', 'orange', 'grape', 'pineapple'];

    test('должен вернуть точное совпадение с высоким score', () => {
      const result = FuzzyMatcher.matchWithScore('banana', candidates);
      expect(result.match).toBe('banana');
      expect(result.score).toBeGreaterThan(90);
    });

    test('должен вернуть частичное совпадение с score', () => {
      const result = FuzzyMatcher.matchWithScore('bana', candidates);
      expect(result.match).toBe('banana');
      expect(result.score).toBeGreaterThan(70);
      expect(result.score).toBeLessThan(100);
    });

    test('должен вернуть null при низком score но показать score', () => {
      const result = FuzzyMatcher.matchWithScore('xyz', candidates, 80);
      expect(result.match).toBeNull();
      expect(result.score).toBeGreaterThanOrEqual(0);
      expect(result.score).toBeLessThan(80);
    });

    test('должен возвращать score даже когда совпадение не найдено', () => {
      const result = FuzzyMatcher.matchWithScore('completely different', candidates, 90);
      expect(result.match).toBeNull();
      expect(typeof result.score).toBe('number');
      expect(result.score).toBeGreaterThanOrEqual(0);
    });

    test('должен работать с пустым списком кандидатов', () => {
      expect(() => {
        FuzzyMatcher.matchWithScore('test', []);
      }).toThrow('Invalid candidates list');
    });
  });
});
