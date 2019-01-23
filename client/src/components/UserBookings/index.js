import React, { Component } from 'react';
// import PropTypes from 'prop-types';
import api from '../../utils/api';


// eslint-disable-next-line react/prefer-stateless-function
class UserBookings extends Component {
  componentDidMount() {
    api.getBookings()
      .then((response) => {
        const { data } = response;
        // eslint-disable-next-line no-console
        console.log(data);
      });
  }

  render() {
    return (
      <div>
        <h1> Bookings </h1>
      </div>
    );
  }
}

export default UserBookings;
