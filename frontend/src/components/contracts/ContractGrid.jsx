import ContractCard from "./ContractCard";


function ContractGrid({

    results,

    filters,

    selectedContracts = [],

    onSelectContract

}) {


    if(
        !results ||
        results.length === 0
    ){

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

            results.map((item,index)=>{


                //
                // Support both:
                //
                // Old:
                // { contract:{...} }
                //
                // New:
                // {...contract}
                //
                const contract =
                    item.contract ?? item;



                if(!contract){

                    return null;

                }



                const isSelected =
                    selectedContracts.some(

                        selected =>
                        selected.sam_id === contract.sam_id

                    );




                return (

                    <ContractCard


                        key={

                            contract.sam_id
                            ??
                            index

                        }



                        contract={

                            contract

                        }



                        filters={

                            filters

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