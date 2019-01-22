import React from 'react';
import ReactDOM from 'react-dom';
import { HashRouter as Router, Route, Switch } from 'react-router-dom';
import Home from './components/Home';
// import Login from './components/Login';
import NotFound from './components/NotFound';
import Registration from './components/Registration';
import Verification from './components/Verification';
import Admin from './components/Admin';
import PrivilegeCategory from './components/Admin/PrivilegeCategory';
import RoomManager from './components/Admin/RoomManager';
import Stats from './components/Admin/Stats';
import BookingActivity from './components/Admin/Stats/BookingActivity';
import Settings from './components/Admin/Settings';
import Groups from './components/Groups';
import Bookers from './components/Admin/Bookers';
import Privileges from './components/Privileges';


ReactDOM.render(
  <Router>
    <div>
      <Switch>
        <Route exact path="/" component={Home} />
        {/* <Route exact path="/login" component={Login} /> */}
        <Route exact path="/registration" component={Registration} />
        <Route exact path="/verify/:token" component={Verification} />
        <Route exact path="/admin" render={() => <Admin menuType="settings" content={<Settings />} />} />
        <Route exact path="/admin/settings" render={() => <Admin menuType="settings" content={<Settings />} />} />
        <Route exact path="/admin/privileges" render={() => <Admin menuType="privileges" content={<PrivilegeCategory />} />} />
        <Route exact path="/admin/rooms" render={() => <Admin menuType="rooms" content={<RoomManager />} />} />
        <Route exact path="/myGroups" component={Groups} />
        <Route exact path="/admin/logs" render={() => <Admin menuType="logs" content={<BookingActivity />} />} />
        <Route exact path="/admin/stats" render={() => <Admin menuType="stats" content={<Stats />} />} />
        <Route exact path="/admin/bookers" render={() => <Admin menuType="bookers" content={<Bookers />} />} />
        <Route exact path="/privileges" component={Privileges} />
        <Route component={NotFound} />
      </Switch>
    </div>
  </Router>,
  document.getElementById('root'),
);
