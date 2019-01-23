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


class UserBookings extends Component {
  state = {
    bookings: [],
    recurringBookings: [],
    CampOns: [],
  }

  componentDidMount() {
    const user = storage.getUser();
    api.getUserBookings(user.id)
      .then(({ data }) => data)
      .then((data) => {
        const {
          campons: CampOns,
          recurring_bookings: recurringBookings,
          standard_bookings: bookings,
        } = data;
        this.setState({
          CampOns,
          recurringBookings,
          bookings,
        });
      });
  }

  renderTableHeader = () => {
    const headers = ['Room', 'Date', 'Start', 'End', 'Group'];
    let component = [];
    component = headers.map((header, index) => (
      // eslint-disable-next-line react/no-array-index-key
      <Table.HeaderCell key={index}>
        {header}
      </Table.HeaderCell>
    ));

    return (
      <Table.Header>
        <Table.Row>
          {component}
        </Table.Row>
      </Table.Header>
    );
  }

  renderTableBody = () => {
    const { bookings } = this.state;
    let component = [];

    if (bookings.length === 0) {
      return component;
    }

    console.log(bookings);
    component = bookings.map((booking, index) => (
      // eslint-disable-next-line react/no-array-index-key
      <Table.Row key={index}>
        <Table.Cell>
          {booking.room.name}
        </Table.Cell>
        <Table.Cell>
          {booking.date}
        </Table.Cell>
        <Table.Cell>
          {booking.start_time}
        </Table.Cell>
        <Table.Cell>
          {booking.end_time}
        </Table.Cell>
        <Table.Cell>
          {booking.group}
        </Table.Cell>
      </Table.Row>
    ));
    return (
      <TableBody>
        {component}
      </TableBody>
    );
  }

  render() {
    return (
      <div>
        <h1> Bookings </h1>
        <Table>
          {this.renderTableHeader()}
          {this.renderTableBody()}
        </Table>
      </div>
    );
  }
}

export default UserBookings;
