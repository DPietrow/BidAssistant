import { useState, useEffect } from "react";

import {
    Search,
    Filter
} from "lucide-react";
import {streamAthenaSearch} from "../../services/api";

import {theme} from "../../theme";


function SearchPanel({
    onResults,
    onSearchStart,
    searchIntent,
    setSearchIntent,
    filters,
    setFilters,
    setSearchSummary
}) {

    const [query,setQuery] = useState("");

    const [agency,setAgency] = useState("");

    const [naics,setNaics] = useState("");

    const [loading,setLoading] = useState(false);

    const [draftFilters, setDraftFilters] = useState(filters);

    async function handleSearch(){


        if(!query){
            return;
        }


        setLoading(true);



        try{


            await streamAthenaSearch(
                
                query,

                {
                    agency,
                    naics,
                    intent: searchIntent,
                    ...filters
                },

                (stage)=>{

                    if(onSearchStart){

                        onSearchStart(stage);

                    }

                },
                

                (response)=>{


                    onResults(response);

                    const completedSearchSummary = {
                    
                        intent: searchIntent,
                    
                        filters:{
                            ...filters
                        }
                    
                    };
                    
                    
                    setSearchSummary(
                        completedSearchSummary
                    );
                    
                    
                    setQuery("");
                    
                    setSearchIntent("");
                    
                    
                    setFilters({
                    
                        noticeType:"",
                        setAside:"",
                        minValue:"",
                        maxValue:"",
                        startDate:"",
                        endDate:""
                    
                    });


                }


            );


        }


        catch(error){

            console.error(
                "Search failed",
                error
            );

        }


        finally{

            setLoading(false);

        }


    }

    useEffect(() => {
        setDraftFilters(filters);
    }, [filters]);

    return (

        <div

            style={{

                background: theme.panel,

                borderRadius:"12px",

                padding:"24px",

                marginBottom:"24px",

                boxShadow:
                theme.shadow

            }}

        >


            <h2
             style={{
                    color:theme.text
                }}
            >

                Search Opportunities

            </h2>



            <div

                style={{

                    display:"grid",

                    gridTemplateColumns:
                    "2fr 1fr 1fr auto",

                    gap:"12px",

                    alignItems:"center"

                }}

            >



                {/* Search */}

                <input

                    value={query}

                    onChange={
                        e =>
                        setQuery(
                            e.target.value
                        )
                    }


                    placeholder=
                    "Search contracts..."

                    style={{

                        padding:"12px",

                        borderRadius:"8px",

                        border:
                        "1px solid #ddd"

                    }}

                />




                {/* Agency */}

                <input

                    value={agency}

                    onChange={
                        e =>
                        setAgency(
                            e.target.value
                        )
                    }


                    placeholder=
                    "Agency"

                    style={{

                        padding:"12px",

                        borderRadius:"8px",

                        border:
                        "1px solid #ddd"

                    }}

                />




                {/* NAICS */}

                <input

                    value={naics}

                    onChange={
                        e =>
                        setNaics(
                            e.target.value
                        )
                    }


                    placeholder=
                    "NAICS"

                    style={{

                        padding:"12px",

                        borderRadius:"8px",

                        border:
                        "1px solid #ddd"

                    }}

                />




                <button

                    onClick={
                        handleSearch
                    }


                    disabled={
                        loading
                    }


                    style={{

                        display:"flex",

                        alignItems:"center",

                        gap:"6px",

                        padding:"12px 18px"

                    }}

                >

                    {
                        loading
                        ?
                        "Searching..."
                        :
                        <>
                            <Search size={18}/>
                            Search
                        </>
                    }


                </button>


            </div>



            <div

                style={{

                    marginTop:"16px",

                    display:"flex",

                    alignItems:"center",

                    gap:"8px",

                    color:"#666"

                }}

            >

                <Filter size={16}/>

                Filters will expand here:
                notice type, set-aside, value, dates


            </div>


        </div>

    )

}


export default SearchPanel;