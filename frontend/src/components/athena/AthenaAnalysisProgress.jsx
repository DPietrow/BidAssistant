import {
    Search,
    Database,
    Layers,
    Sparkles,
    Check
} from "lucide-react";


function AthenaAnalysisProgress({
    status
}) {


    if(
        ![
            "discovering",
            "analyzing",
            "matching",
            "ranking",
            "complete"
        ].includes(status)
    )
    {
        return null;
    }



    const steps = [

        {
            icon:<Search size={18}/>,
            text:
            "Searching government procurement sources"
        },

        {
            icon:<Database size={18}/>,
            text:
            "Analyzing government procurement data"
        },

        {
            icon:<Layers size={18}/>,
            text:
            "Matching NAICS classifications"
        },

        {
            icon:<Sparkles size={18}/>,
            text:
            "Ranking contract relevance"
        }

    ];



    const statusMap = {

        discovering:0,

        analyzing:1,

        matching:2,

        ranking:3,

        complete:4

    };


    const activeStep =
        statusMap[status];

    const titles = {

        discovering:
        "Athena is discovering opportunities...",


        analyzing:
        "Athena is analyzing procurement intelligence...",


        matching:
        "Athena is matching capabilities...",


        ranking:
        "Athena is ranking best-fit opportunities..."

    };

    return (

        <div

            style={{

                marginTop:"24px",

                padding:"18px",

                borderRadius:"14px",

                background:"#f8fafc",

                border:
                "1px solid #e2e8f0"

            }}

        >


            <div

                style={{

                    fontWeight:700,

                    color:"#1e293b",

                    marginBottom:"14px"

                }}

            >

                    {titles[status]}

            </div>





            {
                steps.map(

                    (step,index)=>{


                        const complete =
                            index < activeStep;


                        const active =
                            index === activeStep;



                        return (

                            <div

                                key={index}

                                style={{

                                    display:"flex",

                                    alignItems:"center",

                                    gap:"10px",

                                    marginBottom:"10px",

                                    color:

                                    complete || active

                                    ?

                                    "#2563eb"

                                    :

                                    "#94a3b8",


                                    fontWeight:
                                    active
                                    ? 600
                                    : 400

                                }}

                            >


                                {
                                    complete

                                    ?

                                    <Check size={18}/>

                                    :

                                    step.icon

                                }



                                <span>

                                    {step.text}

                                </span>



                            </div>

                        );

                    }

                )
            }



        </div>

    );

}


export default AthenaAnalysisProgress;