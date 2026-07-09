import time

from services.llm_answer_generator import answer_generator


class AthenaService:


    def chat(
        self,
        message,
        search_results
    ):
        start = time.time()

        print(
            "Athena request started"
        )


        print(
            "Contracts:",
            len(search_results)
            if search_results
            else 0
        )


        if search_results:

            answer = answer_generator.generate(
                query=message,
                results=search_results
            )

            print(
                "LLM finished:",
                time.time() - start
            )

        else:

            answer = (
                "I don't see any contracts selected. "
                "Try searching for opportunities first."
            )


        return {

            "answer":answer,

            "citations":[],

            "contracts":search_results

        }


athena_service = AthenaService()