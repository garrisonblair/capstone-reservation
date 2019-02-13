import React, { Component } from 'react';
import {
  Button, Checkbox, Table, Loader,
} from 'semantic-ui-react';
// import PropTypes from 'prop-types';

class EmailSettings extends Component {
  state = {
    bookingReminder: false,
    recurringBookingReminder: false,
    isLoading: false,
  }

  componentDidMount() {

  }

  handleBookingReminderOnToggle = (e, data) => {
    this.setState({
      bookingReminder: data.checked,
      isLoading: true,
    });
    // this.setState({ isLoading: false });
  }

  handleRecurringBookingOnToggle = (e, data) => {
    this.setState({ recurringBookingReminder: data.checked, isLoading: false });
  }

  render() {
    const { bookingReminder, recurringBookingReminder, isLoading } = this.state;
    console.log(bookingReminder);
    return (
      <div id="email-settings">
        <h1>Email Settings</h1>
        <Table celled collapsing>
          <Table.Header>
            <Table.Row>
              <Table.HeaderCell>Email feature</Table.HeaderCell>
              <Table.HeaderCell />
            </Table.Row>
          </Table.Header>
          <Table.Body>
            <Table.Row>
              <Table.Cell>Receive email reminder for booking</Table.Cell>
              <Table.Cell collapsing>
                {isLoading ? <Loader active inline size="small" /> : (
                  <Checkbox
                    toggle
                    checked={bookingReminder}
                    onChange={this.handleBookingReminderOnToggle}
                  />)}
              </Table.Cell>
            </Table.Row>
            <Table.Row>
              <Table.Cell>Receive email reminder for recurring booking</Table.Cell>
              <Table.Cell collapsing>
                <Checkbox
                  toggle
                  checked={recurringBookingReminder}
                  onChange={this.handleRecurringBookingOnToggle}
                />
              </Table.Cell>
            </Table.Row>
          </Table.Body>
        </Table>
        <Button>Turn all OFF</Button>
        <Button>Turn all ON</Button>
      </div>
    );
  }
}

export default EmailSettings;
