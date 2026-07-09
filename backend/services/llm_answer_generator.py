from openai import OpenAI


client = OpenAI()


class LLMAnswerGenerator:


    def build_context(
        self,
        results
    ):

        context = []


        for item in results:


            context.append(

f"""
Contract ID:
{item["contract"]["contract_id"]}

SAM ID:
{item["contract"]["sam_id"]}

Title:
{item["contract"]["title"]}

Agency:
{item["contract"]["agency"]}

NAICS:
{item["contract"]["naics"]}

Retrieval Type:
{item["match_type"]}

Evidence:
{item["match"]["matched_text"]}
"""

            )


        return "\n\n".join(context)



    def generate(
        self,
        query,
        results
    ):


        context = self.build_context(
            results
        )


        prompt = f"""

You are an expert government procurement assistant.

Answer the user's question using ONLY the supplied contract information.

Rules:
- Do not invent vendors, agencies, or contract details.
- If the answer is not available, state that clearly.
- Cite the SAM ID when possible.


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



answer_generator = LLMAnswerGenerator()