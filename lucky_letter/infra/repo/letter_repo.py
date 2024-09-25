from lucky_letter.domain.letter import Envelope as EnvelopeVo
from lucky_letter.domain.letter import Letter as LetterVo
from lucky_letter.domain.letter import Stamp as StampVo
from lucky_letter.domain.letter import WritingPad as WritingPadVo
from lucky_letter.infra.models.serializers import (
    EnvelopeSerializer,
    LetterSerializer,
    StampSerializer,
    WritingPadSerializer,
)
from lucky_letter.service.i_repo.i_letter_repo import ILetterRepo


class LetterRepo(ILetterRepo):
    def create(self, letter_vo: LetterVo) -> LetterVo:
        letter_dict = letter_vo.to_dto()
        serializer = LetterSerializer(data=letter_dict)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return letter_vo

    def register_envelope(self, envelop: EnvelopeVo) -> EnvelopeVo:
        """
        admin 용
        """
        envelop_dict = envelop.to_dto()
        serializer = EnvelopeSerializer(data=envelop_dict)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return envelop

    def register_writing_pad(self, writing_pad: WritingPadVo) -> WritingPadVo:
        """
        admin 용
        """
        writing_pad_dict = writing_pad.to_dto()
        serializer = WritingPadSerializer(data=writing_pad_dict)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return writing_pad

    def register_stamp(self, stamp: StampVo) -> StampVo:
        """
        admin 용
        """
        stamp_dict = stamp.to_dto()
        serializer = StampSerializer(data=stamp_dict)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return stamp
