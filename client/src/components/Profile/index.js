/* eslint-disable react/prefer-stateless-function */
import React, { Component } from 'react';
import {
  Segment,
} from 'semantic-ui-react';
import Navigation from '../Navigation';
import UserInfo from '../UserInfo';
import Privileges from '../Privileges';
import UserBookings from '../UserBookings';
import Groups from '../Groups';
import GroupInvitations from '../GroupInvitations';
import AuthenticationRequired from '../HOC/AuthenticationRequired';
import './Profile.scss';


class Profile extends Component {
  render() {
    return (
      <div>
        <Navigation />
        <div className="profile">
          <h1> Profile </h1>
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
              <Privileges />
            </Segment>
            <Segment className="segment__groups">
              <Groups />
            </Segment>
            <Segment className="segment__invitations">
              <GroupInvitations />
            </Segment>
          </div>
        </div>
      </div>
    );
  }
}

export default AuthenticationRequired(Profile);
