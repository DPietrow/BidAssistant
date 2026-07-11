import { EyeOff } from "lucide-react";


function AthenaButton({
    onClick,
    active,
    notify,
    count = 0,
    onHide
}) {


return (

<div

style={{

    position:"fixed",

    right:"32px",

    top:"24px",

    zIndex:2000,

    display:"flex",

    flexDirection:"column",

    alignItems:"center"

}}

>


{
count > 0 &&

<div

style={{

    marginBottom:"8px",

    fontSize:"38px",

    fontWeight:900,

    color:"#2563eb",

    textShadow:
        "0 0 15px rgba(37,99,235,.9)",

    animation:"pulseGlow 1.8s infinite",

    textAlign:"center"

}}

>

{count}

<div

style={{

    fontSize:"11px",

    fontWeight:700,

    color:"#475569",

    textShadow:"none"

}}

>

CONTEXT

</div>


</div>

}



<button

className={

    `athena-button
    ${active ? "active" : ""}
    ${notify ? "notify" : ""}`

}

onClick={onClick}

aria-label="Open Athena Assistant"

>

<img

src="/favicon-athenalogo.svg"

className="athena-icon"

/>

</button>



<button

onClick={onHide}

style={{

    position:"absolute",

    right:"0",

    bottom:"-38px",

    zIndex:2000,

    borderRadius:"999px",

    padding:"8px 16px",

    background:"#111827",

    color:"white",

    border:"none",

    cursor:"pointer",

    fontSize:"12px",

    boxShadow:
        "0 4px 12px rgba(0,0,0,.25)",

    transition:
        "transform .2s ease"

}}


onMouseEnter={(e)=>{

    e.currentTarget.style.transform =
        "translateY(-3px)";

}}


onMouseLeave={(e)=>{

    e.currentTarget.style.transform =
        "translateY(0)";

}}

>

Hide Athena

</button>


</div>

)

}


export default AthenaButton;