/* eslint-disable react/prefer-stateless-function */
import React, { Component } from 'react';
import {
  Segment,
} from 'semantic-ui-react';
import withTracker from '../HOC/withTracker';
import Navigation from '../Navigation';
import UserInfo from '../UserInfo';
import Privileges from '../Privileges';
import UserBookings from '../UserBookings';
import Groups from '../Groups';
import GroupInvitations from '../GroupInvitations';
import AuthenticationRequired from '../HOC/AuthenticationRequired';
import './Dashboard.scss';

class Dashboard extends Component {
  groupRef = React.createRef();

  syncGroups = () => {
    this.groupRef.current.syncGroups();
  };

  render() {
    return (
      <div>
        <Navigation />
        <div className="dashboard">
          <h1 className="title"><center> Dashboard </center></h1>
          <div className="segment__container top">
            <Segment className="segment__user">
              <UserInfo />
            </Segment>
            <Segment className="segment__bookings">
              <UserBookings />
            </Segment>
          </div>
          <div className="segment__container bottom">
            <Segment className="segment__privileges">
              <Privileges showTitle />
            </Segment>
            <Segment className="segment__groups">
              <Groups showTitle ref={this.groupRef} />
            </Segment>
            <Segment className="segment__invitations">
              <GroupInvitations showTitle syncGroups={this.syncGroups} />
            </Segment>
          </div>
        </div>
      </div>
    );
  }
}

export default withTracker(AuthenticationRequired(Dashboard));
