import React, { Component } from 'react';
// import PropTypes from 'prop-types';
import {
  Table, TableBody,
} from 'semantic-ui-react';
import api from '../../utils/api';


class UserBookings extends Component {
  state = {
    bookings: [],
  }

  componentDidMount() {
    api.getBookings()
      .then((response) => {
        const { data: bookings } = response;
        this.setState({
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
    let rows = [];
    rows = bookings.map((booking, index) => (
      // eslint-disable-next-line react/no-array-index-key
      <Table.Row key={index}>
        <Table.Cell>
          {booking.room}
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
        {rows}
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
