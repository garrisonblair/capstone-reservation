import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Table, TableBody } from 'semantic-ui-react';
import EmptySegment from './EmptySegment';


class CampOns extends Component {
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
    const { campOns, allBookings, rooms } = this.props;
    let component = [];

    if (campOns.length === 0) {
      return component;
    }

    const bookingsLookup = allBookings.reduce((obj, booking) => {
      // eslint-disable-next-line no-param-reassign
      obj[booking.id] = {
        room: booking.room,
        date: booking.date,
        start_time: booking.start_time,
        end_time: booking.end_time,
        group: booking.group,
      };
      return obj;
    });

    const roomsLookup = rooms.reduce((obj, room) => {
      // eslint-disable-next-line no-param-reassign
      obj[room.id] = {
        name: room.name,
      };
      return obj;
    });

    component = campOns.map((campOn, index) => (
      // eslint-disable-next-line react/no-array-index-key
      <Table.Row key={index}>
        <Table.Cell>
          {roomsLookup[bookingsLookup[`${campOn.camped_on_booking}`].room].name}
        </Table.Cell>
        <Table.Cell>
          {bookingsLookup[`${campOn.camped_on_booking}`].date}
        </Table.Cell>
        <Table.Cell>
          {campOn.start_time}
        </Table.Cell>
        <Table.Cell>
          {campOn.end_time}
        </Table.Cell>
        <Table.Cell>
          {bookingsLookup[`${campOn.camped_on_booking}`].group}
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
    const { campOns } = this.props;
    let component = (
      <div>
        <Table>
          {this.renderTableHeader()}
          {this.renderTableBody()}
        </Table>
      </div>
    );

    if (campOns.length === 0) {
      component = (
        <EmptySegment message="No Camp Ons" />
      );
    }
    return component;
  }
}

CampOns.propTypes = {
  rooms: PropTypes.instanceOf(Object).isRequired,
  allBookings: PropTypes.instanceOf(Object).isRequired,
  campOns: PropTypes.instanceOf(Object).isRequired,
};

export default CampOns;
