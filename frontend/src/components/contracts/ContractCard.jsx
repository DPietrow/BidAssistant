import {
    ExternalLink
} from "lucide-react";


function ContractCard({
    contract,
    onSelect
}) {


    return (

        <div

            onClick={() =>
                onSelect(contract)
            }


            style={{

                background:"white",

                borderRadius:"12px",

                padding:"20px",

                cursor:"pointer",

                boxShadow:
                "0 2px 8px rgba(0,0,0,.08)",

                transition:
                "transform .2s"

            }}

        >


            <h3>

                {contract.title}

            </h3>


            <p>

                <strong>
                    Agency:
                </strong>

                {" "}

                {contract.agency}

            </p>


            <p>

                <strong>
                    SAM ID:
                </strong>

                {" "}

                {contract.sam_id}

            </p>


            <p>

                <strong>
                    NAICS:
                </strong>

                {" "}

                {contract.naics}

            </p>



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

                        display:"flex",

                        alignItems:"center",

                        gap:"6px"

                    }}

                >

                    View Posting

                    <ExternalLink size={14}/>


                </a>

            }


        </div>

    )

}


export default ContractCard;