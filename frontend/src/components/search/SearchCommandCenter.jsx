import { useState } from "react";

import SearchPanel from "./SearchPanel";
import FilterPanel from "./FilterPanel";
import AthenaStatusBar from "../athena/AthenaStatusBar";
import AthenaAnalysisProgress from "../athena/AthenaAnalysisProgress";


function SearchCommandCenter({

    filters,
    setFilters,
    onResults,
    status,
    setStatus,
    resultCount,
    searchIntent,
    setSearchIntent

}) {


    function getActiveFilters(){

        const chips = [];


        if(filters.noticeType)
            chips.push(filters.noticeType);


        if(filters.setAside)
            chips.push(filters.setAside);


        if(filters.minValue)
            chips.push(
                `Min $${Number(filters.minValue).toLocaleString()}`
            );


        if(filters.maxValue)
            chips.push(
                `Max $${Number(filters.maxValue).toLocaleString()}`
            );


        if(filters.startDate && filters.endDate)
            chips.push(
                `${filters.startDate} → ${filters.endDate}`
            );


        return chips;

    }



    const activeFilters = getActiveFilters();



    return (

        <div

            style={{

                background:"#ffffff",

                borderRadius:"18px",

                padding:"28px",

                boxShadow:
                "0 8px 24px rgba(15,23,42,.08)"

            }}

        >



            <h2

                style={{

                    color:"#111827",

                    marginBottom:"6px",

                    fontSize:"24px",

                    fontWeight:700

                }}

            >

                Athena Procurement Command Center

            </h2>





            <p

                style={{

                    color:"#64748b",

                    marginBottom:"24px"

                }}

            >

                Describe the opportunities you want Athena to discover and analyze.

            </p>







            {/* Search Intent */}

            <div

                style={{

                    marginBottom:"22px"

                }}

            >


                <input

                    value={searchIntent}

                    onChange={
                        e =>
                        setSearchIntent(e.target.value)
                    }


                    placeholder="Example: Find cybersecurity contracts for small businesses under $5M"


                    style={{

                        width:"100%",

                        padding:"14px 16px",

                        borderRadius:"12px",

                        border:"1px solid #cbd5e1",

                        fontSize:"16px",

                        outline:"none"

                    }}


                />


            </div>

                <SearchPanel

                    onResults={(results)=>{
                    
                        onResults(results);
                    
                    }}
                
                
                    onSearchStart={(stage)=>{

                        setStatus(stage);

                    }}
                
                
                    filters={filters}
                
                />


            <FilterPanel

                filters={filters}

                setFilters={setFilters}

            />


            {/* Active Filter Chips */}

            {

            activeFilters.length > 0 &&


            <div

                style={{

                    marginTop:"20px"

                }}

            >


                <div

                    style={{

                        fontSize:"14px",

                        fontWeight:600,

                        color:"#475569",

                        marginBottom:"10px"

                    }}

                >

                    Active Filters

                </div>





                <div

                    style={{

                        display:"flex",

                        gap:"8px",

                        flexWrap:"wrap"

                    }}

                >


                    {

                    activeFilters.map(

                        (filter,index)=>(


                            <div

                                key={index}

                                style={{

                                    background:"#eef2ff",

                                    color:"#4338ca",

                                    padding:"6px 12px",

                                    borderRadius:"999px",

                                    fontSize:"13px",

                                    fontWeight:600

                                }}

                            >

                                {filter}

                            </div>


                        )

                    )

                    }


                </div>


            </div>


            }









            {/* Athena Status */}

            <div

                style={{

                    marginTop:"20px"

                }}

            >

                <AthenaAnalysisProgress

                    status={status}                            
                />

                <AthenaStatusBar

                    status={
                        status === "complete"
                        ? status
                        : null
                    }
                
                    resultCount={resultCount}
                
                />

            </div>


            {/* Metrics */}

            {

            status === "complete" &&


            <div

                style={{

                    display:"grid",

                    gridTemplateColumns:
                    "repeat(3,1fr)",

                    gap:"14px",

                    marginTop:"20px"

                }}

            >



                <div className="metric-card">


                    <h3>

                        {resultCount ?? 0}

                    </h3>


                    <span>

                        Opportunities Found

                    </span>


                </div>







                <div className="metric-card">


                    <h3>

                        AI Ranked

                    </h3>


                    <span>

                        Athena Matches

                    </span>


                </div>







                <div className="metric-card">


                    <h3>

                        Ready

                    </h3>


                    <span>

                        For Review

                    </span>


                </div>



            </div>


            }



        </div>

    );


}


export default SearchCommandCenter;