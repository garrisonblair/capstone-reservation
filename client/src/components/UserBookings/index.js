/* eslint-disable no-console */
/* eslint-disable react/no-unused-state */
/* eslint-disable no-unused-vars */
import React, { Component } from 'react';
// import PropTypes from 'prop-types';
import {
  Table, TableBody,
} from 'semantic-ui-react';
import api from '../../utils/api';
import storage from '../../utils/local-storage';
import Bookings from './Bookings';


class UserBookings extends Component {
  state = {
    bookings: [],
    recurringBookings: [],
    campOns: [],
  }

  componentDidMount() {
    const user = storage.getUser();
    api.getUserBookings(user.id)
      .then(({ data }) => data)
      .then((data) => {
        const {
          campons: campOns,
          recurring_bookings: recurringBookings,
          standard_bookings: bookings,
        } = data;
        this.setState({
          campOns,
          recurringBookings,
          bookings,
        });
      });
  }

  render() {
    const { bookings } = this.state;
    return (
      <div>
        <Bookings bookings={bookings} />
      </div>
    );
  }
}

export default UserBookings;
