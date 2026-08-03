import { useState } from "react";
import { theme } from "../theme";


function Projects({

    projects,

    onCreateProject,

    onOpenProject,

    onDeleteProject

}) {


    const [deleteTarget, setDeleteTarget] = useState(null);



    function confirmDelete(){

        if(deleteTarget){

            onDeleteProject(deleteTarget.id);

            setDeleteTarget(null);

        }

    }



    return (

        <div

            style={{

                maxWidth:"1400px",

                margin:"0 auto",

                paddingBottom:40

            }}

        >


            {/* Header */}

            <div

                style={{

                    marginBottom:48

                }}

            >

                <h1

                    style={{

                        color:theme.text,

                        margin:"0 0 16px",

                        fontSize:"42px",

                        fontWeight:700,

                        letterSpacing:"-1px"

                    }}

                >

                    Projects

                </h1>


                <p

                    style={{

                        color:theme.mutedText,

                        fontSize:18,

                        maxWidth:700,

                        lineHeight:1.6

                    }}

                >

                    Organize contracts, pricing sheets and proposals into dedicated Athena workspaces.

                </p>


            </div>





            {/* Create Project Panel */}


            <div

                style={{


                    background:theme.panel,

                    borderRadius:16,

                    padding:30,

                    marginBottom:36,

                    display:"flex",

                    justifyContent:"space-between",

                    alignItems:"center",

                    boxShadow:theme.shadow


                }}

            >


                <div>


                    <h2

                        style={{

                            color:theme.text,

                            margin:"0 0 8px"

                        }}

                    >

                        Start a New Project

                    </h2>


                    <p

                        style={{

                            color:theme.mutedText,

                            margin:0

                        }}

                    >

                        Upload documents and let Athena build an AI workspace.

                    </p>


                </div>



                <button

                    onClick={onCreateProject}

                    style={{

                        background:theme.primary,

                        color:"white",

                        border:"none",

                        borderRadius:10,

                        padding:"14px 24px",

                        cursor:"pointer",

                        fontWeight:600,

                        fontSize:15

                    }}

                >

                    + New Project

                </button>


            </div>







            {/* Project Cards */}


            <div

                style={{

                    display:"grid",

                    gridTemplateColumns:
                        "repeat(auto-fill,minmax(360px,1fr))",

                    gap:24

                }}

            >


                {

                    projects.map(project => (


                        <div

                            key={project.id}

                            style={{

                                background:theme.panel,

                                borderRadius:16,

                                padding:28,

                                boxShadow:theme.shadow,

                                transition:"0.2s"

                            }}

                        >


                            <div

                                onClick={()=>onOpenProject(project)}

                                style={{

                                    cursor:"pointer"

                                }}

                            >


                                <h3

                                    style={{

                                        color:theme.text,

                                        marginTop:0,

                                        marginBottom:12,

                                        fontSize:22

                                    }}

                                >

                                    {project.name}

                                </h3>



                                <p

                                    style={{

                                        color:theme.mutedText,

                                        lineHeight:1.6,

                                        minHeight:50,

                                        marginBottom:20

                                    }}

                                >

                                    {project.description}

                                </p>


                            </div>




                            <div

                                style={{

                                    display:"flex",

                                    justifyContent:"space-between",

                                    alignItems:"center"

                                }}

                            >


                                <span

                                    style={{

                                        color:theme.mutedText

                                    }}

                                >

                                    {project.documents} Documents

                                </span>



                                <div

                                    style={{

                                        display:"flex",

                                        alignItems:"center",

                                        gap:12

                                    }}

                                >


                                    <button

                                        onClick={()=>setDeleteTarget(project)}

                                        style={{

                                            background:"transparent",

                                            color:"#dc2626",

                                            border:"1px solid #fecaca",

                                            borderRadius:8,

                                            padding:"8px 14px",

                                            cursor:"pointer",

                                            fontWeight:600

                                        }}

                                    >

                                        Delete

                                    </button>



                                    <button

                                        onClick={()=>onOpenProject(project)}

                                        style={{

                                            background:"transparent",

                                            border:"none",

                                            color:theme.primary,

                                            cursor:"pointer",

                                            fontWeight:600,

                                            fontSize:15

                                        }}

                                    >

                                        Open →

                                    </button>


                                </div>


                            </div>



                        </div>


                    ))

                }


            </div>







            {/* Delete Confirmation Modal */}


            {

                deleteTarget &&

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

                            boxShadow:theme.shadow

                        }}

                    >


                        <h2

                            style={{

                                color:theme.text,

                                marginTop:0

                            }}

                        >

                            Delete Project?

                        </h2>



                        <p

                            style={{

                                color:theme.mutedText,

                                lineHeight:1.6

                            }}

                        >

                            Are you sure you want to delete

                            <strong> {deleteTarget.name}</strong>?

                            This action cannot be undone.

                        </p>




                        <div

                            style={{

                                display:"flex",

                                justifyContent:"flex-end",

                                gap:12,

                                marginTop:28

                            }}

                        >


                            <button

                                onClick={()=>setDeleteTarget(null)}

                                style={{

                                    border:`1px solid ${theme.border}`,

                                    borderRadius:8,

                                    padding:"10px 18px",

                                    cursor:"pointer"

                                }}

                            >

                                Cancel

                            </button>



                            <button

                                onClick={confirmDelete}

                                style={{

                                    background:"#dc2626",

                                    color:"white",

                                    border:"none",

                                    borderRadius:8,

                                    padding:"10px 18px",

                                    cursor:"pointer",

                                    fontWeight:600

                                }}

                            >

                                Delete Project

                            </button>


                        </div>


                    </div>


                </div>

            }


        </div>

    );

}


export default Projects;