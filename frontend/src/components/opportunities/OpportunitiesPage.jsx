import { useState, useEffect } from "react";

import ContractGrid from "../contracts/ContractGrid";
import AthenaPanel from "../athena/AthenaPanel";
import AthenaButton from "../athena/AthenaButton";
import SearchCommandCenter from "../search/SearchCommandCenter";

import { theme } from "../../theme";

function OpportunitiesPage() {

    // Search response from backend
    const [searchResponse, setSearchResponse] = useState(null);
    const [pendingResponse, setPendingResponse] = useState(null);
    const [backendComplete, setBackendComplete] = useState(false);

    // Athena state
    const [athenaStatus, setAthenaStatus] = useState("idle");
    const [athenaOpen, setAthenaOpen] = useState(false);
    const [showAthenaButton, setShowAthenaButton] = useState(true);
    const [athenaNotify, setAthenaNotify] = useState(false);

    // Search state
    const [searchIntent, setSearchIntent] = useState("");
    const [searchSummary, setSearchSummary] = useState(null);

    // Selected contracts
    const [selectedContracts, setSelectedContracts] = useState([]);

    // Filters
    const [filters, setFilters] = useState({

        noticeType: "",
        setAside: "",
        minValue: "",
        maxValue: "",
        startDate: "",
        endDate: ""

    });

    function handleSearchResults(response) {

        setPendingResponse({

            ...response,

            filters

        });

        setBackendComplete(true);

        setSelectedContracts([]);

    }

    function handleContractSelected(contract) {

        setSelectedContracts(prev => {

            const exists = prev.some(
                item => item.sam_id === contract.sam_id
            );

            return exists
                ? prev.filter(item => item.sam_id !== contract.sam_id)
                : [...prev, contract];

        });

        setAthenaNotify(true);

        setTimeout(() => {

            setAthenaNotify(false);

        }, 1800);

    }

    useEffect(() => {

        if (

            backendComplete &&
            pendingResponse &&
            athenaStatus === "ranking"

        ) {

            setAthenaStatus("complete");

            setSearchResponse(pendingResponse);

            setPendingResponse(null);

            setBackendComplete(false);

        }

    }, [

        backendComplete,
        pendingResponse,
        athenaStatus

    ]);

    return (

        <>

            {/* Hero */}

            <div

                style={{

                    textAlign: "center",

                    marginBottom: "45px"

                }}

            >

                <h1

                    style={{

                        color: theme.text,

                        margin: "0 0 16px",

                        fontSize: "42px",

                        fontWeight: 700,

                        letterSpacing: "-1px"

                    }}

                >

                    Athena AI Procurement Intelligence

                </h1>

                <p

                    style={{

                        color: theme.mutedText,

                        fontSize: "18px",

                        maxWidth: "720px",

                        margin: "24px auto 0",

                        lineHeight: "1.6"

                    }}

                >

                    Discover, analyze, and prioritize government contract
                    opportunities with AI-powered intelligence.

                </p>

            </div>

            {/* Search */}

            <SearchCommandCenter

                filters={filters}

                setFilters={setFilters}

                onResults={handleSearchResults}

                status={athenaStatus}

                setStatus={setAthenaStatus}

                resultCount={searchResponse?.results?.length}

                searchIntent={searchIntent}

                setSearchIntent={setSearchIntent}

                searchSummary={searchSummary}

                setSearchSummary={setSearchSummary}

            />

            {/* Results */}

            {

                searchResponse?.results?.length > 0 &&

                <div

                    className="contract-section-enter"

                    style={{

                        background: theme.panel,

                        borderRadius: "16px",

                        padding: "28px",

                        marginTop: "32px",

                        boxShadow: theme.shadow

                    }}

                >

                    <h2

                        style={{

                            color: theme.text,

                            marginBottom: "18px"

                        }}

                    >

                        Contract Opportunities

                    </h2>

                    <ContractGrid

                        results={searchResponse.results}

                        filters={searchResponse.filters}

                        selectedContracts={selectedContracts}

                        onSelectContract={handleContractSelected}

                    />

                </div>

            }

            {/* Athena Button */}

            {

                showAthenaButton

                    ?

                    (

                        <AthenaButton

                            onClick={() => {

                                setAthenaOpen(!athenaOpen);

                                setAthenaNotify(false);

                            }}

                            active={athenaOpen}

                            notify={athenaNotify}

                            count={selectedContracts.length}

                            onHide={() =>
                                setShowAthenaButton(false)
                            }

                        />

                    )

                    :

                    (

                        <button

                            onClick={() =>
                                setShowAthenaButton(true)
                            }

                            style={{

                                position: "fixed",

                                right: "32px",

                                top: "24px",

                                zIndex: 2000,

                                borderRadius: "999px",

                                padding: "10px 16px",

                                background: "#111827",

                                color: "white",

                                border: "none",

                                cursor: "pointer"

                            }}

                        >

                            Open Athena

                        </button>

                    )

            }

            {/* Athena Panel */}

            {

                athenaOpen &&

                <AthenaPanel

                    onClose={() =>
                        setAthenaOpen(false)
                    }

                    searchResults={searchResponse}

                    selectedContracts={selectedContracts}

                />

            }

        </>

    );

}

export default OpportunitiesPage;