import { useState, useEffect } from "react";

import SearchPanel from "../components/search/SearchPanel";
import FilterPanel from "../components/search/FilterPanel";
import ContractGrid from "../components/contracts/ContractGrid";
import AthenaPanel from "../components/athena/AthenaPanel";
import AthenaButton from "../components/athena/AthenaButton";

import { theme } from "../theme";



function Dashboard() {


    // Search response from backend
    const [searchResponse, setSearchResponse] = useState(null);



    // Athena visibility
    const [athenaOpen, setAthenaOpen] = useState(false);


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


        setSearchResponse({

            ...response,

            filters

        });


        // Reset selected contracts on new search
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






            {/* Search */}

            <div

                style={{

                    background:"white",

                    borderRadius:"16px",

                    padding:"24px",

                    marginBottom:"24px",

                    boxShadow:
                    "0 4px 14px rgba(15,23,42,.08)"

                }}

            >


                <SearchPanel

                    onResults={handleSearchResults}

                    filters={filters}

                />

                   <FilterPanel

                     filters={filters}
                            
                     setFilters={setFilters}
                            
                     onApply={() => {
                        
                         console.log(
                             "Applying filters",
                             filters
                         );
                        
                         // later:
                         // trigger backend search here
                        
                     }}
                    
                 />



            </div>







            {/* Contracts */}

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