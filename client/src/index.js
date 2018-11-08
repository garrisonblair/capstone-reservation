import React from 'react';
import ReactDOM from 'react-dom';
import {HashRouter as Router, Route, Switch} from 'react-router-dom';
import Home from './components/Home';
import Login from './components/Login';
import NotFound from './components/NotFound';
import Registration from './components/Registration';
import Verification from './components/Verification';
import Admin from './components/Admin';
import PrivilegeCategory from './components/Admin/PrivilegeCategory';
import Stats from './components/Admin/Stats';


ReactDOM.render(
    <Router>
    <div>
      <Switch>
        <Route exact path="/" component={Home}/>
        <Route exact path="/login" component={Login}/>
        <Route exact path="/registration" component={Registration}/>
        <Route exact path="/verify/:token" component={Verification}/>
        <Route exact path="/admin" component={Admin}/>
        <Route exact path="/admin/settings" component={Admin}/>
        <Route exact path="/admin/privileges" component={PrivilegeCategory}/>
        <Route exact path="/admin/stats" component={Stats}/>
        <Route component={NotFound}/>
      </Switch>
    </div>
    </Router>,
    document.getElementById('root')
)
