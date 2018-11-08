import React, {Component} from 'react';
import ReactDOMServer from "react-dom/server";
import {Button, Checkbox, Dropdown, Form, Header, Icon, Input, Modal, FormField} from 'semantic-ui-react';
import sweetAlert from 'sweetalert2';
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
    bookingStartTime: '08:00:00',
    bookingEndTime: '23:00:00'
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
      max_days_until_booking: maxDaysUntilBooking,
      max_bookings: maxBookings,
      max_recurring_bookings: maxRecurringBookings,
      can_make_recurring_booking: recurringBookingPermission,
      booking_start_time: bookingStartTime,
      booking_end_time: bookingEndTime
    }

    console.log(data);

    api.createPrivilege(data)
    .then((response) => {
      sweetAlert(
        'Completed',
        'New privilege successfully added.',
        'success'
      )

      // Reset states
      this.setState({
        name: '',
        parent: '',
        maxDaysUntilBooking: 0,
        maxBookings: 0,
        maxRecurringBookings: 0,
        recurringBookingPermission: false,
        bookingStartTime: '08:00:00',
        bookingEndTime: '23:00:00'
      })
    })
    .catch((error) => {
      let {status, data} = error.response;

      if (status === 500) {
        sweetAlert({
          title: 'Error',
          text: 'Internal Server Error',
          type: 'error'
        })
        return;
      }

      // console.log(data);
      let errors = Object.keys(data).map((field, index) => {
        return (
          <div key={index} className="error-message">
            <p className='field'> {field} </p>
            <ul>
              <li>{data[field][0]}</li>
            </ul>
          </div>
        )
      })
      sweetAlert({
        title: 'Error',
        html: ReactDOMServer.renderToString(errors),
        type: 'error'
      })
    })
    this.props.onClose();
  }

  renderForm() {
    const {privileges} = this.props;
    const {recurringBookingPermission, bookingStartTime, bookingEndTime} = this.state;

    let privilegeOptions = privileges.map((privilege) => ({
      key: privilege.id,
      value: privilege.id,
      text: privilege.name
    }))

    privilegeOptions.unshift({
      key: '',
      value: '',
      text: 'No parent'
    })

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

