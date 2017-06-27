import React, { Component } from 'react';
import logo from '../images/logo.svg';
import {Router, Route, withRouter} from 'react-router-dom';
import createHistory from 'history/createBrowserHistory';
import { connect } from 'react-redux';

const history = createHistory();


class App extends Component {
  render() {
    return (
      <div className="App">
        <div className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h2>Welcome to React</h2>
        </div>
          <Router history={history}>
              <div>

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
