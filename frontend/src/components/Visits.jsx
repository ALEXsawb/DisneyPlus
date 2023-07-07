import React from "react";
import {addVisitsQuantity} from "../user-reducer";

const Visits = (props) => {
    return <div>
        {props.visits.map(visit => {
            return <h6>{visit}</h6>
        })}
        <p>{props.visits.length} from {props.visits_count}</p>
        {
            (props.visits.length !== props.visits_count)?
                <button onClick={() => addVisitsQuantity(props.wsChanel, props.userId, props.visits.length,
                        props.visits_count)}>
                    Show more visits
                </button>: ''
        }
    </div>
}

export default Visits