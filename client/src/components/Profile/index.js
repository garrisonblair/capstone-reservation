/* eslint-disable no-console */
/* eslint-disable react/prefer-stateless-function */
import React, { Component } from 'react';
import {
  Segment,
} from 'semantic-ui-react';
import Navigation from '../Navigation';
import Groups from '../Groups';
import Privileges from '../Privileges';
// import api from '../../utils/api';
import './Profile.scss';

// TODO: Add Bookings

class Profile extends Component {
  // componentDidMount() {
  //   api.getBookings()
  //     .then((response) => {
  //       console.log(response);
  //     });
  // }

  render() {
    return (
      <div>
        <Navigation />
        <div className="profile">
          <h1> Profile </h1>
          <Segment>
            <Privileges />
          </Segment>
          <Segment>
            <Groups />
            {/* Group invivations */}
          </Segment>
        </div>
      </div>
    );
  }
}

export default Profile;
