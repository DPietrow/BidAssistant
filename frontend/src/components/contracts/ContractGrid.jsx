import ContractCard from "./ContractCard";


function ContractGrid({
    results,
    onSelectContract
}) {


    if(!results || results.length === 0){

        return (

            <p>
                No contract opportunities found.
            </p>

        )

    }



    return (

        <div

            style={{

                display:"grid",

                gridTemplateColumns:
                "repeat(auto-fill,minmax(300px,1fr))",

                gap:"20px"

            }}

        >

            {
                results.map(
                    item =>

                    <ContractCard

                        key={
                            item.contract.sam_id
                        }


                        contract={
                            item.contract
                        }


                        onSelect={
                            onSelectContract
                        }

                    />

                )
            }


        </div>

    )

}


export default ContractGrid;