import re


class ChunkingService:


    def __init__(
        self,
        chunk_size=500,
        overlap=100
    ):

        self.chunk_size = chunk_size
        self.overlap = overlap



    def chunk_contract(
        self,
        contract
    ):

        text = self.create_contract_text(
            contract
        )

        return self.chunk_text(
            text
        )



    def create_contract_text(
        self,
        contract
    ):


        sections = [

            f"Title:\n{contract.title}",

            f"Agency:\n{contract.agency}",

            f"Office:\n{contract.office}",

            f"Description:\n{contract.description}",

            f"Solicitation:\n{contract.solicitation_number}",

            f"NAICS:\n{contract.naics}",

            f"PSC Code:\n{contract.psc_code}",

            f"Notice Type:\n{contract.notice_type}",

            f"Set Aside:\n{contract.set_aside}",

            f"Additional Details:\n{contract.raw_text}"

        ]


        return "\n\n".join(

            section

            for section in sections

            if section and "None" not in section

        )



    def chunk_text(
        self,
        text
    ):
 

        words = text.split()


        chunks = []


        start = 0


        while start < len(words):

            end = start + self.chunk_size


            chunk = words[start:end]


            chunks.append(
                " ".join(chunk)
            )


            start += (
                self.chunk_size
                -
                self.overlap
            )


        return chunks



chunking_service = ChunkingService()