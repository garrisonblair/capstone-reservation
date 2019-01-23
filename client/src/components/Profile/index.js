/* eslint-disable react/prefer-stateless-function */
import React, { Component } from 'react';
import {
  Segment,
} from 'semantic-ui-react';
import Navigation from '../Navigation';
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
          <Segment.Group horizontal compact>
            <Segment>
              <Privileges />
            </Segment>
            <Segment>
              <UserBookings />
            </Segment>
          </Segment.Group>
          <Segment.Group horizontal compact>
            <Segment>
              <Groups />
            </Segment>
            <Segment>
              {/* Group invivations */}
            </Segment>
          </Segment.Group>
        </div>
      </div>
    );
  }
}

export default AuthenticationRequired(Profile);
