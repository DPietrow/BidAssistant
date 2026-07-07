import re
from typing import List


class ChunkingService:

    def __init__(
        self,
        chunk_size: int = 1200,
        overlap: int = 200,
    ):

        if overlap >= chunk_size:
            raise ValueError(
                "overlap must be smaller than chunk_size"
            )

        self.chunk_size = chunk_size
        self.overlap = overlap


    def normalize(self, text: str) -> str:

        if not text:
            return ""

        text = text.replace("\r\n", "\n")

        # remove trailing whitespace
        text = re.sub(r"[ \t]+", " ", text)

        # collapse excessive blank lines
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()


    def split_paragraphs(self, text: str):

        return [
            p.strip()
            for p in text.split("\n\n")
            if p.strip()
        ]

    

    def split_sentences(self, paragraph: str):

        return re.split(
            r'(?<=[.!?])\s+',
            paragraph
        )


    def chunk(self, text: str) -> List[str]:

        text = self.normalize(text)

        if not text:
            return []

        paragraphs = self.split_paragraphs(text)

        chunks = []

        current = ""

        for paragraph in paragraphs:

            #
            # Paragraph fits
            #

            if len(current) + len(paragraph) + 2 <= self.chunk_size:

                if current:
                    current += "\n\n"

                current += paragraph
                continue

            #
            # Flush current chunk
            #

            if current:

                chunks.append(current)

                overlap_text = current[-self.overlap:]

                current = overlap_text + "\n\n"

            #
            # Paragraph itself too large
            #

            if len(paragraph) > self.chunk_size:

                sentences = self.split_sentences(paragraph)

                for sentence in sentences:

                    if len(current) + len(sentence) + 1 <= self.chunk_size:

                        current += " " + sentence

                    else:

                        chunks.append(current.strip())

                        overlap_text = current[-self.overlap:]

                        current = overlap_text + " " + sentence

            else:

                current += paragraph

        if current.strip():

            chunks.append(current.strip())

        return chunks


    def enumerate_chunks(self, text: str):

        chunks = self.chunk(text)

        return [

            {
                "chunk_index": i,
                "chunk_text": chunk
            }

            for i, chunk in enumerate(chunks)

        ]


chunking_service = ChunkingService()