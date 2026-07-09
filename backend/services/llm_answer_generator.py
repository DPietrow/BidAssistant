from openai import OpenAI


client = OpenAI()


class LLMAnswerGenerator:


    def build_context(
        self,
        results
    ):

        context = []


        for item in results:


            contract = item["contract"]

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

Retrieval Method:
{item.get("match_type")}

Evidence:
{item["match"]["matched_text"]}
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

            contract = item["contract"]


            sam_id = contract["sam_id"]


            # prevent duplicates
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
        filters=None
    ):


        context = self.build_context(
            results
        )


        filter_context = ""


        if filters:

            filter_context = f"""

Active Search Filters:

{filters}

"""


        prompt = f"""

You are Athena, an expert government procurement intelligence assistant.

Answer the user's question using ONLY the supplied contract information.

Rules:

- Do not invent vendors, agencies, dates, or contract details.
- If information is unavailable, clearly state that.
- Reference SAM IDs when discussing specific opportunities.
- Summarize the opportunities clearly.
- Do not create citations. Citations are handled separately.


{filter_context}


Contract Information:

{context}


Question:

{query}


Answer:

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
        filters=None
    ):


        answer = self.generate(
            query=query,
            results=results,
            filters=filters
        )


        citations = self.build_citations(
            results
        )


        return {

            "answer":
                answer,

            "citations":
                citations

        }



answer_generator = LLMAnswerGenerator()