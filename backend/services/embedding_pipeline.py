from datetime import datetime
import logging

from database import db

from models import (
    Contract,
    ContractChunk,
    ContractEmbedding
)

from services.chunking_service import chunking_service
from services.embedding_service import embedding_service

logger = logging.getLogger(__name__)


class EmbeddingPipeline:

    # =====================================================
    # PUBLIC ENTRY POINT
    # =====================================================

    def process_pending(self, batch_size: int = 25):

        pending_contracts = (
            Contract.query
            .filter(
                Contract.embedding_status.in_(
                    ["pending", "failed"]
                )
            )
            .order_by(Contract.posted_date.desc())
            .limit(batch_size)
            .all()
        )

        summary = {

            "processed": 0,
            "successful": 0,
            "failed": 0

        }

        logger.info(
            "Found %s contracts to process.",
            len(pending_contracts)
        )

        for contract in pending_contracts:

            summary["processed"] += 1

            try:

                self.embed_contract(contract)

                summary["successful"] += 1

            except Exception as ex:

                logger.exception(
                    "Embedding failed for %s",
                    contract.sam_id
                )

                db.session.rollback()

                contract.embedding_status = "failed"
                contract.embedding_error = str(ex)
                contract.embedding_attempts += 1

                db.session.commit()

                summary["failed"] += 1

        return summary

    # =====================================================
    # EMBED SINGLE CONTRACT
    # =====================================================

    def embed_contract(self, contract):

        logger.info(
            "Embedding %s",
            contract.sam_id
        )

        start_time = datetime.utcnow()

        #
        # Begin pipeline
        #

        contract.embedding_status = "processing"

        #
        # Delete previous chunks.
        #
        # Embeddings cascade automatically.
        #

        ContractChunk.query.filter_by(
            contract_id=contract.id
        ).delete()

        #
        # Build chunks
        #

        chunks = chunking_service.chunk_contract(contract)

        contract.chunk_count = len(chunks)

        #
        # Process each chunk
        #

        self._process_chunks(
            contract,
            chunks
        )

        #
        # Final metadata
        #

        contract.embedding_status = "completed"

        contract.embedding_model = embedding_service.model

        contract.embedded_at = datetime.utcnow()

        contract.processing_time_ms = int(

            (
                datetime.utcnow() - start_time
            ).total_seconds() * 1000

        )

        db.session.commit()

        logger.info(
            "Finished %s (%s chunks)",
            contract.sam_id,
            len(chunks)
        )

    # =====================================================
    # PROCESS CHUNKS
    # =====================================================

    def _process_chunks(
        self,
        contract,
        chunks
    ):

        for index, chunk_text in enumerate(chunks):

            #
            # Create DB chunk
            #

            chunk = ContractChunk(

                contract_id=contract.id,

                chunk_index=index,

                chunk_text=chunk_text,

                token_count=len(chunk_text.split())

            )

            db.session.add(chunk)

            #
            # Flush so chunk.id exists
            #

            db.session.flush()

            #
            # Generate embedding
            #

            vector = embedding_service.create_embedding(
                chunk_text
            )

            embedding = ContractEmbedding(

                chunk_id=chunk.id,

                model=embedding_service.model,

                dimensions=len(vector),

                embedding=vector

            )

            db.session.add(embedding)


embedding_pipeline = EmbeddingPipeline()