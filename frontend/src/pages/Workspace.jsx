import { theme } from "../theme";

import { useRef, useState } from "react";


function Workspace({ project, onBack, onSaveProject }) {


    const fileInputRef = useRef(null);

    const [hasSaved, setHasSaved] = useState(
        project.saved ?? false
    );


    const [dragging, setDragging] = useState(false);


    const [uploadedFiles, setUploadedFiles] = useState([]);


    const [chatMessage, setChatMessage] = useState("");


    const [messages, setMessages] = useState([]);

    const [showSavedModal, setShowSavedModal] = useState(false);

    const [editingName, setEditingName] = useState(false);

    const [projectName, setProjectName] = useState(
        project.name || "Untitled Project"
    );



    function handleFiles(files) {


        const newFiles = Array.from(files).map(file => ({

            id: crypto.randomUUID(),

            name: file.name,

            size: file.size,

            status: "Uploading..."

        }));


        setUploadedFiles(prev => [

            ...prev,

            ...newFiles

        ]);



        newFiles.forEach(file => {


            const stages = [

                {
                    delay:1200,
                    status:"Extracting text..."
                },

                {
                    delay:2400,
                    status:"Building embeddings..."
                },

                {
                    delay:3600,
                    status:"Ready for Athena"
                }

            ];



            stages.forEach(stage => {


                setTimeout(()=>{


                    setUploadedFiles(prev =>

                        prev.map(f =>

                            f.id === file.id

                            ?

                            {
                                ...f,
                                status:stage.status
                            }

                            :

                            f

                        )

                    );


                }, stage.delay);


            });


        });


    }



    const athenaReady = uploadedFiles.some(

        file => file.status === "Ready for Athena"

    );




    function sendMessage(){


        if(!chatMessage.trim() || !athenaReady)

            return;



        const userMessage = {


            role:"user",

            content:chatMessage


        };


        setMessages(prev => [

            ...prev,

            userMessage

        ]);



        setChatMessage("");



        // Fake Athena response


        setTimeout(()=>{


            setMessages(prev => [


                ...prev,


                {

                    role:"athena",

                    content:
                    "I've analyzed the uploaded documents. I can help summarize requirements, identify risks, compare costs, and draft proposal content."

                }


            ]);



        },1000);


    }




    return (


        <div

            style={{

                maxWidth:"1450px",

                margin:"0 auto"

            }}

        >


            <input

                ref={fileInputRef}

                type="file"

                multiple

                accept=".pdf,.doc,.docx,.xlsx,.xls,.csv"

                style={{display:"none"}}

                onChange={(e)=>handleFiles(e.target.files)}

            />




            {/* Header */}


           <div
                style={{
                    display:"grid",
                    gridTemplateColumns:"1fr auto 1fr",
                    alignItems:"center",
                    marginBottom:36
                }}
            >
            
            
                {/* Left */}
            
                <div>
            
                <button

                    onClick={()=>{


                        const isEmptyProject =

                            projectName === "Untitled Project" &&

                            uploadedFiles.length === 0;



                        if(!hasSaved && !isEmptyProject){
                        
                        
                            const confirmExit = window.confirm(
                            
                                "Are you sure you want to exit this page without saving?"
                            
                            );
                        
                        
                            if(confirmExit){
                            
                                onBack();
                            
                            }
                        
                        
                        }
                    
                        else{
                        
                            onBack();
                        
                        }
                    
                    
                    }}
                
                >
                    
                        ← Projects
                    
                    </button>
                    
                </div>
                    
                    
                    
                    
                {/* Center Project Title */}

                <div
                    style={{
                        display:"flex",
                        alignItems:"center",
                        justifyContent:"center",
                        gap:12
                    }}
                >
                
                
                {
                editingName
                
                ?
                
                <input
                
                    autoFocus
                
                    value={projectName}
                
                    onChange={(e)=>setProjectName(e.target.value)}
                
                    onBlur={()=>setEditingName(false)}
                
                    onKeyDown={(e)=>{
                    
                        if(e.key==="Enter"){
                        
                            setEditingName(false);
                        
                        }
                    
                    }}
                
                    style={{
                    
                        color:theme.text,
                    
                        fontSize:32,
                    
                        fontWeight:700,
                    
                        border:`1px solid ${theme.primary}`,
                    
                        borderRadius:8,
                    
                        padding:"4px 12px",
                    
                        background:"white",
                    
                        textAlign:"center",
                    
                        outline:"none",
                    
                        width:450
                    
                    }}
                
                />
                
                
                :
                
                <>

                <h1

                    style={{
                    
                        color:theme.text,
                    
                        margin:0,
                    
                        fontSize:32,
                    
                        fontWeight:700
                    
                    }}
                
                >
                
                    {projectName}
                
                </h1>
                
                
                <button

                    onClick={()=>setEditingName(true)}
                
                    title="Rename project"
                
                    style={{
                    
                        background:"transparent",
                    
                        border:"none",
                    
                        cursor:"pointer",
                    
                        color:theme.mutedText,
                    
                        fontSize:18,
                    
                        padding:"4px 8px"
                    
                    }}
                
                >
                
                    ✏️
                
                </button>
                
                </>

                
                }


                </div>

                
                
                
                {/* Right */}
                
                <div
                    style={{
                        display:"flex",
                        justifyContent:"flex-end"
                    }}
                >
                
                    <button

                          onClick={()=>{

                            const savedProject = {
                            
                                ...project,
                            
                                name:projectName,
                            
                                updated:"Just now",
                            
                                saved:true
                            
                            };
                        
                        
                            onSaveProject(savedProject);
                        
                        
                            setHasSaved(true);
                        
                        
                            setShowSavedModal(true);
                        
                        }}
                    
                        style={{
                        
                            background:theme.primary,
                        
                            color:"white",
                        
                            border:"none",
                        
                            borderRadius:10,
                        
                            padding:"12px 26px",
                        
                            cursor:"pointer",
                        
                            fontWeight:600,
                        
                            fontSize:15
                        
                        }}
                    
                    >
                    
                        Save Project
                    
                    </button>
                    
                </div>
                    
                    
            </div>





            <div

                style={{

                    display:"grid",

                    gridTemplateColumns:"1fr 1fr",

                    gap:28

                }}

            >



                {/* Documents */}


                <div

                    style={{

                        background:theme.panel,

                        borderRadius:16,

                        padding:36,

                        boxShadow:theme.shadow

                    }}

                >


                    <h2 style={{color:theme.text}}>

                        Documents

                    </h2>



                    <div

                        onDragEnter={(e)=>{

                            e.preventDefault();

                            setDragging(true);

                        }}


                        onDragOver={(e)=>{

                            e.preventDefault();

                            setDragging(true);

                        }}


                        onDragLeave={()=>setDragging(false)}


                        onDrop={(e)=>{

                            e.preventDefault();

                            setDragging(false);

                            handleFiles(e.dataTransfer.files);

                        }}


                        style={{

                            marginTop:30,

                            border:`2px dashed ${
                                dragging
                                ?
                                theme.primary
                                :
                                theme.border
                            }`,

                            borderRadius:16,

                            padding:40,

                            background:

                                dragging

                                ?

                                "#eff6ff"

                                :

                                "transparent"

                        }}

                    >



                    {

                        uploadedFiles.length === 0

                        ?

                        <div style={{textAlign:"center"}}>


                            <div style={{fontSize:52}}>

                                ☁

                            </div>


                            <h3 style={{color:theme.text}}>

                                {

                                    dragging

                                    ?

                                    "Release to upload"

                                    :

                                    "Drop files here"

                                }

                            </h3>


                            <p style={{color:theme.mutedText}}>

                                or browse from your computer

                            </p>


                            <button

                                onClick={()=>fileInputRef.current?.click()}

                                style={{

                                    marginTop:20,

                                    background:theme.primary,

                                    color:"white",

                                    border:"none",

                                    borderRadius:10,

                                    padding:"12px 22px",

                                    cursor:"pointer"

                                }}

                            >

                                Browse Files

                            </button>


                        </div>


                        :


                        <div>


                            {

                                uploadedFiles.map(file=>(


                                    <div

                                        key={file.id}

                                        style={{

                                            display:"flex",

                                            justifyContent:"space-between",

                                            padding:14,

                                            marginBottom:12,

                                            border:`1px solid ${theme.border}`,

                                            borderRadius:10

                                        }}

                                    >

                                        <span style={{color:theme.text}}>

                                            📄 {file.name}

                                        </span>


                                        <span

                                            style={{

                                                color:

                                                file.status==="Ready for Athena"

                                                ?

                                                "#16a34a"

                                                :

                                                "#d97706"

                                            }}

                                        >

                                            {file.status}

                                        </span>


                                    </div>


                                ))

                            }



                            <button

                                onClick={()=>fileInputRef.current?.click()}

                                style={{

                                    marginTop:10,

                                    color: theme.text,

                                    background:"transparent",

                                    border:`1px solid ${theme.border}`,

                                    borderRadius:8,

                                    padding:"10px 18px",

                                    cursor:"pointer"

                                }}

                            >

                                + Add More Files

                            </button>


                        </div>


                    }


                    </div>


                </div>





                {/* Athena */}


                <div

                    style={{

                        background:theme.panel,

                        borderRadius:16,

                        padding:36,

                        boxShadow:theme.shadow

                    }}

                >


                    <h2 style={{color:theme.text}}>

                        Athena

                    </h2>



                    <div

                        style={{

                            marginTop:20,

                            height:260,

                            overflowY:"auto"

                        }}

                    >


                        {

                            messages.length === 0 &&

                            <p style={{color:theme.mutedText}}>

                                Upload documents to begin analyzing this project.

                            </p>

                        }



                        {

                            messages.map((message,index)=>(


                                <div

                                    key={index}

                                    style={{

                                        marginBottom:16,

                                        padding:14,

                                        borderRadius:12,

                                        background:

                                            message.role==="athena"

                                            ?

                                            "#f8fafc"

                                            :

                                            "#eff6ff"

                                    }}

                                >

                                    <strong>

                                        {

                                            message.role==="athena"

                                            ?

                                            "Athena"

                                            :

                                            "You"

                                        }

                                    </strong>

                                    <p>

                                        {message.content}

                                    </p>


                                </div>


                            ))

                        }


                    </div>




                    <div

                        style={{

                            marginTop:20,

                            display:"flex",

                            gap:10

                        }}

                    >


                        <input

                            value={chatMessage}

                            onChange={(e)=>setChatMessage(e.target.value)}

                            onKeyDown={(e)=>{

                                    if(
                                        e.key === "Enter" &&
                                        !e.shiftKey
                                    ){
                                    
                                        e.preventDefault();
                                    
                                        sendMessage();
                                    
                                    }
                                
                            }}

                            disabled={!athenaReady}

                            placeholder={

                                athenaReady

                                ?

                                "Ask Athena about this project..."

                                :

                                uploadedFiles.length

                                ?

                                "Athena is preparing your documents..."

                                :

                                "Upload documents to begin chatting..."

                            }


                            style={{

                                flex:1,

                                padding:14,

                                borderRadius:10,

                                border:`1px solid ${theme.border}`,

                                background:

                                    athenaReady

                                    ?

                                    "white"

                                    :

                                    theme.background,
                                
                                color: theme.text,

                                caretColor: theme.text,

                                outline:"none"

                            }}

                        />


                        <button

                            onClick={sendMessage}

                            disabled={!athenaReady}

                            style={{

                                background:

                                    athenaReady

                                    ?

                                    theme.primary

                                    :

                                    theme.border,

                                color:"white",

                                border:"none",

                                borderRadius:10,

                                padding:"0 22px",

                                cursor:

                                    athenaReady

                                    ?

                                    "pointer"

                                    :

                                    "not-allowed"

                            }}

                        >

                            Send

                        </button>


                    </div>


                </div>


            </div>

 {/* Save Confirmation Modal */}

            {
                showSavedModal &&

                <div

                    style={{

                        position:"fixed",

                        inset:0,

                        background:"rgba(15,23,42,.45)",

                        display:"flex",

                        justifyContent:"center",

                        alignItems:"center",

                        zIndex:5000

                    }}

                >


                    <div

                        style={{

                            width:420,

                            background:"white",

                            borderRadius:16,

                            padding:32,

                            boxShadow:theme.shadow,

                            textAlign:"center"

                        }}

                    >


                        <div

                            style={{

                                fontSize:48,

                                marginBottom:16

                            }}

                        >

                            ✅

                        </div>



                        <h2

                            style={{

                                color:theme.text,

                                marginTop:0

                            }}

                        >

                            Project Saved

                        </h2>



                        <p

                            style={{

                                color:theme.mutedText,

                                lineHeight:1.6

                            }}

                        >

                            Your project has been saved successfully.

                            You can safely leave this workspace.

                        </p>



                        <button

                            onClick={()=>setShowSavedModal(false)}

                            style={{

                                marginTop:24,

                                background:theme.primary,

                                color:"white",

                                border:"none",

                                borderRadius:10,

                                padding:"12px 24px",

                                cursor:"pointer",

                                fontWeight:600

                            }}

                        >

                            Continue

                        </button>


                    </div>


                </div>

            }

        </div>

    );

}


export default Workspace;