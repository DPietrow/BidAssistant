import { Search, Sparkles, CheckCircle } from "lucide-react";


function AthenaStatusBar({
    status,
    resultCount,
    searchSummary
}) {


    if(!status)
        return null;


    const states = {

        searching:{
            icon:<Search size={18}/>,
            text:"Athena is searching government opportunities..."
        },


        analyzing:{
            icon:<Sparkles size={18}/>,
            text:"Athena is analyzing and ranking contract matches..."
        },


        complete:{
            icon:<CheckCircle size={18}/>,
            text:
                searchSummary
                ?
                (()=>{
                
                    const filters = [];
                
                    const f = searchSummary.filters;
                
                
                    if(f.noticeType)
                        filters.push(f.noticeType);
                
                
                    if(f.setAside)
                        filters.push(f.setAside);
                
                
                    if(f.minValue)
                        filters.push(
                            `Min $${Number(f.minValue).toLocaleString()}`
                        );
                    
                    
                    if(f.maxValue)
                        filters.push(
                            `Max $${Number(f.maxValue).toLocaleString()}`
                        );
                    
                    
                    if(f.startDate && f.endDate)
                        filters.push(
                            `${f.startDate} → ${f.endDate}`
                        );
                    
                    
                    return `Athena found ${
                        resultCount ?? 0
                    } matching opportunities based on "${
                        searchSummary.intent || "your search criteria"
                    }"${
                        filters.length
                        ?
                        ` with ${filters.join(", ")}`
                        :
                        ""
                    }`;
                
                })()
                :
                `Athena found ${resultCount ?? 0} matching opportunities`
        }

    };


    const current =
        states[status];



    return (

        <div

            style={{

                display:"flex",

                alignItems:"center",

                gap:"10px",

                marginBottom:"20px",

                padding:"14px 18px",

                borderRadius:"12px",

                background:"#eef2ff",

                border:"1px solid #c7d2fe",

                color:"#3730a3",

                fontWeight:600,

                animation:"fadeIn .25s ease"

            }}

        >

            <div>

                {current.icon}

            </div>


            <span>

                {current.text}

            </span>


            {
                status !== "complete" &&

                <div
                    className="athena-thinking-dots"
                >

                    <span></span>
                    <span></span>
                    <span></span>

                </div>

            }


        </div>

    );

}


export default AthenaStatusBar;