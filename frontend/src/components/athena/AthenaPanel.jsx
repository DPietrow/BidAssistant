import { useRef, useState, useEffect } from "react";
import { Rnd } from "react-rnd";
import { Send, X } from "lucide-react";


function AthenaPanel({

    onClose,

    searchResults,

    selectedContracts

}) {


    const [messages,setMessages] = useState([

        {
            role:"assistant",
            content:
            "Hello, I'm Athena. Select a contract or ask me about procurement opportunities."
        }

    ]);



    const [input,setInput] = useState("");

    const [loading,setLoading] = useState(false);

    const [sessionId,setSessionId] = useState(null);

    const lastContextRef = useRef(null);



    useEffect(() => {


        if(
            !selectedContracts ||
            selectedContracts.length === 0
        ){

            return;

        }



        const contextKey =
            selectedContracts
            .map(c => c.sam_id)
            .join(",");



        if(
            lastContextRef.current === contextKey
        ){

            return;

        }



        lastContextRef.current = contextKey;



        let message;



        if(selectedContracts.length === 1){


            const contract =
                selectedContracts[0];



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
                role:"assistant",
                content:message
            }

        ]);



    },[selectedContracts]);





    async function sendMessage(){


        if(!input.trim())
            return;



        const currentMessage =
            input;



        setMessages(prev => [

            ...prev,

            {
                role:"user",
                content:currentMessage
            }

        ]);



        setInput("");

        setLoading(true);



        try {


            const response =
                await fetch(

                    "/athena/chat",

                    {

                        method:"POST",

                        headers:{

                            "Content-Type":
                            "application/json"

                        },


                        body:JSON.stringify({

                            session_id: sessionId,

                            message:
                                currentMessage,


                            context:{


                                searchResults:
                                    searchResults?.results ?? [],



                                selectedContracts:
                                    selectedContracts ?? []

                            }


                        })

                    }

                );



            if(!response.ok){

                throw new Error(
                    `Athena API error ${response.status}`
                );

            }



            const data =
                await response.json();

            if(data.session_id){

                setSessionId(
                    data.session_id
                );
            
            }

            setMessages(prev => [

                ...prev,

                {

                    role:"assistant",

                    content:
                        data.answer ??
                        "I could not generate a response."

                }

            ]);



        }


        catch(error){


            console.error(
                "Athena error:",
                error
            );


            setMessages(prev => [

                ...prev,

                {

                    role:"assistant",

                    content:
                    "I encountered an error processing that request."

                }

            ]);


        }


        setLoading(false);


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

                    messages.map(

                        (msg,index)=>(


                        <div

                            key={index}

                            style={{

                                marginBottom:"12px",

                                textAlign:
                                msg.role==="user"
                                ?
                                "right"
                                :
                                "left"

                            }}

                        >


                            <span

                                style={{

                                    display:"inline-block",

                                    padding:"10px 14px",

                                    borderRadius:"12px",

                                    background:
                                    msg.role==="user"
                                    ?
                                    "#2563eb"
                                    :
                                    "#e5e7eb",

                                    color:
                                    msg.role==="user"
                                    ?
                                    "white"
                                    :
                                    "#111827"

                                }}

                            >

                                {msg.content}

                            </span>


                        </div>


                    ))}


                    {

                    loading &&

                    <p>
                        Athena is thinking...
                    </p>

                    }


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
                            e=>setInput(e.target.value)
                        }


                        onKeyDown={

                            e=>{

                                if(e.key==="Enter")

                                    sendMessage();

                            }

                        }


                        placeholder="Ask Athena..."


                        style={{

                            flex:1,

                            padding:"10px",

                            borderRadius:"8px",

                            border:"1px solid #ccc"

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