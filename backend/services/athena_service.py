import time

from services.llm_answer_generator import answer_generator
from services.athena_memory import memory

class AthenaService:


    def chat(
        self,
        session_id,
        message,
        search_results=None,
        selected_contracts=None
    ):

        start = time.time()


        search_results = search_results or []

        selected_contracts = selected_contracts or []

        memory.update_context(

            session_id,

            selected_contracts,

            search_results

        )

        session = memory.get_session(
            session_id
        )

        print(
            "Athena request started"
        )


        print(
            "Search results:",
            len(search_results)
        )


        print(
            "Selected:",
            len(selected_contracts)
        )



        # --------------------------------
        # Selected contracts take priority
        # --------------------------------

        if selected_contracts:


            context_results = [

                {
                    "contract": contract,

                    "match_type":
                        "selected_contract",

                    "match":{

                        "matched_text":
                        "User selected contract"

                    }

                }

                for contract in selected_contracts

            ]


        else:


            context_results = search_results




        if not context_results:


            return {


                "answer":
                "I don't have any contract opportunities in context yet. Try searching first.",


                "citations":[],

                "contracts":[]

            }





        answer = answer_generator.generate(


            query=message,


            results=context_results,

            selected_contracts=selected_contracts,


            conversation_history=session["messages"]


        )



        print(

            "LLM finished:",

            time.time() - start

        )




        return {


            "answer":
                answer,


            "citations":
                self.build_citations(
                    context_results
                ),


            "contracts":
                [

                    item["contract"]

                    for item in context_results

                ]

        }





    def build_citations(
        self,
        results
    ):


        citations=[]


        seen=set()



        for item in results:


            contract=item["contract"]


            sam_id=contract.get(
                "sam_id"
            )


            if sam_id in seen:

                continue


            seen.add(
                sam_id
            )


            citations.append({

                "sam_id":
                    sam_id,

                "title":
                    contract.get("title"),

                "agency":
                    contract.get("agency"),

                "url":
                    contract.get("url")

            })


        return citations





athena_service = AthenaService()