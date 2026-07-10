import { useState } from "react";

import {
    ExternalLink,
    CheckCircle2
} from "lucide-react";


function ContractCard({

    contract,

    onSelect,

    selected

}) {


    const [hover,setHover] = useState(false);



    function handleSelect(){

        onSelect(contract);

    }



    return (

        <div


            onClick={handleSelect}


            style={{


                position:"relative",


                background:
                    selected
                    ? "#eff6ff"
                    : "white",



                border:
                    selected
                    ? "2px solid #2563eb"
                    : hover
                        ? "2px solid #d1d5db"
                        : "2px solid transparent",



                borderRadius:"14px",


                padding:"20px",


                cursor:"pointer",



                transition:"all .18s ease",



                transform:
                    hover
                    ? "translateY(-2px)"
                    : "translateY(0)",



                boxShadow:
                    selected
                    ? "0 8px 18px rgba(37,99,235,.18)"
                    : hover
                        ? "0 6px 14px rgba(0,0,0,.10)"
                        : "0 2px 8px rgba(0,0,0,.08)"


            }}



            onMouseEnter={() =>
                setHover(true)
            }



            onMouseLeave={() =>
                setHover(false)
            }



        >



            {
                selected &&

                <div

                    style={{

                        position:"absolute",

                        left:0,

                        top:0,

                        bottom:0,

                        width:"6px",

                        background:"#2563eb",

                        borderRadius:
                            "14px 0 0 14px"

                    }}

                />

            }





            {/* Header */}

            <div

                style={{

                    display:"flex",

                    justifyContent:"space-between",

                    alignItems:"flex-start",

                    marginBottom:"14px"

                }}

            >



                <h3

                    style={{

                        margin:0,

                        color:"#111827",

                        fontSize:"1.15rem",

                        paddingRight:"10px"

                    }}

                >

                    {contract.title}

                </h3>




                {

                    selected &&

                    <CheckCircle2

                        color="#2563eb"

                        size={22}

                    />

                }



            </div>





            <div

                style={{

                    display:"grid",

                    rowGap:"8px",

                    color:"#374151",

                    fontSize:".95rem"

                }}

            >



                <div>

                    <strong>
                        Agency:
                    </strong>

                    {" "}

                    {contract.agency}

                </div>





                <div>

                    <strong>
                        SAM ID:
                    </strong>

                    {" "}

                    {contract.sam_id}

                </div>





                <div>

                    <strong>
                        NAICS:
                    </strong>

                    {" "}

                    {contract.naics ?? "Not listed"}

                </div>



            </div>





            {
                selected &&

                <div

                    style={{

                        marginTop:"14px",

                        color:"#2563eb",

                        fontSize:".85rem",

                        fontWeight:600

                    }}

                >

                    Selected for Athena analysis

                </div>

            }






            {
                contract.url &&

                <a

                    href={contract.url}

                    target="_blank"

                    rel="noopener noreferrer"


                    onClick={
                        e =>
                        e.stopPropagation()
                    }



                    style={{


                        display:"inline-flex",


                        alignItems:"center",


                        gap:"6px",


                        marginTop:"18px",


                        color:"#2563eb",


                        textDecoration:"none",


                        fontWeight:500


                    }}

                >


                    View Posting


                    <ExternalLink size={15}/>


                </a>

            }



        </div>

    );

}


export default ContractCard;