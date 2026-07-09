import axios from "axios";


const api = axios.create({

    baseURL:
        "/api"

});


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