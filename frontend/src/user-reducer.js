const UsersState = {
    users: [
        {id: '32343242342342343',
         email: 'email@gmail.com',
         visits: ['http://http://127.0.0.1:8000/star_wars'],
         visits_count: 1
        }
        ],
    count_users: 1
}


const SET_USERS = "SET_USERS"
const SET_VISITS = "SET_VISITS"
const ADD_VISIT = "ADD_VISIT"
const ADD_USER = "ADD_USER"
const ADD_USERS = "ADD_USERS"
const ADD_VISITS = "ADD_VISITS"



const usersReducer = (state = UsersState, action) => {
    switch (action.type){
        case SET_USERS: {
            console.log('USERS: ', action.users)
            return {...state, users: [...action.users.reverse().map(u => ({...u, visits: u.visits.reverse()}))], count_users: action.count_users}
        }
        case SET_VISITS: {
            let users = [...state.users.map( user => {
                if(user.id === action.user_id){
                    return {...user, visits: action.visits.reverse(), visits_count: action.count_visits}
                }
                return user
            })]
            return {...state, users}
        }
        case ADD_VISIT: {
            let users = [...state.users.map( user => {
                if(user.id === action.user_id){
                    return {
                        ...user,
                        visits: [action.visit, ...user.visits],
                        visits_count: user.visits_count + 1
                    }
                }
                return user
            })]
            return {...state, users}
        }
        case ADD_USER: {
            return {...state, users: [action.user, ...state.users], count_users: state.count_users + 1}
        }
        case ADD_USERS: {
            return {...state, users: [...state.users, ...action.users.reverse()]}
        }
        case ADD_VISITS: {
            let users = [...state.users.map( user => {
                if(user.id === action.user_id){
                    return {...user, visits: [...user.visits, ...action.visits.reverse()]}
                }
                return user
            })]
            return {...state, users}
        }
        default: return state
    }
}

export const setUsers = (usersData, count_users) => ({type: SET_USERS, users: usersData, count_users})
export const setVisits = (user_id, visits, count_visits) => ({type: SET_VISITS, user_id, visits, count_visits})
export const addVisit = (user_id, visit) => ({type: ADD_VISIT, user_id, visit})
export const addUser = (userData) => ({type: ADD_USER, user: userData})
export const addUsers = (users) => ({type: ADD_USERS, users})
export const addVisits = (visits, user_id) => ({type: ADD_VISITS, visits, user_id})


export const addUsersQuantity = (ws, showed_users_count, all_users_count) => {
    if(all_users_count - showed_users_count < 10){
        ws.send(JSON.stringify({event: 'show_more_users', count: showed_users_count,
                                     limit: all_users_count - showed_users_count}))
    }
    else{
        ws.send(JSON.stringify({event: 'show_more_users', count: showed_users_count}))
    }
}

export const addVisitsQuantity = (ws, userId, showed_visits_count, all_visits_count) => {
    if(all_visits_count - showed_visits_count < 10){
        ws.send(JSON.stringify({event: 'show_more_visits', user_id: userId, count: showed_visits_count,
                                      limit: all_visits_count - showed_visits_count}))
    }
    else{
        ws.send(JSON.stringify({event: 'show_more_visits', user_id: userId, count: showed_visits_count}))
    }
}


export default usersReducer;
