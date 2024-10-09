import uuid

from django.core.management.base import BaseCommand

from letter.settings import S3_URL
from lucky_letter.domain.letter import Envelope, Stamp, WritingPad
from lucky_letter.infra.repo.letter_repo import LetterRepo
from lucky_letter.service.i_repo.i_letter_repo import ILetterRepo

BASE_URL = S3_URL


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        letter_repo: ILetterRepo = LetterRepo()

        envelopes = [
            Envelope(
                id=str(uuid.uuid4()), name="envelope1", url=f"{BASE_URL}/Envelope1.png"
            ),
            Envelope(
                id=str(uuid.uuid4()), name="envelope2", url=f"{BASE_URL}/Envelope2.png"
            ),
            Envelope(
                id=str(uuid.uuid4()), name="envelope3", url=f"{BASE_URL}/Envelope3.png"
            ),
        ]

        writing_pads = [
            WritingPad(
                id=str(uuid.uuid4()), name="writing_pad1", url=f"{BASE_URL}/Pad+1.png"
            ),
            WritingPad(
                id=str(uuid.uuid4()), name="writing_pad2", url=f"{BASE_URL}/Pad+2.png"
            ),
            WritingPad(
                id=str(uuid.uuid4()), name="writing_pad3", url=f"{BASE_URL}/Pad+3.png"
            ),
            WritingPad(
                id=str(uuid.uuid4()), name="writing_pad4", url=f"{BASE_URL}/Pad+4.png"
            ),
        ]

        stamps = [
            Stamp(id=str(uuid.uuid4()), name="stamp1", url=f"{BASE_URL}/Stamp+1.svg"),
            Stamp(id=str(uuid.uuid4()), name="stamp2", url=f"{BASE_URL}/Stamp+2.svg"),
            Stamp(id=str(uuid.uuid4()), name="stamp3", url=f"{BASE_URL}/Stamp+3.svg"),
            Stamp(id=str(uuid.uuid4()), name="stamp4", url=f"{BASE_URL}/Stamp+4.svg"),
        ]

        for envelope in envelopes:
            letter_repo.register_envelope(envelope)

        for writing_pad in writing_pads:
            letter_repo.register_writing_pad(writing_pad)

        for stamp in stamps:
            letter_repo.register_stamp(stamp)

        print("register clear")
