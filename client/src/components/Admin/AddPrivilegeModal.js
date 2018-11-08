import React, {Component} from 'react';
import {Button, Form, Header, Icon, Input, Modal} from 'semantic-ui-react';
import api from '../../utils/api';
import './AddPrivilegeModal.scss';


class AddPrivilegeModal extends Component {

  state = {
    name: '',
    parent: '',
    maxDaysUntilBooking: 0,
    maxBookings: 0,
    maxRecurringBookings: 0,
    bookingPermission: false,
    bookingStartTime: '06:00:00',
    bookingEndTime: '00:00:00'
  }

  handleNameChange = (e) => {
    this.setState({
      name: e.target.value
    })
  }

  handleSubmit = (e) => {
    const {name, parent, maxDaysUntilBooking, maxBookings, maxRecurringBookings, bookingPermission, bookingStartTime, bookingEndTime} = this.state;
    let data = {
      name,
      parent_category: '',
      max_day_until_booking: maxDaysUntilBooking,
      max_bookings: maxBookings,
      max_recurring_bookings: maxRecurringBookings,
      booking_start_time: bookingStartTime,
      booking_end_time: bookingEndTime
    }

    api.createPrivilege(data)
    .then((response) => {
      console.log(response);
    })
    this.props.onClose();
  }

  renderForm() {
    return (
      <div>
        <Form.Field>
          <Input
            fluid
            size='small'
            icon='user'
            iconPosition='left'
            placeholder='Name'
            onChange={this.handleNameChange}
          />
        </Form.Field>
      </div>
    )
  }

  render() {
    return (
      <Modal className="privilege-modal" open={this.props.show} onClose={this.props.onClose}>
        <Header>
          <Icon name='plus'/> Add Privilege
        </Header>
        <div className="privilege-modal__container">
          <div className="ui divider"/>
          {this.renderForm()}
          <div className="ui divider"/>
          <Form.Field>
            <Button fluid size='small' icon onClick={this.handleSubmit}>
              Add
            </Button>
          </Form.Field>
        </div>
      </Modal>
    )
  }
}

export default AddPrivilegeModal;

