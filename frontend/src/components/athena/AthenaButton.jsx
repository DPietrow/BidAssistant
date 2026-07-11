function AthenaButton({
    onClick,
    active,
    notify,
    count = 0
}) {

return (

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


{
count > 0 &&
<span
    style={{
        fontWeight:700,
        color:"#1e3a8a"
     }}
>
{count}
</span>
}


</button>

)

}

export default AthenaButton;