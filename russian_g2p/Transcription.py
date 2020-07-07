#!/usr/bin/python3
"""Transcription class.

:class: Transcription is used to transcribe text.

  Typical usage example:
  ...

"""
from russian_g2p.Preprocessor import Preprocessor
from russian_g2p.Accentor import Accentor
from russian_g2p.Grapheme2Phoneme import Grapheme2Phoneme


class Transcription:
    """[summary]
    """

    def __init__(self, raise_exceptions: bool = False, batch_size: int = 64,
                 verbose: bool = False, use_wiki: bool = False):
        """[summary]

        Args:
            raise_exceptions (bool, optional): [description]. Defaults to False.
            batch_size (int, optional): [description]. Defaults to 64.
            verbose (bool, optional): [description]. Defaults to False.
            use_wiki (bool, optional): [description]. Defaults to False.
        """

        self.__preprocessor = Preprocessor(batch_size=batch_size)
        self.__accentor = Accentor(exception_for_unknown=raise_exceptions, use_wiki=use_wiki)
        self.__g2p = Grapheme2Phoneme(exception_for_nonaccented=raise_exceptions)
        self.verbose = verbose

    def __call__(self, texts: list):
        """[summary]

        Args:
            texts (list): [description]

        Returns:
            [type]: [description]
        """

        return self.transcribe(texts)

    def transcribe(self, texts: list) -> list:
        """[summary]

        Args:
            texts (list): [description]

        Returns:
            list: [description]
        """

        all_words_and_tags = self.__preprocessor.preprocessing(texts)
        if self.verbose:
            print('All texts have been preprocessed...')
        n_texts = len(texts)
        n_data_parts = 100
        part_size = n_texts // n_data_parts
        while (part_size * n_data_parts) < n_texts:
            part_size += 1
        data_counter = 0
        part_counter = 0
        total_result = []
        for cur_words_and_tags in all_words_and_tags:
            try:
                accented_text = self.__accentor.do_accents(cur_words_and_tags)
            except:
                accented_text = []
            if len(accented_text) > 0:
                tmp = ' '.join(accented_text[0])
                tmp = ' ' + tmp
                phonetic_words = tmp.split(' <sil>')
                try:
                    result = []
                    for phonetic_word in phonetic_words:
                        if len(phonetic_word) != 0:
                            phonemes = self.__g2p.phrase_to_phonemes(phonetic_word)
                            result.append(phonemes)
                except:
                    result = []
            else:
                result = []
            total_result.append(result)
            data_counter += 1
            if (part_size > 0) and self.verbose:
                if (data_counter % part_size) == 0:
                    part_counter += 1
                    print(f'{part_counter}% of texts have been processed...')
        if (part_counter < n_data_parts) and self.verbose:
            print('100% of texts have been processed...')
        return total_result
    
    def bad_words(self):
        return sorted(list(set(self.__accentor.get_bad_words())))
