import uuid


class AthenaMemory:


    def __init__(self):

        self.sessions = {}



    def create_session(self):

        session_id = str(uuid.uuid4())

        self.sessions[session_id] = {

            "messages": [],

            "selected_contracts": [],

            "search_results": []

        }

        return session_id



    def get_session(
        self,
        session_id
    ):

        if session_id not in self.sessions:

            self.sessions[session_id] = {

                "messages": [],

                "selected_contracts": [],

                "search_results": []

            }


        return self.sessions[session_id]



    def add_message(
        self,
        session_id,
        role,
        content
    ):

        session = self.get_session(
            session_id
        )


        session["messages"].append({

            "role": role,

            "content": content

        })



    def update_context(
        self,
        session_id,
        selected_contracts=None,
        search_results=None
    ):

        session = self.get_session(
            session_id
        )


        if selected_contracts is not None:

            session["selected_contracts"] = selected_contracts



        if search_results is not None:

            session["search_results"] = search_results



memory = AthenaMemory()