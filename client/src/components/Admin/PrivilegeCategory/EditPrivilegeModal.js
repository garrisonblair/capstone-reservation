/* eslint-disable react/prop-types */
/* eslint-disable no-console */
import React, { Component } from 'react';
import PropTypes from 'prop-types';
import ReactDOMServer from 'react-dom/server';
import {
  Button, Checkbox, Dropdown, Form, Header, Icon, Input, Modal, FormField,
} from 'semantic-ui-react';
import sweetAlert from 'sweetalert2';
import api from '../../../utils/api';
import './AddPrivilegeModal.scss';


class EditPrivilegeModal extends Component {
  constructor(props) {
    super(props);
    this.state = {
      privilegeID: props.privilege.id,
      name: props.privilege.name,
      parent: props.privilege.parent_category,
      course: props.privilege.related_course,
      maxDaysUntilBooking: props.privilege.max_days_until_booking,
      maxBookingsPerDay: props.privilege.max_num_bookings_for_date,
      maxDaysWithBookings: props.privilege.max_num_days_with_bookings,
      maxRecurringBookings: props.privilege.max_recurring_bookings,
      recurringBookingPermission: props.privilege.can_make_recurring_booking,
      isDefault: props.privilege.is_default,
      bookingStartTime: props.privilege.booking_start_time,
      bookingEndTime: props.privilege.booking_end_time,
    };
  }

  static getDerivedStateFromProps(props, state) {
    return {
      privilegeID: state.privilegeID || props.privilege.id,
      name: state.name || props.privilege.name,
      parent: state.parent || props.privilege.parent_category,
      course: state.course || props.privilege.related_course,
      maxDaysUntilBooking: state.maxDaysUntilBooking || props.privilege.max_days_until_booking,
      maxBookingsPerDay: state.maxBookingsPerDay || props.privilege.max_num_bookings_for_date,
      maxDaysWithBookings: state.maxDaysWithBookings || props.privilege.max_num_days_with_bookings,
      maxRecurringBookings: state.maxRecurringBookings || props.privilege.max_recurring_bookings,
      recurringBookingPermission: state.recurringBookingPermission || props.privilege.can_make_recurring_booking,
      isDefault: state.isDefault || props.privilege.is_default,
      bookingStartTime: state.bookingStartTime || props.privilege.booking_start_time,
      bookingEndTime: state.bookingEndTime || props.privilege.booking_end_time,
    };
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
      name, privilegeID, parent, course, maxDaysUntilBooking,
      maxBookingsPerDay, maxDaysWithBookings, maxRecurringBookings, recurringBookingPermission,
      isDefault, bookingStartTime, bookingEndTime,
    } = this.state;
    const { onClose } = this.props;
    const data = {
      name,
    };

    if (parent) {
      data.parent_category = parent;
    }

    if (course) {
      data.related_course = course;
    }

    if (maxDaysUntilBooking) {
      data.max_days_until_booking = maxDaysUntilBooking;
    }

    if (maxBookingsPerDay) {
      data.max_num_bookings_for_date = maxBookingsPerDay;
    }

    if (maxDaysWithBookings) {
      data.max_num_days_with_bookings = maxDaysWithBookings;
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

    console.log(data);

    api.updatePrivilege(privilegeID, data)
      .then(() => {
        sweetAlert(
          'Completed',
          'New privilege successfully added.',
          'success',
        )
          .then(() => {
            onClose();
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
      name, parent, course, maxDaysUntilBooking,
      maxBookingsPerDay, maxDaysWithBookings, maxRecurringBookings, recurringBookingPermission,
      isDefault, bookingStartTime, bookingEndTime,
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
            value={name}
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
            icon="text cursor"
            iconPosition="left"
            placeholder="Related Course"
            value={course}
            onChange={e => this.handleInputChange('course', e)}
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
            value={maxDaysUntilBooking}
            onChange={e => this.handleInputChange('maxDaysUntilBooking', e)}
          />
        </Form.Field>
        <Form.Field>
          <Input
            fluid
            size="small"
            icon="sort"
            iconPosition="left"
            placeholder="Max Bookings per day"
            type="number"
            min="0"
            value={maxBookingsPerDay}
            onChange={e => this.handleInputChange('maxBookingsPerDay', e)}
          />
        </Form.Field>
        <Form.Field>
          <Input
            fluid
            size="small"
            icon="sort"
            iconPosition="left"
            placeholder="Max days with bookings"
            type="number"
            min="0"
            value={maxDaysWithBookings}
            onChange={e => this.handleInputChange('maxDaysWithBookings', e)}
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
            value={maxRecurringBookings}
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
          Edit Privilege
        </Header>
        <div className="privilege-modal__container">
          {this.renderForm()}
          <div className="ui divider" />
          <Form.Field>
            <Button fluid size="small" icon onClick={this.handleSubmit}>
              Update
            </Button>
          </Form.Field>
        </div>
      </Modal>
    );
  }
}

EditPrivilegeModal.propTypes = {
  onClose: PropTypes.func,
  privileges: PropTypes.instanceOf(Array),
  show: PropTypes.bool,
};

EditPrivilegeModal.defaultProps = {
  onClose: () => {},
  privileges: [],
  show: false,
};

export default EditPrivilegeModal;
