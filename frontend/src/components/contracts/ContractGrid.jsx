import ContractCard from "./ContractCard";


function ContractGrid({

    results,

    selectedContracts,

    onSelectContract

}) {


    if(!results || results.length === 0){

        return (

            <p
                style={{
                    color:"#6b7280"
                }}
            >
                No contract opportunities found.
            </p>

        );

    }



    return (

        <div

            style={{

                display:"grid",

                gridTemplateColumns:
                    "repeat(auto-fill,minmax(320px,1fr))",

                gap:"20px"

            }}

        >

            {

                results.map((item)=>{

                    const isSelected =
                        selectedContracts.some(
                            contract =>
                            contract.sam_id === item.contract.sam_id
                        );


                    return (

                        <ContractCard

                            key={
                                item.contract.sam_id
                            }

                            contract={
                                item.contract
                            }

                            selected={
                                isSelected
                            }

                            onSelect={
                                onSelectContract
                            }

                        />

                    );

                })

            }

        </div>

    );

}


export default ContractGrid;