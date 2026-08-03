import { useState } from "react";

import Navbar from "../components/navigation/Navbar";

import OpportunitiesPage from "../components/opportunities/OpportunitiesPage";
import Projects from "./Projects";
import Workspace from "./Workspace";

import { theme } from "../theme";


function Dashboard() {


    const [activePage, setActivePage] = useState(()=>{

        return localStorage.getItem("athena_active_page")
            ||
            "opportunities";

    });


    const [selectedProject, setSelectedProject] = useState(null);



    // Temporary project database
    // Later this becomes your backend/database

    const defaultProjects = [
    
        {
            id:1,
            name:"VA Medical Center HVAC",
            description:
                "Preventive maintenance and HVAC modernization proposal.",
            documents:3,
            updated:"2 hours ago"
        },
    
        {
            id:2,
            name:"NASA Facilities Support",
            description:
                "Operations and maintenance services for NASA facilities.",
            documents:5,
            updated:"Yesterday"
        },
    
        {
            id:3,
            name:"Army Barracks Renovation",
            description:
                "Renovation and facility improvement proposal.",
            documents:2,
            updated:"Last week"
        }
    
    ];
    
    
    
    const [projects, setProjects] = useState(()=>{
    
        const saved = localStorage.getItem("athena_projects");
    
    
        return saved
    
            ?
    
            JSON.parse(saved)
    
            :
    
            defaultProjects;
    
    });


    function persistProjects(updatedProjects){

        setProjects(updatedProjects);

        localStorage.setItem(
            "athena_projects",
            JSON.stringify(updatedProjects)
        );

    }

    function navigate(page){

        setActivePage(page);

        localStorage.setItem(
            "athena_active_page",
            page
        );


        if(page !== "projects"){

            setSelectedProject(null);

        }

    }


    function createProject(){


        const newProject = {

            id:crypto.randomUUID(),

            name:"Untitled Project",

            description:
                "New Athena AI workspace.",

            documents:0,

            updated:"Just now",

            saved:false

        };


        setSelectedProject(newProject);

    }

    function saveProject(updatedProject){
    
    
        const projectToSave = {
        
            ...updatedProject,
        
            saved:true
        
        };
    
    
        const exists = projects.some(
        
            project => project.id === projectToSave.id
        
        );
    
    
        let updatedProjects;
    
    
        if(exists){
        
        
            updatedProjects = projects.map(project =>
            
                project.id === projectToSave.id
            
                    ? projectToSave
            
                    : project
            
            );
        
        
        }
    
        else{
        
        
            updatedProjects = [
            
                ...projects,
            
                projectToSave
            
            ];
        
        }
    
    
    
        persistProjects(updatedProjects);
    
    
        setSelectedProject(projectToSave);
    
    
    }



    return (

        <div

            style={{

                minHeight:"100vh",

                width:"100%",

                background:theme.background,

                padding:"32px",

                color:theme.text

            }}

        >


            <Navbar

                activePage={activePage}

                onNavigate={navigate}

            />



            {
                activePage === "opportunities" &&

                <OpportunitiesPage />

            }




            {
                activePage === "projects" &&

                !selectedProject &&

                <Projects

                    projects={projects}

                    onCreateProject={createProject}

                    onOpenProject={(project)=>
                    
                        setSelectedProject(project)
                    
                    }
                
                    onDeleteProject={(projectId)=>{
                    
                    
                        const updatedProjects = projects.filter(
                        
                            project => project.id !== projectId
                        
                        );
                    
                    
                        persistProjects(updatedProjects);
                    
                    
                    }}
                
                />

            }




            {
                activePage === "projects" &&

                selectedProject &&

                <Workspace

                    project={selectedProject}


                    onBack={()=>{

                        setSelectedProject(null);

                    }}


                    onSaveProject={saveProject}

                />

            }



        </div>

    );

}


export default Dashboard;