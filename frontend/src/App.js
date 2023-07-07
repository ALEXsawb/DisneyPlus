import styles from './App.module.css';
import React from "react";
import {connect} from "react-redux";
import {addUser, addVisit, addUsers, addVisits, addUsersQuantity, setUsers, setVisits} from "./user-reducer";
import User from "./components/User";


class App extends React.Component {
  state = {
    ws: null
  }

  check = () => {
    const ws = this.state;
    if (ws !== null  || ws.readyState === WebSocket.CLOSED) {
      this.createChanel()
    }
  }

  closeHandler = () => {
      setTimeout(this.check, 3000)
    }

  createChanel = () => {

      let wsChanel = new WebSocket('ws://localhost:8000/admin/ws/users')

      wsChanel.onopen = () => {
        this.setState({ws: wsChanel})
      }

      wsChanel.onclose = () => {
        this.closeHandler()
      }

      wsChanel.onmessage = (e) => {
        let data = JSON.parse(e.data)
        switch (data.event) {
          case 'connect': {
            return this.props.setUsers(data.data, data.count_users)
          }
          case 'add_visits': {
            return this.props.addVisits(data.user_id, data.visits)
          }
          case 'add_users': {
            return this.props.addUsers(data.users)
          }
          case 'add_visit': {
            return this.props.addVisit(data.end_user_id, data.web_page_url)
          }
          case 'add_user': {
            return this.props.addUser(data)
          }
          case 'visits_by_page': {
            return this.props.setVisits(data.user_id, data.visits, data.page)
          }
          case 'users_by_page': {
            return this.props.setUsers(data.users, data.page)
          }
        }
      }

      wsChanel.onerror = () => {
        wsChanel.close()
      }
    }

  componentDidMount() {
    this.createChanel()
  }

  render() {
    return <div className={styles.table}>
      {this.props.users.map(m => {
        return <User userData={m} wsChanel={this.state.ws}/>
      })}
      <p>{this.props.users.length} from {this.props.count_users}</p>
      {
        (this.props.count_users !== this.props.users.length)?
            <button onClick={() => {
              addUsersQuantity(this.state.ws, this.props.users.length, this.props.count_users)
            }}>
              Show more Users
            </button>: ''
      }
    </div>
  }
}

const mapDispatchToProps = (dispatch) => {
  return {
    setUsers: (usersData, count_users) => dispatch(setUsers(usersData, count_users)),
    setVisits: (user_id, visits, count_visits) => dispatch(setVisits(user_id, visits, count_visits)),
    addVisit: (user_id, visit) => dispatch(addVisit(user_id, visit)),
    addUser: (userData) => dispatch(addUser(userData)),
    addUsers: (users) => dispatch(addUsers(users)),
    addVisits: (user_id, visits) => dispatch(addVisits(visits, user_id)),
  }
};


const mapStateToProps = (state) => {
  return ({
    users: state.users.users,
    count_users: state.users.count_users
  })
};

export default connect(mapStateToProps, mapDispatchToProps)(App);