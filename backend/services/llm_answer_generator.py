from openai import OpenAI


client = OpenAI()



class LLMAnswerGenerator:



    def normalize_contract(
        self,
        item
    ):
        """
        Converts retrieval results and selected contracts
        into a common structure.
        """

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




    def build_history(
        self,
        messages
    ):


        if not messages:

            return "No previous conversation history."



        history = []



        for msg in messages[-10:]:


            history.append(

f"""
{msg["role"].upper()}:

{msg["content"]}
"""

            )



        return "\n".join(history)





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



            citations.append({

                "sam_id":
                    sam_id,


                "title":
                    contract["title"],


                "agency":
                    contract["agency"],


                "url":
                    contract.get("url")

            })


        return citations





    def generate(
        self,
        query,
        results,
        selected_contracts=None,
        filters=None,
        conversation_history=None
    ):


        results = results or []


        selected_contracts = (
            selected_contracts
            or []
        )



        #
        # Selected contracts override search
        #

        if selected_contracts:

            context_results = selected_contracts


        else:

            context_results = results



        context = self.build_context(
            context_results
        )



        history = self.build_history(
            conversation_history
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

Use ONLY the supplied contract information.

Rules:

- Do not invent vendors, agencies, dates, values, or contract details.
- If information is unavailable, clearly state that.
- Always reference SAM IDs when discussing opportunities.
- When multiple contracts are provided, compare them when useful.
- Do not create citations. Citations are generated separately.



Conversation History:

{history}



{filter_context}



Contract Information:

{context}



Current User Question:

{query}



Athena Response:

"""



        response = client.responses.create(

            model="gpt-5",

            input=prompt

        )


        return response.output_text
    

    def stream_generate(
        self,
        query,
        results,
        selected_contracts=None,
        filters=None,
        conversation_history=None
    ):


        results = results or []


        selected_contracts = (
            selected_contracts
            or []
        )



        #
        # Selected contracts override search
        #

        if selected_contracts:

            context_results = selected_contracts


        else:

            context_results = results



        context = self.build_context(
            context_results
        )



        history = self.build_history(
            conversation_history
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

Use ONLY the supplied contract information.

Rules:

- Do not invent vendors, agencies, dates, values, or contract details.
- If information is unavailable, clearly state that.
- Always reference SAM IDs when discussing opportunities.
- When multiple contracts are provided, compare them when useful.
- Do not create citations. Citations are generated separately.



Conversation History:

{history}



{filter_context}



Contract Information:

{context}



Current User Question:

{query}



Athena Response:

"""



        stream = client.responses.create(

            model="gpt-5",

            input=prompt,

            stream=True

        )


        for event in stream:

            if event.type == "response.output_text.delta":

                yield event.delta





    def generate_with_citations(
        self,
        query,
        results,
        selected_contracts=None,
        filters=None,
        conversation_history=None
    ):



        answer = self.generate(

            query=query,

            results=results,

            selected_contracts=selected_contracts,

            filters=filters,

            conversation_history=conversation_history

        )



        citation_source = (

            selected_contracts

            if selected_contracts

            else results

        )



        citations = self.build_citations(
            citation_source
        )



        return {


            "answer":
                answer,


            "citations":
                citations

        }





answer_generator = LLMAnswerGenerator()