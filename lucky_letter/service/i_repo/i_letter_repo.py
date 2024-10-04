from abc import ABCMeta, abstractmethod

from lucky_letter.domain.letter import Envelope as EnvelopeVo
from lucky_letter.domain.letter import Letter as LetterVo
from lucky_letter.domain.letter import LetterGroup as LetterGroupVo
from lucky_letter.domain.letter import Stamp as StampVo
from lucky_letter.domain.letter import WritingPad as WritingPadVo


class ILetterGroupRepo(metaclass=ABCMeta):
    class Filter:
        def __init__(self):
            pass

    @abstractmethod
    def create(self, letter_group_vo: LetterGroupVo) -> LetterGroupVo:
        pass


class ILetterRepo(metaclass=ABCMeta):
    class Filter:
        def __init__(self):
            pass

    @abstractmethod
    def create(self, letter_vo: LetterVo) -> LetterVo:
        pass

    @abstractmethod
    def register_envelope(self, envelop: EnvelopeVo) -> EnvelopeVo:
        """
        admin 용
        """
        pass

    @abstractmethod
    def register_writing_pad(self, writing_pad: WritingPadVo) -> WritingPadVo:
        """
        admin 용
        """
        pass

    @abstractmethod
    def register_stamp(self, stamp: StampVo) -> StampVo:
        """
        admin 용
        """
        pass
