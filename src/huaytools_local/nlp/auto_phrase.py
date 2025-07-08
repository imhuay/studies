#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Time:
    2022-08-01 17:32
Author:
    HuaYang (imhuay@163.com)
Subject:
    A wrapper of AutoPhrase：命令行调用 AutoPhrase 的简单包装
References:
    - https://github.com/shangjingbo1226/AutoPhrase
    - pip install autophrase
"""
import os
import sys
import json
import time
import shutil

from typing import *
from pathlib import Path
from collections import defaultdict

from huaytools_local.utils import get_logger, TypeUtils

_logger = get_logger()

_Official_Language = ['EN', 'CN', 'JA', 'ES', 'AR', 'FR', 'IT', 'RU']
_ENV_AUTOPHRASE = 'AUTOPHRASE'

Language = Literal['EN', 'CN', 'JA', 'ES', 'AR', 'FR', 'IT', 'RU', 'OTHER']
LanguageArabic = 'AR'
"""
EN: English
FR: French
DE: German
ES: Spanish
IT: Italian
PT: Portuguese
RU: Russian
AR: Arabic
CN: Chinese
JA: Japanese
"""
LIB_PATH = None
_TokenizeMode = Literal['train', 'test', 'direct_test', 'translate', 'segmentation']
_Path = TypeUtils.FilePath


# @singleton
class AutoPhrase:
    """"""
    _lib_path: ClassVar
    _tokenizer: ClassVar[str] = None

    def __init__(self,
                 model_path: _Path,
                 lib_path: _Path = None,
                 fp_train_data: _Path = None,
                 fp_stopwords: _Path = None,
                 fp_seed_words: _Path = None,
                 fp_quality_seed_words: _Path = None,
                 language: Language = 'CN',
                 enable_postag: bool = False,
                 highlight_multi: float = 0.5,
                 highlight_single: float = 0.8,
                 lowercase: bool = True,
                 thread: int = 10,
                 min_sup: int = 10):
        """

        Args:
            model_path:
                ├── model/
                │   ├── segmentation.model
                │   ├── token_mapping.txt
                │   └── ...  # some outputs
                └── tmp/
                    └── ...  # some tmp files
            lib_path:
            fp_train_data:
            fp_stopwords:
            fp_seed_words:
            fp_quality_seed_words:
            language:
            enable_postag:
            highlight_multi:
            highlight_single:
            lowercase:
            thread:
            min_sup:
        """
        self._model_path = Path(model_path)
        self._lib_path = Path(lib_path)
        self._fp_train_data = fp_train_data
        self._fp_stopwords = fp_stopwords
        self._fp_seed_words = fp_seed_words
        self._fp_quality_seed_words = fp_quality_seed_words
        self._language = language
        self._enable_postag = enable_postag
        self._case_sensitive = 'N' if lowercase else 'Y'
        self._thread = thread

        self._check_args()

        if self._language == LanguageArabic:
            self._tagger_model = self.lib_path / "tools/models/arabic.tagger"

        # self._fp_model = self._model_path / 'model'
        self._fp_tmp = Path('tmp')  # self._model_path / 'tmp'

        # model/*
        self._fp_token_mapping = self._model_path / 'token_mapping.txt'
        self._fp_segmentation = self._model_path / 'segmentation.model'

        # tmp/*
        self._fp_tokenized_train = self._fp_tmp / 'tokenized_train.txt'
        self._fp_tokenized_stopwords = self._fp_tmp / 'tokenized_stopwords.txt'
        self._fp_tokenized_all = self._fp_tmp / 'tokenized_all.txt'
        self._fp_tokenized_quality = self._fp_tmp / 'tokenized_quality.txt'

    def _check_args(self):
        assert self._fp_train_data is not None or self._model_path.exists()
        if self._model_path.exists():
            assert self._model_path.is_dir()
        if self._language not in _Official_Language:
            _logger.warning(f'{self._language} is not official supported language')
        assert self._thread > 0

    def train(self, ):
        """"""
        self._tokenize_train_data()
        self._tokenize_stopwords()
        self._tokenize_seed_words()
        self._tokenize_quality_seed_words()
        self._pos_tagging_train()
        self._core_training()

    def extract(self,
                fp_input: _Path,
                fp_save: _Path = None,
                highlight_multi: float = 0,
                highlight_single: float = 0):
        """"""
        # 1. tokenize
        print("===Tokenization===")
        fp_input = Path(fp_input)
        if fp_save is None:
            fp_save = fp_input.parent / r'ret.txt'
        else:
            fp_save = Path(fp_save)

        fp_tokenized = self._fp_tmp / 'tokenized_text_to_seg.txt'
        fp_tokenized_raw = self._fp_tmp / 'raw_tokenized_text_to_seg.txt'
        command = self._get_tokenize_command(fp_input, fp_tokenized, 'direct_test')
        self._run_command(command)
        assert fp_tokenized.exists()
        assert fp_tokenized_raw.exists()

        # 2. postag
        if self._enable_postag:
            pass

        # 3. segment
        print("===Phrasal Segmentation===")
        fp_segmented = self._fp_tmp / 'tokenized_segmented_sentences.txt'
        if self._enable_postag:
            pass
        else:
            command = f'{self.lib_path / "bin/segphrase_segment"}' \
                      f' --thread {self._thread}' \
                      f' --model {self._fp_segmentation}' \
                      f' --highlight-multi {highlight_multi}' \
                      f' --highlight-single {highlight_single}' \
                      f' --text_to_seg_file {fp_tokenized}' \
                      f' --output_tokenized_degmented_sentences {fp_segmented}'
        self._run_command(command)
        assert fp_segmented.exists()

        # 4. output
        print("===Generating Output===")
        command = self._get_tokenize_command(fp_input, fp_save, mode='segmentation',
                                             segmented=fp_segmented,
                                             tokenized_id=fp_tokenized,
                                             tokenized_raw=fp_tokenized_raw)
        self._run_command(command)

    def postag(self):
        """TODO"""
        pass

    def _core_training(self):
        """"""
        if self._enable_postag:
            command = f'{self.lib_path / "/bin/segphrase_train"}' \
                      f' --pos_tag' \
                      f' --train_file {self._fp_tokenized_train}' \
                      f' --'

    def _pos_tagging_train(self):
        """TODO"""
        pass

    def _tokenize_train_data(self):
        """"""
        _logger.info(AutoPhrase._get_start_log())
        command = self._get_tokenize_command(self._fp_train_data,
                                             self._fp_tokenized_train,
                                             mode='train')
        self._run_command(command)

    def _tokenize_stopwords(self):
        """"""
        _logger.info(AutoPhrase._get_start_log())
        command = self._get_tokenize_command(self._fp_stopwords,
                                             self._fp_tokenized_stopwords,
                                             mode='test')
        self._run_command(command)

    def _tokenize_seed_words(self):
        """"""
        _logger.info(AutoPhrase._get_start_log())
        command = self._get_tokenize_command(self._fp_seed_words,
                                             self._fp_tokenized_all,
                                             mode='test')
        self._run_command(command)

    def _tokenize_quality_seed_words(self):
        """"""
        command = self._get_tokenize_command(self._fp_quality_seed_words,
                                             self._fp_tokenized_quality,
                                             mode='test')
        self._run_command(command)

    @classmethod
    def load(cls, model_path):
        """"""

    def _get_tokenize_command(self,
                              input_file,
                              output_file,
                              mode: _TokenizeMode,
                              segmented=None,
                              tokenized_id=None,
                              tokenized_raw=None):
        """"""
        command = f'java {self.tokenizer}' \
                  f' -m {mode}' \
                  f' -i {input_file}' \
                  f' -o {output_file}' \
                  f' -t {self._fp_token_mapping}' \
                  f' -c {self._case_sensitive}' \
                  f' -thread {self._thread}'

        if self._language == LanguageArabic:
            command = f'{command} -tagger_model {self._tagger_model}'

        if segmented is not None:
            assert tokenized_raw is not None and tokenized_raw is not None
            command = f'{command}' \
                      f' -segmented {segmented}' \
                      f' -tokenized_id {tokenized_id}' \
                      f' -tokenized_raw {tokenized_raw}'

        return command

    @staticmethod
    def _run_command(command):
        return os.system(command)

    def _tokenize(self,
                  input_file,
                  output_file,
                  mapping_file,
                  mode: _TokenizeMode,
                  language: Language = 'CN',
                  lowercase: bool = True,
                  thread: int = 10):
        """"""
        case_sensitive = 'N' if lowercase else 'Y'
        command = f'java {self.tokenizer}' \
                  f' -m {mode}' \
                  f' -i {input_file}' \
                  f' -o {output_file}' \
                  f' -t {mapping_file}' \
                  f' -c {case_sensitive}' \
                  f' -thread {thread}'

        if language == LanguageArabic:
            command = f'{command} -tagger_model {self._tagger_model}'

    @property
    def lib_path(self) -> Path:
        if self._lib_path is None:
            self._lib_path = AutoPhrase.find_lib_path()
        return self._lib_path

    @property
    def tokenizer(self):
        if self._tokenizer is None:
            tokenizer_path = f'{self.lib_path}:' \
                             f'{self.lib_path}/tools/tokenizer/lib/*:' \
                             f'{self.lib_path}/tools/tokenizer/resources/:' \
                             f'{self.lib_path}/tools/tokenizer/build/'
            self._tokenizer = f'-cp {tokenizer_path} Tokenizer'
        return self._tokenizer

    @staticmethod
    def find_lib_path() -> Path:
        """
        TODO:
            - `pip install autophrase` 安装的 autophrase 有问题
            - 修改为 从 github 下载
        """

        def try_import():
            try:
                import autophrase  # noqa
            except ImportError:
                _p = None
            else:
                _p = Path(Path(autophrase.__file__).parent)
            return _p

        if _ENV_AUTOPHRASE in os.environ:
            lib_path = os.environ[_ENV_AUTOPHRASE]
        elif p := try_import():
            lib_path = p
        else:
            raise ValueError(f'Not find autophrase. '
                             f'Please `pip install autophrase` or '
                             f'download from "https://github.com/shangjingbo1226/AutoPhrase"')
        return Path(lib_path)

    @staticmethod
    def _get_start_log() -> str:
        from huaytools_local.utils import get_caller_name
        return f'=== Start {get_caller_name()} ==='


class __Test:
    """"""

    def __init__(self):
        """"""
        self.model_path = Path(r'/Users/huay/tmp/autophrase_model_test')
        self.model = AutoPhrase(self.model_path)

        for k, v in self.__class__.__dict__.items():
            if k.startswith('_test') and isinstance(v, Callable):
                print(f'\x1b[32m=== Start "{k}" {{\x1b[0m')
                start = time.time()
                v(self)
                print(f'\x1b[32m}} End "{k}" - Spend {time.time() - start:3f}s===\x1b[0m\n')

    def _test_doctest(self):  # noqa
        """"""
        import doctest
        doctest.testmod()

    def _test_tokenize(self):  # noqa
        """"""
        model = self.model
        fp_input = self.model_path / r'dish_name_20220801_demo_100.txt'
        model.extract(fp_input)


if __name__ == '__main__':
    """"""
    __Test()
    # print(os.environ['AUTOPHRASE'])
