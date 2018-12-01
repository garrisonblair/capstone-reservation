import PropTypes from 'prop-types';
import React, { Component } from 'react';
import ReactDOMServer from 'react-dom/server';
import {
  Button, Checkbox, Dropdown, Form, Header, Icon, Input, Modal, FormField,
} from 'semantic-ui-react';
import sweetAlert from 'sweetalert2';
import api from '../../../utils/api';
import './AddPrivilegeModal.scss';


class AddPrivilegeModal extends Component {
  state = {
    name: '',
    // parent: '',
    // maxDaysUntilBooking: 0,
    // maxBookings: 0,
    // maxRecurringBookings: 0,
    // recurringBookingPermission: false,
    // isDefault: false,
    // bookingStartTime: '08:00:00',
    // bookingEndTime: '23:00:00'
  }

  handleInputChange = (state, e) => {
    this.setState({
      [`${state}`]: e.target.value,
    });
  }

  handleCheckbox = (state, e, data) => {
    const { checked } = data;
    this.setState({
      [`${state}`]: checked,
    });
  }

  handleParentPrivilegeChange = (e, data) => {
    this.setState({
      parent: data.value,
    });
  }

  handleSubmit = () => {
    const {
      name, parent, maxDaysUntilBooking,
      maxBookings, maxRecurringBookings, recurringBookingPermission,
      isDefault, bookingStartTime, bookingEndTime,
    } = this.state;
    const { onClose } = this.props;
    const data = {
      name,
    };

    if (parent) {
      data.parent_category = parent;
    }

    if (maxDaysUntilBooking) {
      data.max_days_until_booking = maxDaysUntilBooking;
    }

    if (maxBookings) {
      data.max_bookings = maxBookings;
    }

    if (maxRecurringBookings) {
      data.max_recurring_bookings = maxRecurringBookings;
    }

    if (recurringBookingPermission) {
      data.can_make_recurring_booking = recurringBookingPermission;
    }

    if (isDefault) {
      data.is_default = isDefault;
    }

    if (bookingStartTime) {
      data.booking_start_time = bookingStartTime;
    }

    if (bookingEndTime) {
      data.booking_end_time = bookingEndTime;
    }

    api.createPrivilege(data)
      .then(() => {
        sweetAlert(
          'Completed',
          'New privilege successfully added.',
          'success',
        )
          .then(() => {
            onClose();

            // Reset states
            this.setState({
              name: '',
              parent: '',
              maxDaysUntilBooking: 0,
              maxBookings: 0,
              maxRecurringBookings: 0,
              recurringBookingPermission: false,
              isDefault: false,
              bookingStartTime: '08:00:00',
              bookingEndTime: '23:00:00',
            });
          });
      })
      .catch((error) => {
        const { status, data: dataError } = error.response;

        if (status === 500) {
          sweetAlert({
            title: 'Error',
            text: 'Internal Server Error',
            type: 'error',
          });
          return;
        }

        const errors = Object.keys(dataError).map((field, index) => (
          <div key={index[0]} className="error-message">
            <p className="field">
              {field}
            </p>
            <ul>
              <li>{dataError[field][0]}</li>
            </ul>
          </div>
        ));
        sweetAlert({
          title: 'Error',
          html: ReactDOMServer.renderToString(errors),
          type: 'error',
        });
      });
  }

  renderForm() {
    const { privileges } = this.props;
    const {
      recurringBookingPermission, isDefault, bookingStartTime, bookingEndTime,
    } = this.state;

    const privilegeOptions = privileges.map(privilege => ({
      key: privilege.id,
      value: privilege.id,
      text: privilege.name,
    }));

    privilegeOptions.unshift({
      key: '',
      value: '',
      text: 'No parent',
    });

    return (
      <div>
        <Form.Field>
          <Input
            fluid
            size="small"
            icon="text cursor"
            iconPosition="left"
            placeholder="Name"
            onChange={e => this.handleInputChange('name', e)}
          />
        </Form.Field>
        <FormField>
          <Checkbox
            label="Default"
            checked={isDefault}
            onChange={(e, data) => this.handleCheckbox('isDefault', e, data)}
          />
        </FormField>
        <Form.Field>
          <Dropdown
            placeholder="Parent"
            search
            selection
            options={privilegeOptions}
            onChange={this.handleParentPrivilegeChange}
          />
        </Form.Field>
        <Form.Field>
          <Input
            fluid
            size="small"
            icon="sort"
            iconPosition="left"
            placeholder="Max Days Until Booking"
            type="number"
            min="0"
            onChange={e => this.handleInputChange('maxDaysUntilBooking', e)}
          />
        </Form.Field>
        <Form.Field>
          <Input
            fluid
            size="small"
            icon="sort"
            iconPosition="left"
            placeholder="Max Bookings"
            type="number"
            min="0"
            onChange={e => this.handleInputChange('maxBookings', e)}
          />
        </Form.Field>
        <FormField>
          <Checkbox
            label="Recurring Booking Permission"
            checked={recurringBookingPermission}
            onChange={(e, data) => this.handleCheckbox('recurringBookingPermission', e, data)}
          />
        </FormField>
        <Form.Field>
          <Input
            fluid
            size="small"
            icon="sort"
            iconPosition="left"
            placeholder="Max Recurring Bookings"
            type="number"
            min="0"
            onChange={e => this.handleInputChange('maxRecurringBookings', e)}
          />
        </Form.Field>
        <Form.Field>
          <Input
            size="small"
            icon="calendar alternate outline"
            iconPosition="left"
            type="time"
            value={bookingStartTime}
            onChange={e => this.handleInputChange('bookingStartTime', e)}
          />
        </Form.Field>
        <Form.Field>
          <Input
            size="small"
            icon="calendar alternate"
            iconPosition="left"
            type="time"
            value={bookingEndTime}
            onChange={e => this.handleInputChange('bookingEndTime', e)}
          />
        </Form.Field>
      </div>
    );
  }

  render() {
    const { show, onClose } = this.props;
    return (
      <Modal className="privilege-modal" open={show} onClose={onClose}>
        <Header>
          <Icon name="plus" />
          {' '}
          Add Privilege
        </Header>
        <div className="privilege-modal__container">
          {this.renderForm()}
          <div className="ui divider" />
          <Form.Field>
            <Button fluid size="small" icon onClick={this.handleSubmit}>
              Add
            </Button>
          </Form.Field>
        </div>
      </Modal>
    );
  }
}

AddPrivilegeModal.propTypes = {
  onClose: PropTypes.func,
  privileges: PropTypes.instanceOf(Array),
  show: PropTypes.bool,
};

AddPrivilegeModal.defaultProps = {
  onClose: () => {},
  privileges: [],
  show: false,
};

export default AddPrivilegeModal;
