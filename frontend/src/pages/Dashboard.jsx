import { useState, useEffect } from "react";

import ContractGrid from "../components/contracts/ContractGrid";
import AthenaPanel from "../components/athena/AthenaPanel";
import AthenaButton from "../components/athena/AthenaButton";
import SearchCommandCenter from "../components/search/SearchCommandCenter";

import { theme } from "../theme";



function Dashboard() {


    // Search response from backend
    const [searchResponse, setSearchResponse] = useState(null);

    const [pendingResponse, setPendingResponse] = useState(null);

    const [backendComplete,setBackendComplete] = useState(false);

    const [athenaStatus,setAthenaStatus] = useState("idle");

    // Athena visibility
    const [athenaOpen, setAthenaOpen] = useState(false);

    const [searchIntent,setSearchIntent] = useState("");

    // Contracts selected for Athena
    const [selectedContracts, setSelectedContracts] = useState([]);

    const [athenaNotify, setAthenaNotify] = useState(false);

    const [filters,setFilters] = useState({

        noticeType:"",
        setAside:"",
        minValue:"",
        maxValue:"",
        startDate:"",
        endDate:""

    });



    function handleSearchResults(response) {

         // Hold results until Athena finishes ranking

        setPendingResponse({

            ...response,

            filters

        });

        console.log(
            "FINAL ATHENA RESPONSE",
            response
        );

        setBackendComplete(true);

        setSelectedContracts([]);

    }


    function handleContractSelected(contract){

        setSelectedContracts(prev => {

            const exists = prev.some(
                item => item.sam_id === contract.sam_id
            );


            return exists
            ?
            prev.filter(
                item => item.sam_id !== contract.sam_id
            )
            :
            [
                ...prev,
                contract
            ];

        });


        // wake Athena
        setAthenaNotify(true);


        setTimeout(()=>{
            setAthenaNotify(false);
        },1800);

    }

    useEffect(()=>{


        if(
            backendComplete &&
            pendingResponse &&
            athenaStatus === "ranking"
        ){


            setAthenaStatus("complete");


            setSearchResponse(
                pendingResponse
            );


            setPendingResponse(null);


            setBackendComplete(false);


        }


    },[
        backendComplete,
        pendingResponse,
        athenaStatus
    ]);


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

                <div
                    style={{
                        width: "100%",
                        textAlign: "center",
                        marginBottom: "45px"
                    }}
                >
                
                    <h1
                        style={{
                            color: theme.text,
                            margin: "0 0 16px",
                            fontSize: "42px",
                            fontWeight: 700,
                            letterSpacing: "-1px"
                        }}
                    >
                        Athena AI Procurement Intelligence
                    </h1>
                    
                    
                    <p
                        style={{
                            color: theme.mutedText,
                            fontSize: "18px",
                            maxWidth: "720px",
                            margin: "24px auto 0",
                            lineHeight: "1.6"
                        }}
                    >
                        Discover, analyze, and prioritize government contract opportunities
                        with AI-powered intelligence.
                    </p>
                    
                    
                </div>


            </div>






            {/* Search */}

            <SearchCommandCenter

                filters={filters}

                setFilters={setFilters}

                onResults={handleSearchResults}

                status={athenaStatus}

                setStatus={setAthenaStatus}

                resultCount={
                    searchResponse?.results?.length
                }
            
                searchIntent={searchIntent}
            
                setSearchIntent={setSearchIntent}
            
            />


            {/* Contracts */}

            {
            searchResponse?.results?.length > 0 &&
            
            <div

                key={
                    searchResponse?.results?.length
                }

                className="contract-section-enter"
            
                style={{
                
                    background:theme.panel,
                
                    borderRadius:"16px",
                
                    padding:"28px",
                
                    marginTop:"32px",
                
                    boxShadow:
                        theme.shadow
                
                }}
            
            >



                <h2

                    style={{

                        color:theme.text,

                        marginBottom:"18px"

                    }}

                >

                    Contract Opportunities

                </h2>





                <ContractGrid


                    results={
                            searchResponse?.results
                        }
                    
                    filters={
                        searchResponse?.filters
                    }
                
                    selectedContracts={
                        selectedContracts
                    }
                
                    onSelectContract={
                        handleContractSelected
                    }


                />



            </div>
            }







            {/* Athena Launcher */}

            <AthenaButton
            
                onClick={()=>{
                    setAthenaOpen(!athenaOpen);
                    setAthenaNotify(false);
                }}
            
                active={athenaOpen}
            
                notify={athenaNotify}
            
                count={selectedContracts.length}
            
            />








            {/* Athena Panel */}

            {

                athenaOpen &&


                <AthenaPanel


                    onClose={() =>
                        setAthenaOpen(false)
                    }



                    searchResults={
                        searchResponse
                    }



                    selectedContracts={
                        selectedContracts
                    }


                />


            }





        </div>


    );


}



export default Dashboard;