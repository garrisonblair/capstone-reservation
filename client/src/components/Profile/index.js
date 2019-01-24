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
import AuthenticationRequired from '../HOC/AuthenticationRequired';
import './Profile.scss';


class Profile extends Component {
  render() {
    return (
      <div>
        <Navigation />
        <div className="profile">
          <h1> Profile </h1>
          <Segment.Group horizontal compact className="segment__container">
            <Segment className="segment__user">
              <UserInfo />
            </Segment>
            <Segment className="segment__bookings">
              <UserBookings />
            </Segment>
          </Segment.Group>
          <Segment.Group horizontal compact className="segment__container">
            <Segment className="segment__privileges">
              <Privileges />
            </Segment>
            <Segment className="segment__groups">
              <Groups />
            </Segment>
            <Segment className="segment__invitations">
              {/* Group invivations */}
            </Segment>
          </Segment.Group>
        </div>
      </div>
    );
  }
}

export default AuthenticationRequired(Profile);
