import React from 'react';
import ReactDOM from 'react-dom';
import {HashRouter as Router, Route, Switch} from 'react-router-dom';
import Home from './components/Home';
import Login from './components/Login';
import NotFound from './components/NotFound';
import ReservationDetailsModal from './components/ReservationDetailsModal';


ReactDOM.render(
    <Router>
    <div>
      <Switch>
        <Route exact path="/" component={Home}/>
        <Route exact path="/login" component={Login}/>

        {/* This Route is only for development testing. Remove after.*/}
<Route exact path="/andresModal" render={() => <ReservationDetailsModal date ={new Date()} defaultHour={8} defaultMinute={30} roomNumber={1}/>}/>

        <Route component={NotFound}/>
      </Switch>
    </div>
    </Router>,
    document.getElementById('root')
)
