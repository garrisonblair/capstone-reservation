import React, { Component } from 'react';
import { Table, Segment } from 'semantic-ui-react';
import api from '../../utils/api';
import './Privileges.scss';

class Privileges extends Component {
  state = {
    privileges: [],
    isLoading: false,
    groups: [],
  }

  componentDidMount() {
    this.setState({ isLoading: true });
    api.getMyPrivileges()
      .then((r) => {
        this.setState({ isLoading: false });
        if (r.status === 200) {
          this.setState({ privileges: r.data });
        }
      });
  }

  getOwnerGroups = () => {
    const ownerGroups = [{ key: 'me', value: 'me', text: 'me' }];
    api.getMyGroups()
      .then((r) => {
        // eslint-disable-next-line array-callback-return
        r.data.map((g) => {
          ownerGroups.push({ key: g.id, value: g.id, text: `${g.name} (group)` });
          this.setState({
            groups: ownerGroups,
          });
        });
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
    const { privileges, isLoading } = this.state;
    return (
      <div id="privileges">
        <h1> My Privileges </h1>
        <Segment loading={isLoading}>
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
                <Table.Cell>{privileges.can_make_recurring_booking ? 'Yes' : 'No'}</Table.Cell>
              </Table.Row>
              {this.renderMaximumRecurringBookings()}
            </Table.Body>
          </Table>
        </Segment>
      </div>
    );
  }
}

export default Privileges;
