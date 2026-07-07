import logging
from datetime import datetime

from database import db

from models import Contract, ContractChunk, ContractEmbedding

from services.chunking_service import chunking_service
from services.embedding_service import embedding_service


logger = logging.getLogger(__name__)


class EmbeddingPipeline:

    def process_pending(self, batch_size=25):

        contracts = (
            Contract.query
            .filter(
                Contract.embedding_status.in_(
                    [
                        "pending",
                        "failed"
                    ]
                )
            )
            .limit(batch_size)
            .all()
        )


        results = {
            "processed": 0,
            "success": 0,
            "failed": 0
        }


        for contract in contracts:

            results["processed"] += 1

            try:

                self.embed_contract(contract)

                results["success"] += 1


            except Exception as e:

                logger.exception(
                    "Embedding failed %s",
                    contract.sam_id
                )

                self.mark_failed(
                    contract,
                    e
                )

                results["failed"] += 1


        return results



    def embed_contract(self, contract):

        logger.info(
            "Starting embedding %s",
            contract.sam_id
        )


        start = datetime.utcnow()


        #
        # Mark processing
        #

        contract.embedding_status = "processing"

        db.session.commit()


        #
        # STEP 1
        # Chunk in memory
        #

        chunks = chunking_service.chunk_contract(
            contract
        )


        logger.info(
            "%s generated %s chunks",
            contract.sam_id,
            len(chunks)
        )



        #
        # STEP 2
        # Generate embeddings
        #
        # No database interaction here
        #

        embedded_chunks = []


        for index, text in enumerate(chunks):

            vector = (
                embedding_service
                .create_embedding(text)
            )


            embedded_chunks.append({

                "index": index,

                "text": text,

                "tokens": len(text.split()),

                "vector": vector

            })



        #
        # STEP 3
        # Short DB transaction
        #

        self.persist_embeddings(
            contract,
            embedded_chunks
        )


        #
        # Metadata
        #

        contract.embedding_status = "completed"

        contract.chunk_count = len(
            embedded_chunks
        )

        contract.embedding_model = (
            embedding_service.model
        )

        contract.embedded_at = datetime.utcnow()

        contract.processing_time_ms = int(

            (
                datetime.utcnow() - start
            )
            .total_seconds()
            *
            1000

        )


        db.session.commit()



    def persist_embeddings(
        self,
        contract,
        chunks
    ):

        #
        # Remove previous embeddings
        #

        ContractChunk.query.filter_by(
            contract_id=contract.id
        ).delete()



        for item in chunks:


            chunk = ContractChunk(

                contract_id=contract.id,

                chunk_index=item["index"],

                chunk_text=item["text"],

                token_count=item["tokens"]

            )


            db.session.add(chunk)

            db.session.flush()



            embedding = ContractEmbedding(

                chunk_id=chunk.id,

                model=embedding_service.model,

                dimensions=len(
                    item["vector"]
                ),

                embedding=item["vector"]

            )


            db.session.add(
                embedding
            )



    def mark_failed(
        self,
        contract,
        error
    ):

        db.session.rollback()


        contract.embedding_status = "failed"

        contract.embedding_error = str(error)


        db.session.commit()



embedding_pipeline = EmbeddingPipeline()