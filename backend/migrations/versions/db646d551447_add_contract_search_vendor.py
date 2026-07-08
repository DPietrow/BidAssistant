"""add contract search vector

Revision ID: db646d551447
Revises: 0b28c4605cd3
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "db646d551447"
down_revision = "0b28c4605cd3"
branch_labels = None
depends_on = None


def upgrade():

    # --------------------------------------------------
    # contract_embeddings
    # --------------------------------------------------

    op.add_column(
        "contract_embeddings",
        sa.Column(
            "embedding_version",
            sa.Integer(),
            nullable=False,
            server_default="1"
        )
    )

    op.alter_column(
        "contract_embeddings",
        "embedding_version",
        server_default=None
    )


    op.drop_constraint(
        "contract_embeddings_chunk_id_key",
        "contract_embeddings",
        type_="unique"
    )


    op.create_index(
        "ix_contract_embeddings_chunk_id",
        "contract_embeddings",
        ["chunk_id"],
        unique=True
    )


    # --------------------------------------------------
    # contracts.search_vector
    # --------------------------------------------------

    op.add_column(
        "contracts",
        sa.Column(
            "search_vector",
            postgresql.TSVECTOR(),
            nullable=True
        )
    )


    # --------------------------------------------------
    # Populate existing contracts
    # --------------------------------------------------

    op.execute(
        """
        UPDATE contracts

        SET search_vector =
            to_tsvector(
                'english',
                concat_ws(
                    ' ',
                    title,
                    description,
                    agency,
                    office,
                    naics,
                    notice_type,
                    set_aside,
                    sam_id,
                    solicitation_number,
                    psc_code,
                    raw_text
                )
            );
        """
    )


    # --------------------------------------------------
    # GIN index
    # --------------------------------------------------

    op.create_index(
        "contract_search_vector_idx",
        "contracts",
        ["search_vector"],
        postgresql_using="gin"
    )


    # --------------------------------------------------
    # Automatic search vector updates
    # --------------------------------------------------

    op.execute(
        """
        CREATE FUNCTION contracts_search_vector_update()

        RETURNS trigger AS $$

        BEGIN

            NEW.search_vector :=
                to_tsvector(
                    'english',
                    concat_ws(
                        ' ',
                        NEW.title,
                        NEW.description,
                        NEW.agency,
                        NEW.office,
                        NEW.naics,
                        NEW.notice_type,
                        NEW.set_aside,
                        NEW.sam_id,
                        NEW.solicitation_number,
                        NEW.psc_code,
                        NEW.raw_text
                    )
                );

            RETURN NEW;

        END;

        $$ LANGUAGE plpgsql;
        """
    )


    op.execute(
        """
        CREATE TRIGGER contracts_search_vector_trigger

        BEFORE INSERT OR UPDATE

        ON contracts

        FOR EACH ROW

        EXECUTE FUNCTION contracts_search_vector_update();
        """
    )



def downgrade():


    # --------------------------------------------------
    # Remove trigger
    # --------------------------------------------------

    op.execute(
        """
        DROP TRIGGER IF EXISTS
        contracts_search_vector_trigger
        ON contracts;
        """
    )


    op.execute(
        """
        DROP FUNCTION IF EXISTS
        contracts_search_vector_update();
        """
    )


    # --------------------------------------------------
    # contracts
    # --------------------------------------------------

    op.drop_index(
        "contract_search_vector_idx",
        table_name="contracts"
    )


    op.drop_column(
        "contracts",
        "search_vector"
    )


    # --------------------------------------------------
    # contract_embeddings
    # --------------------------------------------------

    op.drop_index(
        "ix_contract_embeddings_chunk_id",
        table_name="contract_embeddings"
    )


    op.create_unique_constraint(
        "contract_embeddings_chunk_id_key",
        "contract_embeddings",
        ["chunk_id"]
    )


    op.drop_column(
        "contract_embeddings",
        "embedding_version"
    )