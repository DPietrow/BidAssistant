import {
    theme
} from "../../theme";

import { useState } from "react";
import { Rnd } from "react-rnd";
import { Send, X } from "lucide-react";


function AthenaPanel({
    onClose,
    searchResults
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



    async function sendMessage(){

            if(!input.trim())
        return;


    const currentMessage = input;


    const userMessage = {
        role:"user",
        content:currentMessage
    };


    setMessages(prev => [
        ...prev,
        userMessage
    ]);


    setInput("");

    setLoading(true);


    try {


        const response = await fetch(
            "/athena/chat",
            {
                method:"POST",

                headers:{
                    "Content-Type":"application/json"
                },

                body:JSON.stringify({

                    message: currentMessage,

                    context:{
                        searchResults:
                            searchResults?.results ?? []
                    }

                })
            }
        );



        if(!response.ok){

            throw new Error(
                `Athena API error: ${response.status}`
            );

        }



        const data = await response.json();



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
                x:window.innerWidth - 450,
                y:120,
                width:420,
                height:550
            }}


            minWidth={320}
            minHeight={350}


            bounds="window"


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

                    <strong>
                        Athena Assistant
                    </strong>


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

                        background:"#f9fafb"

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
                                    ?"right"
                                    :"left"

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

                        ))
                    }


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

                            border:"none",

                            background:"#111827",

                            color:"white",

                            borderRadius:"8px",

                            width:"42px",

                            cursor:"pointer"

                        }}

                    >

                        <Send size={18}/>

                    </button>


                </div>


            </div>


        </Rnd>

    )

}


export default AthenaPanel;