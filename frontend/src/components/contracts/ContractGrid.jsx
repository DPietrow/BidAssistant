import ContractCard from "./ContractCard";


function ContractGrid({

    results,

    selectedContracts = [],

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


                    const contract =
                        item.contract;



                    const isSelected =
                        selectedContracts.some(

                            selected =>
                            selected.sam_id === contract.sam_id

                        );



                    return (

                        <ContractCard


                            key={
                                contract.sam_id
                            }



                            contract={
                                contract
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