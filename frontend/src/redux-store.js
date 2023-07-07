import thunk from "redux-thunk";
import usersReducer from "./user-reducer";
import {applyMiddleware, combineReducers, createStore} from "redux";

const reducers = combineReducers({
    users: usersReducer,
})

export const store = createStore(reducers, applyMiddleware(thunk))

window.store = store;

export default store;