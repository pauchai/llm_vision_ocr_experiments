import re
from rapidfuzz import fuzz, process


def correct_units(text:str):
    rules = [
        (r'(\d+)(n|п)\b', r'\1л'),
        (r'(\d+)r\b', r'\1г'),
        (r'(\d+)(mn|мn|mл)\b', r'\1мл'),
        (r'(\d+)(mr|мr|mг)\b', r'\1мг'),
        (r'(\d+)([yу]n|уn|уп|yп)\b', r'\1уп'),
        (r'(\d+)(kr|кr|kг)\b', r'\1кг'),
    ]
    for pattern, repl in rules:
        text = re.sub(pattern, repl, text, flags=re.IGNORECASE)
    return text


class PhraseCorrectorNgrams:
    def __init__(self, words_file="words.csv", score_cutoff=85, min_len=3, max_ngram=3):
        # Чтение и нормализация фраз
        with open(words_file, "r", encoding="utf-8") as f:
            raw_phrases = [line.strip().upper().replace("Ё", "Е") for line in f if line.strip()]

        # Группировка по количеству слов
        self.reference_by_length = {}
        for phrase in raw_phrases:
            word_count = len(phrase.split())
            if word_count not in self.reference_by_length:
                self.reference_by_length[word_count] = []
            self.reference_by_length[word_count].append(phrase)

        self.score_cutoff = score_cutoff
        self.min_len = min_len
        self.max_ngram = max_ngram

    def correct_text(self, text):
        text = text.upper().replace("Ё", "Е")
        tokens = re.split(r"[ \n\t\f\v]+", text)
        tokens = list(filter(None, tokens))

        corrected_tokens = tokens[:]
        corrected = [False] * len(tokens)
        corrections_log = []

        for n in range(self.max_ngram, 0, -1):
            if n not in self.reference_by_length:
                continue  # нет эталонов нужной длины

            for i in range(len(tokens) - n + 1):
                if any(corrected[i:i+n]):
                    continue

                ngram_tokens = tokens[i:i+n]
                ngram = ' '.join(ngram_tokens)
                if len(ngram) < self.min_len:
                    continue

                match = process.extractOne(
                    ngram,
                    self.reference_by_length[n],
                    scorer=fuzz.ratio,
                    score_cutoff=self.score_cutoff
                )
                if match:
                    corrected_tokens[i] = match[0]
                    for j in range(i+1, i+n):
                        corrected_tokens[j] = ''
                    corrected[i:i+n] = [True]*n

                    corrections_log.append({
                        "position": i,
                        "original": ngram,
                        "corrected": match[0],
                        "score": match[1],
                    })

        final_text = ' '.join(filter(None, corrected_tokens))
        return final_text, corrections_log

class PhraseCorrectorByWords:
    def __init__(self, words_file="words.csv",score_cutoff=70, min_len = 5):
        with open(words_file, "r", encoding="utf-8") as f:
            self.reference_words = [line.strip() for line in f]
        self.score_cutoff = score_cutoff
        self.min_len = min_len





    def correct_text(self,text):
        corrected_lines = []
        corrections_log = []
        for line_num, line in enumerate(text.strip().split('\n')):
            corrected_words = []
            words = re.split(r"[ \t\f\v]+", line.upper().replace("Ё", "Е"))
            words = list(filter(None, words))  # убираем пустые строки, если они есть
        
            for word_pos, word in enumerate(words):
                if len(word) < self.min_len:
                    corrected_words.append(word)
                    continue
                # Ищем наиболее близкое слово из словаря
                match = process.extractOne(word, self.reference_words, scorer=fuzz.ratio, score_cutoff=self.score_cutoff)
                #print(match)
                corrected_word = match[0] if match else word
                corrected_words.append(corrected_word)
                if match and corrected_word != word:
                    corrections_log.append({
                        "line": line_num + 1,
                        "position": word_pos + 1,
                        "original": word,
                        "corrected": corrected_word,
                        "score": match[1]
                    })
            corrected_lines.append(' '.join(corrected_words))
        return '\n'.join(corrected_lines), corrections_log
    


def correct_text(multiline_text, corrector):
    txt_lines = str(multiline_text).split("\n")
    txt_other = []

    if len(txt_lines) > 2:
        txt_2lines = txt_lines[:2]
        txt_other = txt_lines[2:]
    else:
        txt_2lines = txt_lines

    corrected_lines = []
    corrected_logs = []

    for txt in txt_2lines:
        corrected_text = correct_units(str(txt))   
        corrected_text, corrected_log = corrector.correct_text(corrected_text)
        corrected_lines.append(corrected_text)
        corrected_logs += corrected_log

    # Преобразуем оставшиеся строки в uppercase
    txt_other = [line.upper() for line in txt_other]

    corrected_lines += txt_other
    # Убираем пустые строки и строки из пробелов
    filtered = [line for line in corrected_lines if line.strip()]

    # Собираем финальный текст
    corrected_text = "\n".join(filtered)
    return corrected_text, corrected_logs




if __name__ == "__main__":
    to_be_corerected_corpus  = []
    to_be_corerected_corpus.append( '''
    Пюре Фрутонята
    Пюре Фруктоня
    Цыпленок 80г
    Цыпденок 80r
    Мясое изделие для детского питания
    ''')
    to_be_corerected_corpus.append('''
    Пюре фруктоня
    цыбленок 80000г
    мясное для детского питания
    ''')
    to_be_corerected_corpus.append('''
    бальзам ШАУМ 7
    ТРАВ 300мл 
    для нормальных и жирных волос
    ''')
    to_be_corerected_corpus.append('''
    Тютюнок Занукелия
    500 мг
    ''')
    to_be_corerected_corpus.append('''
    Вино АБРАУ-ДЮРОСО
    0.75л
    13% объёмное, белое п/с
    ''')

    for text in to_be_corerected_corpus:
        print("Исходный текст:\n", text)
        corrector = PhraseCorrectorNgrams()
        corrected_text, corrections_log = correct_text(text, corrector)
        print("Исправленный текст:\n", corrected_text)
        print("Лог исправлений:\n", corrections_log)
        print("-" * 50)



