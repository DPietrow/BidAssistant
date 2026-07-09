from openai import OpenAI


client = OpenAI()



class LLMAnswerGenerator:



    def normalize_contract(
        self,
        item
    ):
        """
        Converts either:

        1. Retrieval result
        2. Selected contract

        into a common format
        """


        # Retrieval pipeline object

        if "contract" in item:


            contract = item["contract"]


            return {

                "sam_id":
                    contract.get("sam_id"),


                "title":
                    contract.get("title"),


                "agency":
                    contract.get("agency"),


                "naics":
                    contract.get("naics"),


                "url":
                    contract.get("url"),


                "evidence":
                    item.get(
                        "match",
                        {}
                    ).get(
                        "matched_text",
                        ""
                    ),


                "retrieval_method":
                    item.get(
                        "match_type"
                    )

            }



        # Direct selected contract

        return {

            "sam_id":
                item.get("sam_id"),


            "title":
                item.get("title"),


            "agency":
                item.get("agency"),


            "naics":
                item.get("naics"),


            "url":
                item.get("url"),


            "evidence":
                item.get(
                    "description",
                    ""
                ),


            "retrieval_method":
                "selected_contract"

        }




    def build_context(
        self,
        results
    ):


        context = []


        for item in results:


            contract = self.normalize_contract(
                item
            )


            context.append(

f"""
SAM ID:
{contract["sam_id"]}

Contract Title:
{contract["title"]}

Agency:
{contract["agency"]}

NAICS:
{contract.get("naics")}

Context Source:
{contract["retrieval_method"]}

Evidence:
{contract["evidence"]}
"""

            )


        return "\n\n".join(context)





    def build_citations(
        self,
        results
    ):


        citations = []


        seen = set()



        for item in results:


            contract = self.normalize_contract(
                item
            )


            sam_id = contract["sam_id"]



            if not sam_id:
                continue



            if sam_id in seen:
                continue



            seen.add(
                sam_id
            )



            citations.append(

                {

                    "sam_id":
                        sam_id,


                    "title":
                        contract["title"],


                    "agency":
                        contract["agency"],


                    "url":
                        contract.get("url")

                }

            )


        return citations





    def generate(
        self,
        query,
        results,
        selected_contracts=None,
        filters=None
    ):



        results = results or []


        selected_contracts = (
            selected_contracts
            or []
        )


        #
        # Selected contracts get priority
        #

        if selected_contracts:

            context_results = selected_contracts

        else:

            context_results = results



        context = self.build_context(
            context_results
        )



        filter_context = ""



        if filters:


            filter_context = f"""

Active Search Filters:

{filters}

"""



        prompt = f"""

You are Athena, an expert government procurement intelligence assistant.

You help users analyze government contracting opportunities.

Answer the user's question using ONLY the supplied contract information.

Rules:

- Do not invent vendors, agencies, dates, values, or contract details.
- If information is unavailable, say so clearly.
- Always reference SAM IDs when discussing opportunities.
- If multiple contracts are provided, compare them when appropriate.
- Highlight differences in agencies, scope, NAICS, or available information.
- Do not create citations. Citations are generated separately.


{filter_context}


Contract Information:

{context}


User Question:

{query}


Athena Response:

"""



        response = client.responses.create(

            model="gpt-5",

            input=prompt

        )



        return response.output_text






    def generate_with_citations(
        self,
        query,
        results,
        selected_contracts=None,
        filters=None
    ):


        answer = self.generate(

            query=query,

            results=results,

            selected_contracts=selected_contracts,

            filters=filters

        )


        citations = self.build_citations(

            selected_contracts
            if selected_contracts
            else results

        )


        return {

            "answer":
                answer,


            "citations":
                citations

        }




answer_generator = LLMAnswerGenerator()