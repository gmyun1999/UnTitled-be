from lucky_letter.domain.letter import Envelope as EnvelopeVo
from lucky_letter.domain.letter import Letter as LetterVo
from lucky_letter.domain.letter import LetterRelation as LetterRelationVo
from lucky_letter.domain.letter import Stamp as StampVo
from lucky_letter.domain.letter import WritingPad as WritingPadVo
from lucky_letter.infra.models.letter_model import Letter, LetterRelation
from lucky_letter.infra.models.serializers import (
    EnvelopeSerializer,
    LetterRelationSerializer,
    LetterSerializer,
    StampSerializer,
    WritingPadSerializer,
)
from lucky_letter.service.i_repo.i_letter_repo import ILetterRelationRepo, ILetterRepo


class LetterRelationRepo(ILetterRelationRepo):
    def get_letter_relation(self, target_letter_id: str) -> LetterRelationVo | None:
        try:
            letter_relation = LetterRelation.objects.get(
                target_letter_id=target_letter_id
            )
            serializer = LetterRelationSerializer(letter_relation)
            dicted_data = serializer.data
        except LetterRelation.DoesNotExist:
            return None
        return LetterRelationVo.from_dict(dicted_data)

    def create(self, letter_relation_vo: LetterRelationVo) -> LetterRelationVo:
        dicted = letter_relation_vo.to_dict()
        serializer = LetterRelationSerializer(data=dicted)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return letter_relation_vo


class LetterRepo(ILetterRepo):
    def get_letter(self, filter: ILetterRepo.Filter) -> LetterVo | None:
        try:
            letter = Letter.objects.all()
            if filter.id:
                letter = letter.get(id=filter.id)
            serializer = LetterSerializer(letter)
            dicted_data = serializer.data
        except Letter.DoesNotExist:
            return None
        return LetterVo.from_dict(dicted_data)

    def create(self, letter_vo: LetterVo) -> LetterVo:
        letter_dict = letter_vo.to_dict()
        serializer = LetterSerializer(data=letter_dict)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return letter_vo

    def register_envelope(self, envelop: EnvelopeVo) -> EnvelopeVo:
        """
        admin 용
        """
        envelop_dict = envelop.to_dict()
        serializer = EnvelopeSerializer(data=envelop_dict)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return envelop

    def register_writing_pad(self, writing_pad: WritingPadVo) -> WritingPadVo:
        """
        admin 용
        """
        writing_pad_dict = writing_pad.to_dict()
        serializer = WritingPadSerializer(data=writing_pad_dict)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return writing_pad

    def register_stamp(self, stamp: StampVo) -> StampVo:
        """
        admin 용
        """
        stamp_dict = stamp.to_dict()
        serializer = StampSerializer(data=stamp_dict)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return stamp
