import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Table, TableBody } from 'semantic-ui-react';
import EmptySegment from '../EmptySegment';


class Bookings extends Component {
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
          {booking.date}
        </Table.Cell>
        <Table.Cell>
          {booking.start_time}
        </Table.Cell>
        <Table.Cell>
          {booking.end_time}
        </Table.Cell>
        <Table.Cell>
          {booking.group === null ? '' : booking.group.name}
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
    const { bookings } = this.props;
    let component = (
      <div>
        <Table unstackable>
          {this.renderTableHeader()}
          {this.renderTableBody()}
        </Table>
      </div>
    );

    if (bookings.length === 0) {
      component = (
        <EmptySegment message="No Bookings" />
      );
    }
    return component;
  }
}

Bookings.propTypes = {
  bookings: PropTypes.instanceOf(Object).isRequired,
};

export default Bookings;
