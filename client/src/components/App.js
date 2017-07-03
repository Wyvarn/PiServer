import React, { Component } from 'react';
import logo from '../images/logo.svg';
import {Router, Route, withRouter} from 'react-router-dom';
import createHistory from 'history/createBrowserHistory';
import Home from './home/HomePage';
import { connect } from 'react-redux';

const history = createHistory();


class App extends Component {
  render() {
    return (
      <div className="App">
          <Router history={history}>
              <div>
                  <Route path="home" component={Home}/>
              </div>
          </Router>
      </div>
    );
  }
}


function mapStateToProps(state, ownProps){
    return{
        loading: state.ajaxCallsInProgress > 0
    };
}

const container = connect(mapStateToProps)(App);

export default withRouter(container);
