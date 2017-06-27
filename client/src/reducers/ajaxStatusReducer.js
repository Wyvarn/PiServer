/**
 * @author lusinabrian on lusinabrian.
 * @notes: ajaxStatusReducer reducer
 */

import * as types from '../constants/actionTypes';
import initialState from './initialState';


function actionTypeEndsInSuccess(type) {
    return type.substring(type.length - 8) === "_SUCCESS";
}

/**
 * ajaxStatusReducer reducer takes current state and action and
 * returns a new state
 * @param state initial state of the application store
 * @param action function to dispatch to store
 * @return {Object} new state or initial state*/
export default function ajaxStatusReducer(state = initialState.ajaxCallsInProgress, action) {
    if(action.type === types.BEGIN_AJAX_CALL){
        return state + 1;
    }else if(action.type === types.AJAX_CALL_ERROR || actionTypeEndsInSuccess(action.type)){
        return state - 1;
    }
    return state;
}
