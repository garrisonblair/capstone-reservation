import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Table, TableBody } from 'semantic-ui-react';


class CampOns extends Component {
  renderTableHeader = () => {
    // const headers = ['Room', 'Date', 'Start', 'End', 'Group'];
    const headers = ['Start', 'End'];
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
    const { campOns } = this.props;
    let component = [];

    if (campOns.length === 0) {
      return component;
    }

    component = campOns.map((booking, index) => (
      // eslint-disable-next-line react/no-array-index-key
      <Table.Row key={index}>
        {/* <Table.Cell>
          {booking.room.name}
        </Table.Cell> */}
        {/* <Table.Cell>
          {booking.date}
        </Table.Cell> */}
        <Table.Cell>
          {booking.start_time}
        </Table.Cell>
        <Table.Cell>
          {booking.end_time}
        </Table.Cell>
        {/* <Table.Cell>
          {booking.group}
        </Table.Cell> */}
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

CampOns.propTypes = {
  campOns: PropTypes.instanceOf(Object).isRequired,
};

export default CampOns;
