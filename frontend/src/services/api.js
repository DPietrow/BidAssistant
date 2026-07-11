import axios from "axios";


const api = axios.create({

    baseURL:
        "/api"

});




// Existing non-streaming search
export async function askAthena(
    query,
    filters={}
){

    const response =
        await api.post(

            "/ask",

            {
                query,
                filters
            }

        );


    return response.data;

}







// Streaming Athena search using Server Sent Events
export async function streamAthenaSearch(
    query,
    filters={},
    onStatus,
    onComplete
){
    console.log(
                    "ATHENA REQUEST",
                    {
                        query,
                        filters
                    }
                )
                
    const response =
        await fetch(

            "/api/search/stream",

            {
                method:"POST",

                headers:{
                    "Content-Type":"application/json"
                },

                body:JSON.stringify({
                    query,
                    filters
                })

            }

        );



    if(!response.ok){

        throw new Error(
            "Athena streaming search failed"
        );

    }



    const reader =
        response.body.getReader();


    const decoder =
        new TextDecoder();



    let buffer="";



    while(true){


        const {
            done,
            value
        } =
        await reader.read();



        if(done){
            break;
        }



        buffer += decoder.decode(
            value,
            {
                stream:true
            }
        );



        const events =
            buffer.split("\n\n");



        buffer =
            events.pop();



        for(const event of events){


            if(!event.trim()){
                continue;
            }



            let eventName=null;

            let data=null;



            event
                .split("\n")
                .forEach(line=>{


                    if(
                        line.startsWith("event:")
                    ){

                        eventName =
                            line
                            .replace(
                                "event:",
                                ""
                            )
                            .trim();

                    }



                    if(
                        line.startsWith("data:")
                    ){

                        data =
                            JSON.parse(
                                line
                                .replace(
                                    "data:",
                                    ""
                                )
                                .trim()
                            );

                    }


                });



            console.log(
                "ATHENA EVENT:",
                eventName,
                data
            );



            if(
                eventName === "status"
                &&
                data
            ){

                onStatus?.(
                    data.stage
                );

            }



            if(
                eventName === "complete"
                &&
                data
            ){

                console.log(
                    "ATHENA COMPLETE:",
                    data
                );


                onComplete?.(
                    data
                );

            }


        }


    }


}