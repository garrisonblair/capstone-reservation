import React, { Component } from 'react';
import PropTypes from 'prop-types';
import {
  Table,
  TableBody,
} from 'semantic-ui-react';
import EmptySegment from '../EmptySegment';
import RecurringBookingModal from '../RecurringBookingModal';


class RecurringBookings extends Component {
  state = {
    showRecurringModal: false,
    booking: null,
  }

  closeModal = () => {
    this.setState({ showRecurringModal: false });
  }

  openRecurringModal = (booking) => {
    this.setState({ booking }, () => {
      this.setState({ showRecurringModal: true });
    });
  }

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
    const component = bookings.map((booking, index) => (
      // eslint-disable-next-line react/no-array-index-key
      <Table.Row key={index} onClick={() => this.openRecurringModal(booking)}>
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
    const { showRecurringModal, booking } = this.state;
    let component = (
      <div>
        <Table>
          {this.renderTableHeader()}
          {this.renderTableBody()}
        </Table>
        {showRecurringModal === true
          ? (
            <RecurringBookingModal
              show={showRecurringModal}
              booking={booking}
              onClose={this.closeModal}
            />)
          : null}
      </div>
    );

    if (bookings.length === 0) {
      component = (
        <EmptySegment message="No Recurring Bookings" />
      );
    }
    return component;
  }
}

RecurringBookings.propTypes = {
  bookings: PropTypes.instanceOf(Object).isRequired,
};

export default RecurringBookings;
