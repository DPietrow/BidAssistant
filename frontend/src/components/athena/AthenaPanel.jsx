import { useRef, useState, useEffect } from "react";
import { Rnd } from "react-rnd";
import { Send, X } from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";


function AthenaPanel({

    onClose,

    searchResults,

    selectedContracts

}) {


    const [messages, setMessages] = useState([

        {
            role: "assistant",
            content:
                "Hello, I'm Athena. Select a contract or ask me about procurement opportunities."
        }

    ]);


    const [input, setInput] = useState("");

    const [sessionId, setSessionId] = useState(null);

    const lastContextRef = useRef(null);

    const messagesEndRef = useRef(null);



    /*
        Add context update message when contracts change
    */
    useEffect(() => {


        if (
            !selectedContracts ||
            selectedContracts.length === 0
        ) {

            return;

        }


        const contextKey =
            selectedContracts
                .map(c => c.sam_id)
                .join(",");



        if (
            lastContextRef.current === contextKey
        ) {

            return;

        }


        lastContextRef.current = contextKey;



        let message;



        if (selectedContracts.length === 1) {


            const contract = selectedContracts[0];


            message =
`Athena context updated.

Focused contract:

${contract.title}

Agency:
${contract.agency}

SAM ID:
${contract.sam_id}

Ask me to summarize the opportunity, analyze risks, or evaluate bid potential.`;


        }

        else {


            message =
`Athena context updated.

${selectedContracts.length} contracts selected.

I can compare these opportunities, analyze risks, identify the stronger bid candidate, or help prepare a proposal strategy.`;

        }



        setMessages(prev => [

            ...prev,

            {
                role: "assistant",
                content: message
            }

        ]);



    }, [selectedContracts]);





    /*
        Auto scroll
    */
    useEffect(() => {


        messagesEndRef.current?.scrollIntoView({

            behavior: "smooth"

        });


    }, [messages]);






    async function sendMessage() {


        if (!input.trim()) {

            return;

        }



        const userMessage = input;


        setInput("");



        /*
            Add user message
        */
        setMessages(prev => [

            ...prev,

            {
                role: "user",
                content: userMessage
            },

            {
                role: "assistant",
                content: "",
                thinking: true,
                streaming: false
            }

        ]);



        const assistantId =
            crypto.randomUUID();



        let completeText = "";



        try {


            const response = await fetch(

                "/athena/chat/stream",

                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json"

                    },

                    body: JSON.stringify({

                        session_id: sessionId,

                        message: userMessage,

                        context: {

                            searchResults:
                                searchResults?.results ?? [],


                            selectedContracts:
                                selectedContracts ?? []

                        }

                    })

                }

            );



            if (!response.ok) {


                throw new Error(

                    `Athena API error ${response.status}`

                );


            }




            const reader =
                response.body.getReader();



            const decoder =
                new TextDecoder();



            let buffer = "";




            /*
                Find the assistant placeholder index dynamically.

                This avoids stale indexes when state updates.
            */
            const getAssistantIndex = () => {


                let index = -1;


                setMessages(current => {


                    index =
                        current.length - 1;


                    return current;


                });


                return index;

            };




            while (true) {


                const {
                    done,
                    value
                } =
                    await reader.read();



                if (done) {

                    break;

                }



                buffer += decoder.decode(

                    value,

                    {
                        stream:true
                    }

                );



                const events =
                    buffer.split("\n\n");



                buffer =
                    events.pop();




                for (const event of events) {



                    if (!event.startsWith("data:")) {

                        continue;

                    }



                    const json =
                        JSON.parse(

                            event.replace(
                                "data:",
                                ""
                            )

                        );





                    /*
                        First token:
                        remove thinking state
                    */
                    if (json.type === "token") {


                        completeText += json.content;



                        setMessages(prev => {


                            const updated =
                                [...prev];


                            const index =
                                updated.length - 1;



                            updated[index] = {

                                ...updated[index],

                                content:
                                    completeText,


                                thinking:false,


                                streaming:true

                            };



                            return updated;


                        });



                    }






                    /*
                        Finished
                    */
                    if (json.type === "done") {


                        if (json.session_id) {


                            setSessionId(

                                json.session_id

                            );


                        }



                        setMessages(prev => {


                            const updated =
                                [...prev];


                            const index =
                                updated.length - 1;



                            updated[index] = {

                                ...updated[index],

                                streaming:false,

                                thinking:false

                            };



                            return updated;


                        });



                    }





                    /*
                        Backend error
                    */
                    if (json.type === "error") {


                        setMessages(prev => {


                            const updated =
                                [...prev];


                            const index =
                                updated.length - 1;



                            updated[index] = {

                                role:"assistant",

                                content:
                                    json.content,


                                streaming:false,

                                thinking:false

                            };



                            return updated;


                        });


                    }


                }


            }



        }


        catch(error) {


            console.error(

                "Athena streaming error:",
                error

            );



            setMessages(prev => {


                const updated =
                    [...prev];



                const index =
                    updated.length - 1;



                updated[index] = {


                    role:"assistant",


                    content:
                    "I encountered an error processing that request.",


                    thinking:false,

                    streaming:false


                };



                return updated;


            });


        }


    }
    
    return (

        <Rnd

            default={{

                x:
                    window.innerWidth - 450,

                y:120,

                width:420,

                height:550

            }}


            minWidth={320}

            minHeight={350}

            bounds="window"

            dragHandleClassName="athena-drag-handle"


            style={{

                zIndex:1000

            }}

        >


            <div

                style={{

                    height:"100%",

                    background:"white",

                    borderRadius:"16px",

                    boxShadow:
                    "0 8px 30px rgba(0,0,0,.25)",

                    display:"flex",

                    flexDirection:"column",

                    overflow:"hidden"

                }}

            >



                {/* Header */}

                <div

                    className="athena-drag-handle"

                    style={{

                        background:"#111827",

                        color:"white",

                        padding:"14px 18px",

                        display:"flex",

                        justifyContent:"space-between",

                        alignItems:"center",

                        cursor:"move"

                    }}

                >


                    <div>


                        <strong>
                            Athena Assistant
                        </strong>


                        <div

                            style={{

                                fontSize:"12px",

                                opacity:.8,

                                marginTop:"3px"

                            }}

                        >

                            {

                                selectedContracts?.length

                                ?

                                `${selectedContracts.length} contract${selectedContracts.length > 1 ? "s" : ""} selected`

                                :

                                "No contracts selected"

                            }


                        </div>


                    </div>



                    <button

                        onClick={onClose}

                        style={{

                            background:"transparent",

                            border:"none",

                            color:"white",

                            cursor:"pointer"

                        }}

                    >

                        <X size={18}/>


                    </button>


                </div>






                {/* Messages */}

                <div

                    style={{

                        flex:1,

                        padding:"15px",

                        overflowY:"auto",

                        background:"#f9fafb",

                        userSelect:"text"

                    }}

                >


                    {

                        messages.map((msg,index)=>(


                            <div

                                key={index}

                                style={{

                                    marginBottom:"12px",

                                    textAlign:

                                        msg.role === "user"

                                        ?

                                        "right"

                                        :

                                        "left"

                                }}

                            >



                                <div

                                    style={{

                                        display:"inline-block",

                                        maxWidth:"90%",

                                        padding:"10px 14px",

                                        borderRadius:"12px",

                                        background:

                                            msg.role === "user"

                                            ?

                                            "#2563eb"

                                            :

                                            "#e5e7eb",

                                        color:

                                            msg.role === "user"

                                            ?

                                            "white"

                                            :

                                            "#111827"

                                    }}

                                >



                                    {

                                        msg.thinking

                                        ?

                                        (

                                            <div

                                                style={{

                                                    display:"flex",

                                                    alignItems:"center",

                                                    gap:"10px",

                                                    color:"#6b7280",

                                                    fontSize:"14px"

                                                }}

                                            >


                                                <div className="athena-thinking-dots">

                                                    <span></span>

                                                    <span></span>

                                                    <span></span>

                                                </div>


                                                <span>
                                                    Athena is analyzing opportunities...
                                                </span>


                                            </div>

                                        )


                                        :


                                        (

                                            <div className="athena-markdown">


                                                <ReactMarkdown

                                                    remarkPlugins={[remarkGfm]}

                                                >

                                                    {msg.content}

                                                </ReactMarkdown>


                                                {


                                                    msg.streaming

                                                    &&

                                                    (

                                                        <span

                                                            className="athena-cursor"

                                                        >

                                                            ▌

                                                        </span>

                                                    )


                                                }


                                            </div>

                                        )

                                    }



                                </div>



                            </div>


                        ))

                    }



                    <div ref={messagesEndRef}/>


                </div>






                {/* Input */}

                <div

                    style={{

                        display:"flex",

                        padding:"12px",

                        borderTop:
                        "1px solid #ddd"

                    }}

                >


                    <input

                        value={input}

                        onChange={

                            e => setInput(e.target.value)

                        }


                        onKeyDown={

                            e => {

                                if(
                                    e.key === "Enter"
                                ) {

                                    sendMessage();

                                }

                            }

                        }


                        placeholder="Ask Athena..."


                        style={{

                            flex:1,

                            padding:"10px",

                            borderRadius:"8px",

                            border:
                            "1px solid #ccc"

                        }}


                    />



                    <button

                        onClick={sendMessage}

                        style={{

                            marginLeft:"8px",

                            width:"42px",

                            border:"none",

                            borderRadius:"8px",

                            background:"#111827",

                            color:"white",

                            cursor:"pointer"

                        }}

                    >

                        <Send size={18}/>

                    </button>


                </div>



            </div>


        </Rnd>

    );


}


export default AthenaPanel;