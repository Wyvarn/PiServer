/**
 * @author lusinabrian on 28/06/17
 * @notes: Root reducer
 */

import {combineReducers} from 'redux';
import ajaxCallsInProgress from './ajaxStatusReducer';

/**
 * Combines all reducers for use in the application
 * Uses short hand property names from ES6
 * */
const rootReducer = combineReducers({
    ajaxCallsInProgress
});

export default rootReducer;
