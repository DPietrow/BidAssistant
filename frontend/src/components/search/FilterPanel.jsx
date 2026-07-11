import { useState } from "react";
import { SlidersHorizontal } from "lucide-react";


function FilterPanel({

    filters,
    setFilters,
    onApply

}) {


    const [open,setOpen] = useState(false);

    const activeFilterCount = Object.entries(filters)
    .filter(([key,value]) => {

        if(Array.isArray(value)) {
            return value.length > 0;
        }

        return value !== "";

    })
    .length;


    return (

        <div className="filter-container">


           <button

                className="filter-toggle"

                onClick={() =>
                    setOpen(!open)
                }
            
            >
            
                <SlidersHorizontal size={18}/>
            
                <span>
                    Advanced Filters
                </span>
            
            
                {
                    activeFilterCount > 0 &&
                
                    <span className="filter-count">
                    
                        {activeFilterCount}
                
                    </span>
                }

            
            </button>




            {
            open &&

            <div className="filter-panel">


                <div className="filter-grid">



                    {/* Notice Type */}

                    <div className="filter-field">

                        <label>
                            Notice Type
                        </label>


                        <select

                            value={filters.noticeType}

                            onChange={
                                e =>
                                setFilters({
                                    ...filters,
                                    noticeType:e.target.value
                                })
                            }

                        >

                            <option value="">
                                All Notice Types
                            </option>

                            <option>
                                Solicitation
                            </option>

                            <option>
                                Award
                            </option>

                            <option>
                                Sources Sought
                            </option>


                        </select>

                    </div>





                    {/* Set Aside */}

                    <div className="filter-field">

                        <label>
                            Set Aside
                        </label>


                        <select

                            value={filters.setAside}

                            onChange={
                                e =>
                                setFilters({
                                    ...filters,
                                    setAside:e.target.value
                                })
                            }

                        >

                            <option value="">
                                All Set Asides
                            </option>

                            <option>
                                Small Business
                            </option>

                            <option>
                                Women Owned
                            </option>

                            <option>
                                Veteran Owned
                            </option>


                        </select>

                    </div>






                    {/* Contract Value */}

                    <div className="filter-field">

                        <label>
                            Contract Value
                        </label>


                        <div className="range-inputs">


                            <input

                                placeholder="Minimum"

                                type="number"

                                value={filters.minValue}

                                onChange={
                                    e =>
                                    setFilters({
                                        ...filters,
                                        minValue:e.target.value
                                    })
                                }

                            />



                            <input

                                placeholder="Maximum"

                                type="number"

                                value={filters.maxValue}

                                onChange={
                                    e =>
                                    setFilters({
                                        ...filters,
                                        maxValue:e.target.value
                                    })
                                }

                            />


                        </div>


                    </div>








                    {/* Dates */}

                    <div className="filter-field">

                        <label>
                            Posted Date Range
                        </label>


                        <div className="range-inputs">


                            <input

                                type="date"

                                value={filters.startDate}

                                onChange={
                                    e =>
                                    setFilters({
                                        ...filters,
                                        startDate:e.target.value
                                    })
                                }

                            />



                            <input

                                type="date"

                                value={filters.endDate}

                                onChange={
                                    e =>
                                    setFilters({
                                        ...filters,
                                        endDate:e.target.value
                                    })
                                }

                            />


                        </div>


                    </div>



                </div>





                <button

                    className="apply-filter"

                    onClick={() => {

                        onApply();
                                        
                        setOpen(false);
                                        
                    }}
                >

                    Apply Filters

                </button>



            </div>

            }


        </div>

    );

}


export default FilterPanel;