from openai import OpenAI

from config import Config


class EmbeddingService:

    def __init__(self):

        self.client = OpenAI(
            api_key=Config.OPENAI_API_KEY
        )

        #
        # Great balance of quality + price
        #

        self.model = "text-embedding-3-small"

    # --------------------------------------------------------

    def create_embedding(
        self,
        text: str,
    ) -> list[float]:

        if not text:

            raise ValueError(
                "Cannot embed empty text."
            )

        response = self.client.embeddings.create(

            model=self.model,

            input=text

        )

        return response.data[0].embedding
    
    # --------------------------------------------------------

    
    def embed_query(
        self,
        query: str
    ) -> list[float]:


        return self.create_embedding(
            query
        )

    # --------------------------------------------------------

    def create_contract_text(
        self,
        contract,
    ) -> str:

        sections = [

            contract.title,

            contract.agency,

            contract.description,

            contract.raw_text,

            contract.naics,

            contract.notice_type,

            contract.set_aside

        ]

        return "\n\n".join(

            s.strip()

            for s in sections

            if s

        )


embedding_service = EmbeddingService()