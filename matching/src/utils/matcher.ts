import fuzz from 'fuzzball';

export interface MatchResult {
  match: string | null;
  score: number;
}

export class FuzzyMatcher {
  static match(
    query: string,
    candidates: string[],
    threshold: number = 70
  ): string | null {
    if (!Array.isArray(candidates) || candidates.length === 0) {
      throw new Error('Invalid candidates list');
    }

    const results = fuzz.extract(query, candidates, {
      scorer: fuzz.token_set_ratio,
      limit: 1
    });

    const [bestMatch, score] = results[0] ?? [null, 0];

    return score >= threshold ? bestMatch : null;
  }

  static matchWithScore(
    query: string,
    candidates: string[],
    threshold: number = 70
  ): MatchResult {
    if (!Array.isArray(candidates) || candidates.length === 0) {
      throw new Error('Invalid candidates list');
    }

    const results = fuzz.extract(query, candidates, {
      scorer: fuzz.token_set_ratio,
      limit: 1
    });

    const [bestMatch, score] = results[0] ?? [null, 0];

    return {
      match: score >= threshold ? bestMatch : null,
      score: score
    };
  }
}
