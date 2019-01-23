/* eslint-disable no-console */
/* eslint-disable react/prefer-stateless-function */
import React, { Component } from 'react';
import {
  Segment,
} from 'semantic-ui-react';
import Navigation from '../Navigation';
import Groups from '../Groups';
import Privileges from '../Privileges';
import AuthenticationRequired from '../HOC/AuthenticationRequired';
import api from '../../utils/api';
import './Profile.scss';

// TODO: Add Bookings

class Profile extends Component {
  componentDidMount() {
    api.getBookings()
      .then((response) => {
        const { data } = response;
        console.log(data);
      });
  }

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
              {/* Bookings */}
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
