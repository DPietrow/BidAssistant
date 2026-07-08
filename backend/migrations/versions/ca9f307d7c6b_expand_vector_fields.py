"""expand vector fields

Revision ID: ca9f307d7c6b
Revises: db646d551447
Create Date: 2026-07-07 21:03:25.505283

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'ca9f307d7c6b'
down_revision = 'db646d551447'
branch_labels = None
depends_on = None


def upgrade():


    #
    # Rebuild existing vectors
    #

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


    #
    # Function
    #

    op.execute(
        """
        CREATE OR REPLACE FUNCTION contracts_search_vector_update()

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


    #
    # Trigger
    #

    op.execute(
        """
        DROP TRIGGER IF EXISTS contracts_search_vector_trigger
        ON contracts;
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

    op.execute(
        """
        DROP TRIGGER IF EXISTS contracts_search_vector_trigger
        ON contracts;
        """
    )