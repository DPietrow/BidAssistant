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
<span className="athena-badge">
{count}
</span>
}


</button>

)

}

export default AthenaButton;