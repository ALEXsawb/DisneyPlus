import React from "react";
import styles from "../App.module.css";
import Visits from "./Visits";

class User extends React.Component{
    state = {
        dropped: false,
    }

    render() {
        return <div key={this.props.userData.email} className={styles.row}>
            <div onClick={() => {this.setState({dropped: !this.state.dropped})}} className={styles.user_data}>
                <div>{this.props.userData.id}</div>
                <div>{this.props.userData.email}</div>
            </div>
            <div>
                <div className={styles.visits}>
                    {this.state.dropped ? <Visits wsChanel={this.props.wsChanel}
                                                  visits={this.props.userData.visits}
                                                  userId={this.props.userData.id}
                                                  visits_count={this.props.userData.visits_count}/> : ''}
                </div>
            </div>
        </div>;
    }
}

export default User