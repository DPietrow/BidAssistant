import time

from services.llm_answer_generator import answer_generator


class AthenaService:


    def chat(
        self,
        message,
        search_results=None,
        selected_contracts=None
    ):

        start = time.time()


        print(
            "Athena request started"
        )


        search_results = (
            search_results
            or []
        )


        selected_contracts = (
            selected_contracts
            or []
        )


        print(
            "Search results:",
            len(search_results)
        )


        print(
            "Selected contracts:",
            len(selected_contracts)
        )



        # ---------------------------------
        # Build Athena workspace context
        # ---------------------------------

        if selected_contracts:

            print(
                "Active contracts:"
            )

            for contract in selected_contracts:

                print(
                    "-",
                    contract.get("sam_id"),
                    contract.get("title")
                )



        # ---------------------------------
        # Determine what Athena should use
        # ---------------------------------

        context_results = search_results


        # If user selected contracts,
        # prioritize those over search results

        if selected_contracts:

            context_results = selected_contracts



        # ---------------------------------
        # Generate response
        # ---------------------------------

        if context_results:


            answer = answer_generator.generate(

                query=message,

                results=context_results,

                selected_contracts=selected_contracts

            )


            print(
                "LLM finished:",
                time.time() - start
            )


        else:


            answer = (

                "I don't have any contract opportunities "
                "in context yet. Try searching first, "
                "then ask me about the results."

            )



        return {


            "answer":
                answer,


            "citations":
                self.build_citations(
                    context_results
                ),


            "contracts":
                context_results

        }



    def build_citations(
        self,
        contracts
    ):

        citations = []


        for contract in contracts:


            # Handles both:
            # search result objects
            # direct contract objects

            if "contract" in contract:

                contract = contract["contract"]



            citations.append({

                "sam_id":
                    contract.get("sam_id"),


                "title":
                    contract.get("title"),


                "agency":
                    contract.get("agency"),


                "url":
                    contract.get("url")

            })


        return citations



athena_service = AthenaService()