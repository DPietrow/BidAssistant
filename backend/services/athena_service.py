import time
import json

from services.llm_answer_generator import answer_generator
from services.athena_memory import memory


class AthenaService:


    def _build_context_results(
        self,
        search_results,
        selected_contracts
    ):

        search_results = search_results or []

        selected_contracts = selected_contracts or []


        #
        # Selected contracts always override search
        #

        if selected_contracts:

            return [

                {
                    "contract": contract,

                    "match_type":
                        "selected_contract",

                    "match": {

                        "matched_text":
                            "User selected contract"

                    }

                }

                for contract in selected_contracts

            ]


        return search_results



    def chat(
        self,
        session_id,
        message,
        search_results=None,
        selected_contracts=None
    ):

        start = time.time()


        context_results = self._prepare_request(
            session_id,
            search_results,
            selected_contracts
        )


        session = memory.get_session(
            session_id
        )



        if not context_results:

            return {

                "answer":
                    "I don't have any contract opportunities in context yet. Try searching first.",

                "citations": [],

                "contracts": []

            }



        answer = answer_generator.generate(

            query=message,

            results=context_results,

            selected_contracts=selected_contracts,

            conversation_history=session["messages"]

        )


        memory.add_message(
            session_id,
            "user",
            message
        )


        memory.add_message(
            session_id,
            "assistant",
            answer
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



    def stream_chat(
        self,
        session_id,
        message,
        search_results=None,
        selected_contracts=None
    ):

        start = time.time()



        context_results = self._prepare_request(
            session_id,
            search_results,
            selected_contracts
        )


        session = memory.get_session(
            session_id
        )



        if not context_results:

            yield {

                "type":
                    "token",

                "content":
                    "I don't have any contract opportunities in context yet. Try searching first."

            }


            yield {

                "type":"done",
            
                "session_id":session_id,
            
                "citations":
                    self.build_citations(context_results),
            
                "contracts":
                    [
                        item["contract"]
                        for item in context_results
                    ]
            
            }

            return




        full_answer = ""



        for chunk in answer_generator.stream_generate(

            query=message,

            results=context_results,

            selected_contracts=selected_contracts,

            conversation_history=session["messages"]

        ):


            full_answer += chunk


            yield {

                "type":
                    "token",

                "content":
                    chunk

            }



        memory.add_message(
            session_id,
            "user",
            message
        )


        memory.add_message(
            session_id,
            "assistant",
            full_answer
        )



        print(
            "LLM streaming finished:",
            time.time() - start
        )



        yield {


            "type":
                "done",


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




    def _prepare_request(
        self,
        session_id,
        search_results,
        selected_contracts
    ):


        search_results = search_results or []

        selected_contracts = selected_contracts or []



        memory.update_context(

            session_id,

            selected_contracts,

            search_results

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



        return self._build_context_results(

            search_results,

            selected_contracts

        )



    def build_citations(
        self,
        results
    ):


        citations = []

        seen = set()



        for item in results:


            contract = item["contract"]


            sam_id = contract.get(
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