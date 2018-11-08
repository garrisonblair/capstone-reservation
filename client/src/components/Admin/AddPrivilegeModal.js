import React, {Component} from 'react';
import {Button, Checkbox, Dropdown, Form, Header, Icon, Input, Modal, FormField} from 'semantic-ui-react';
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
    bookingStartTime: '',
    bookingEndTime: ''
  }

  handleInputChange = (state, e) => {
    this.setState({
      [`${state}`]: e.target.value
    })
  }

  handleParentPrivilegeChange = (e, data) => {
    this.setState({
      parent: data.value
    })
  }

  handleRecurringBookingPermission = (e, data) => {
    const {checked} = data;
    this.setState({
      recurringBookingPermission: checked
    })
  }

  handleSubmit = (e) => {
    const {name, parent, maxDaysUntilBooking, maxBookings, maxRecurringBookings, recurringBookingPermission, bookingStartTime, bookingEndTime} = this.state;
    let data = {
      name,
      parent_category: parent,
      max_day_until_booking: maxDaysUntilBooking,
      max_bookings: maxBookings,
      max_recurring_bookings: maxRecurringBookings,
      can_make_recurring_booking: recurringBookingPermission,
      booking_start_time: bookingStartTime,
      booking_end_time: bookingEndTime
    }

    console.log(data);

    // TEST DATA
    // data = {
    //   "name": "Second Tier",
    //   "parent_category": 'null',
    //   "max_days_until_booking": '',
    //   "can_make_recurring_booking": true,
    //   "max_bookings": 2,
    //   "max_recurring_bookings": 3
    // }

    // api.createPrivilege(data)
    // .then((response) => {
    //   console.log(response);
    // })
    // this.props.onClose();
  }

  renderForm() {
    const {privileges} = this.props;
    const {recurringBookingPermission, bookingStartTime, bookingEndTime} = this.state;

    let privilegeOptions = privileges.map((privilege) => ({
      key: privilege.id,
      value: privilege.id,
      text: privilege.name
    }))

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
          <Dropdown
            placeholder='Parent'
            search
            selection
            options={privilegeOptions}
            onChange={this.handleParentPrivilegeChange}
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
        <FormField>
          <Checkbox
            label='Recurring Booking Permission'
            checked={recurringBookingPermission}
            onChange={this.handleRecurringBookingPermission}
          />
        </FormField>
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
        <Form.Field>
          <Input
            size='small'
            icon='calendar alternate outline'
            iconPosition='left'
            type='time'
            value={bookingStartTime}
            onChange={(e) => this.handleInputChange('bookingStartTime', e)}
          />
        </Form.Field>
        <Form.Field>
          <Input
            size='small'
            icon='calendar alternate'
            iconPosition='left'
            type='time'
            value={bookingEndTime}
            onChange={(e) => this.handleInputChange('bookingEndTime', e)}
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

