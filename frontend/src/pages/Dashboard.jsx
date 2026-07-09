import { useState } from "react";

import SearchPanel from "../components/search/SearchPanel";

import ContractGrid from "../components/contracts/ContractGrid";

import AthenaPanel from "../components/athena/AthenaPanel";

import {
    Bot
} from "lucide-react";

import {
    theme
} from "../theme";


function Dashboard() {

    const [searchResults,setSearchResults] = useState([]);

    const [athenaOpen,setAthenaOpen] = useState(false);

    const [selectedContract,setSelectedContract] = useState(null);

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


            {/* Header */}

            <div
                style={{
                    display:"flex",
                    justifyContent:"space-between",
                    alignItems:"center",
                    marginBottom:"30px"
                }}
            >

                <div>

                    <h1
                        style={{
                            color:theme.text,
                            marginBottom:"8px"
                        }}                  
                    >
                        Athena Bid Intelligence
                    </h1>

                    <p
                        style={{
                             color:theme.mutedText
                         }}
                    >
                        Search and analyze government contracting opportunities
                    </p>

                </div>


            </div>



            {/* Search Area */}

            <div
                style={{
                    background:"white",
                    borderRadius:"12px",
                    padding:"24px",
                    marginBottom:"24px",
                    boxShadow:
                    "0 2px 8px rgba(0,0,0,.08)"
                }}
            >

                <SearchPanel
                    onResults={
                        setSearchResults
                    }
                />


            </div>





            {/* Results Area */}

            <div
                style={{
                    background:"white",
                    borderRadius:"12px",
                    padding:"24px",
                    minHeight:"300px"
                }}
            >
            
            <h2
                style={{
                    color:theme.text
                }}
            >
                Contract Opportunities
            </h2>
            
            
            <ContractGrid

                results={
                    searchResults?.results
                }
            
                onSelectContract={
                    setSelectedContract
                }
            
            />

            
            </div>



            {/* Athena Floating Button */}

            <button

                onClick={() =>
                    setAthenaOpen(
                        !athenaOpen
                    )
                }


                style={{

                    position:"fixed",

                    right:"32px",

                    bottom:"32px",

                    width:"60px",

                    height:"60px",

                    borderRadius:"50%",

                    border:"none",

                    background:"#111827",

                    color:"white",

                    display:"flex",

                    alignItems:"center",

                    justifyContent:"center",

                    cursor:"pointer",

                    boxShadow:
                    "0 4px 15px rgba(0,0,0,.25)"

                }}

            >

                <Bot size={28}/>


            </button>


            {
               athenaOpen &&
                <AthenaPanel
                    searchResults={searchResults}
                    onClose={() =>
                        setAthenaOpen(false)
                    }
                />

            }


        </div>

    )

}


export default Dashboard;