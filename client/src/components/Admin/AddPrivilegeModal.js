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
    recurringBookingPermission: false,
    bookingStartTime: '06:00:00',
    bookingEndTime: '00:00:00'
  }

  handleInputChange = (state, e) => {
    this.setState({
      [`${state}`]: e.target.value
    })
  }

  handleSubmit = (e) => {
    const {name, parent, maxDaysUntilBooking, maxBookings, maxRecurringBookings, recurringBookingPermission, bookingStartTime, bookingEndTime} = this.state;
    let data = {
      name,
      parent_category: '',
      max_day_until_booking: maxDaysUntilBooking,
      max_bookings: maxBookings,
      max_recurring_bookings: maxRecurringBookings,
      can_make_recurring_booking: recurringBookingPermission,
      booking_start_time: bookingStartTime,
      booking_end_time: bookingEndTime
    }

    // TEST DATA
    // data = {
    //   "name": "Second Tier",
    //   "parent_category": 'null',
    //   "max_days_until_booking": '',
    //   "can_make_recurring_booking": true,
    //   "max_bookings": 2,
    //   "max_recurring_bookings": 3
    // }

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
            icon='text cursor'
            iconPosition='left'
            placeholder='Name'
            onChange={(e) => this.handleInputChange('name', e)}
          />
        </Form.Field>
        <Form.Field>
          <Input
            fluid
            size='small'
            icon='sort'
            iconPosition='left'
            placeholder='Max Days Until Booking'
            type='number'
            min='0'
            onChange={(e) => this.handleInputChange('maxDaysUntilBooking', e)}
          />
        </Form.Field>
        <Form.Field>
          <Input
            fluid
            size='small'
            icon='sort'
            iconPosition='left'
            placeholder='Max Bookings'
            type='number'
            min='0'
            onChange={(e) => this.handleInputChange('maxBookings', e)}
          />
        </Form.Field>
        <Form.Field>
          <Input
            fluid
            size='small'
            icon='sort'
            iconPosition='left'
            placeholder='Max Recurring Bookings'
            type='number'
            min='0'
            onChange={(e) => this.handleInputChange('maxRecurringBookings', e)}
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

