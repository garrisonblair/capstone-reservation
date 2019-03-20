import React from 'react';
import ReactDOM from 'react-dom';
import ReactGA from 'react-ga';
import { HashRouter as Router, Route, Switch } from 'react-router-dom';
import settings from './config/settings';
import api from './utils/api';
import storage from './utils/local-storage';
import NotFound from './components/NotFound';
// Admin
import Admin from './components/Admin';
import Settings from './components/Admin/Settings';
import Announcements from './components/Admin/Announcements';
import Bookers from './components/Admin/Bookers';
import PrivilegeCategory from './components/Admin/PrivilegeCategory';
import GroupPrivilegeRequest from './components/Admin/GroupPrivilegeRequest';
import RoomManager from './components/Admin/RoomManager';
import Stats from './components/Admin/Stats';
import BookingActivity from './components/Admin/Logs/BookingActivity';
import DatabaseDump from './components/Admin/DatabaseDump';
// Users
import Registration from './components/Registration';
import ResetPassword from './components/ResetPassword';
import Verification from './components/Verification';
import ResetPasswordVerification from './components/ResetPasswordVerification';
import Home from './components/Home';
import HomeMobile from './components/Mobile/Home';
import HomeDisplay from './components/HomeDisplay';
import Dashboard from './components/Dashboard';
import Profile from './components/Profile';

function renderPage() {
  ReactDOM.render(
    <Router>
      <div>
        <Switch>
          <Route exact path="/" component={Home} />
          <Route exact path="/mobile_home" component={HomeMobile} />
          <Route exact path="/forDisplay" component={HomeDisplay} />
          <Route exact path="/registration" component={Registration} />
          <Route exact path="/resetPassword" component={ResetPassword} />
          <Route exact path="/verify/:token" component={Verification} />
          <Route exact path="/verifyReset/:token" component={ResetPasswordVerification} />
          <Route exact path="/admin" render={() => <Admin menuType="settings" content={<Settings />} />} />
          <Route exact path="/admin/settings" render={() => <Admin menuType="settings" content={<Settings />} />} />
          <Route exact path="/admin/announcements" render={() => <Admin menuType="announcements" content={<Announcements />} />} />
          <Route exact path="/admin/bookers" render={() => <Admin menuType="bookers" content={<Bookers />} />} />
          <Route exact path="/admin/privileges" render={() => <Admin menuType="privileges" content={<PrivilegeCategory />} />} />
          <Route exact path="/admin/privileges/requests" render={() => <Admin menuType="group-privilege-request" content={<GroupPrivilegeRequest />} />} />
          <Route exact path="/admin/rooms" render={() => <Admin menuType="rooms" content={<RoomManager />} />} />
          <Route exact path="/admin/stats" render={() => <Admin menuType="stats" content={<Stats />} />} />
          <Route exact path="/admin/logs" render={() => <Admin menuType="logs" content={<BookingActivity />} />} />
          <Route exact path="/admin/databasedump" render={() => <Admin menuType="databasedumps" content={<DatabaseDump />} />} />
          <Route exact path="/dashboard" component={Dashboard} />
          <Route exact path="/profile" render={() => <Profile asPage />} />
          <Route component={NotFound} />
        </Switch>
      </div>
    </Router>,
    document.getElementById('root'),
  );
}

if (settings.IS_PROD) {
  ReactGA.initialize(settings.gaTrackingID);
}

const user = storage.getUser();
if (user) {
  api.getUserBookings(user.id)
    .then(() => {
      renderPage();
    })
    .catch(() => {
      localStorage.removeItem('CapstoneReservationUser');
      renderPage();
    });
} else {
  renderPage();
}
