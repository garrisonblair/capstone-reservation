import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Table, TableBody } from 'semantic-ui-react';


class RecurringBookings extends Component {
  renderTableHeader = () => {
    const headers = ['Room', 'Start Date', 'End Date', 'Start Time', 'End Time', 'Group'];
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
    const { bookings } = this.props;
    let component = [];

    if (bookings.length === 0) {
      return component;
    }

    component = bookings.map((booking, index) => (
      // eslint-disable-next-line react/no-array-index-key
      <Table.Row key={index}>
        <Table.Cell>
          {booking.room.name}
        </Table.Cell>
        <Table.Cell>
          {booking.start_date}
        </Table.Cell>
        <Table.Cell>
          {booking.end_date}
        </Table.Cell>
        <Table.Cell>
          {booking.booking_start_time}
        </Table.Cell>
        <Table.Cell>
          {booking.booking_end_time}
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
        <Table>
          {this.renderTableHeader()}
          {this.renderTableBody()}
        </Table>
      </div>
    );
  }
}

RecurringBookings.propTypes = {
  bookings: PropTypes.instanceOf(Object).isRequired,
};

export default RecurringBookings;
