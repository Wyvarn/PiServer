/**
 * @author lusinabrian on 05/06/17.
 * @notes: action to begin ajax call
 */
import * as types from '../constants/actionTypes';

export function beginAjaxCall(){
    return {type: types.BEGIN_AJAX_CALL};
}

export function ajaxCallError(){
    return {type: types.AJAX_CALL_ERROR};
}

