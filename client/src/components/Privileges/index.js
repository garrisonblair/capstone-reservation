import React, { Component } from 'react';
import { Table } from 'semantic-ui-react';
import api from '../../utils/api';
import './Privileges.scss';

class Privileges extends Component {
  state = {
    privileges: [],
  }

  componentDidMount() {
    api.getMyPrivileges()
      .then((r) => {
        if (r.status === 200) {
          this.setState({ privileges: r.data });
        }
      });
  }

  renderMaximumRecurringBookings = () => {
    let content = null;
    const { privileges } = this.state;
    if (privileges.can_make_recurring_booking === true) {
      content = (
        <Table.Row>
          <Table.Cell textAlign="left">Maximum recurring bookings</Table.Cell>
          <Table.Cell>{privileges.max_recurring_bookings}</Table.Cell>
        </Table.Row>
      );
    }
    return content;
  }

  render() {
    const { privileges } = this.state;
    return (
      <div id="privileges">
        <h1> My Privileges </h1>
        <Table collapsing>
          <Table.Header>
            <Table.Row>
              <Table.HeaderCell>Definition</Table.HeaderCell>
              <Table.HeaderCell>Value</Table.HeaderCell>
            </Table.Row>
          </Table.Header>
          <Table.Body>
            <Table.Row>
              <Table.Cell textAlign="left">Maximum days until booking</Table.Cell>
              <Table.Cell>{privileges.max_days_until_booking}</Table.Cell>
            </Table.Row>
            <Table.Row>
              <Table.Cell textAlign="left">Maximum days with bookings</Table.Cell>
              <Table.Cell>{privileges.max_num_days_with_bookings}</Table.Cell>
            </Table.Row>
            <Table.Row>
              <Table.Cell textAlign="left">Maximum bookings for date</Table.Cell>
              <Table.Cell>{privileges.max_num_bookings_for_date}</Table.Cell>
            </Table.Row>
            <Table.Row>
              <Table.Cell textAlign="left">Booking start time</Table.Cell>
              <Table.Cell>{privileges.booking_start_time}</Table.Cell>
            </Table.Row>
            <Table.Row>
              <Table.Cell textAlign="left">Booking end time</Table.Cell>
              <Table.Cell>{privileges.booking_end_time}</Table.Cell>
            </Table.Row>
            <Table.Row>
              <Table.Cell textAlign="left">Recurring bookings</Table.Cell>
              <Table.Cell>{privileges.can_make_recurring_booking ? 'True' : 'False'}</Table.Cell>
            </Table.Row>
            {this.renderMaximumRecurringBookings()}
          </Table.Body>
        </Table>
      </div>
    );
  }
}

export default Privileges;
