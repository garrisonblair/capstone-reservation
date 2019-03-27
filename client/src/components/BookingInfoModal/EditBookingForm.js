import PropTypes from 'prop-types';
import React, { Component } from 'react';
import {
  Button,
  Dropdown,
  Icon,
  Checkbox,
  Divider,
} from 'semantic-ui-react';
import sweetAlert from 'sweetalert2';
import api from '../../utils/api';
import storage from '../../utils/local-storage';
import timeUtil from '../../utils/time';
import './BookingInfoModal.scss';


class EditBookingForm extends Component {
  static generateReservationProfilesOptions(reservationProfiles) {
    const result = reservationProfiles.map(profile => ({ text: profile, value: profile }));
    return result;
  }

  state = {
    startHour: '00',
    startMinute: '00',
    endHour: '00',
    endMinute: '00',
    hourOptions: [],
    minuteOptions: [],
    reservedOptions: [{ text: 'me', value: 'me' }],
    isLoading: false,
    bypassPrivileges: false,
    bypassValidation: false,
  }

  componentDidMount() {
    const {
      minuteInterval, reservationProfiles, booking, minHour, maxHour,
    } = this.props;
    const startTime = booking.start_time;
    const endTime = booking.end_time;
    this.setState({
      startHour: startTime.substring(0, 2),
      startMinute: startTime.substring(3, 5),
      endHour: endTime.substring(0, 2),
      endMinute: endTime.substring(3, 5),
      hourOptions: timeUtil.generateHourOptions(minHour, maxHour),
      minuteOptions: timeUtil.generateMinuteOptions(minuteInterval),
      reservedOptions: EditBookingForm.generateReservationProfilesOptions(reservationProfiles),
    });
  }

  sendPatchBooking = () => {
    this.setState({ isLoading: true });

    const { booking } = this.props;
    const {
      startHour,
      startMinute,
      endHour,
      endMinute,
      bypassPrivileges,
      bypassValidation,
    } = this.state;

    const data = {
      start_time: `${startHour}:${startMinute}`,
      end_time: `${endHour}:${endMinute}`,
    };
    if (bypassPrivileges) {
      data.bypass_privileges = true;
    }

    if (bypassValidation) {
      data.bypass_validation = true;
    }

    api.updateBooking(booking.id, data)
      .then(() => {
        this.setState({ isLoading: false });
        this.closeModalWithEditBooking();
        sweetAlert.fire({
          position: 'top',
          type: 'success',
          title: 'Booking was successfully updated.',
          toast: true,
          showConfirmButton: false,
          timer: 2000,
        });
      })
      .catch((error) => {
        this.setState({ isLoading: false });

        sweetAlert.fire({
          position: 'top',
          type: 'error',
          title: 'Reservation failed',
          text: error.response.data,
        });
      });
  }

  sendPatchCampOn = () => {
    this.setState({ isLoading: true });
    const { booking } = this.props;
    const {
      endHour,
      endMinute,
    } = this.state;

    const data = {
      end_time: `${endHour}:${endMinute}`,
    };

    api.updateCampOn(booking.camp_on_id, data)
      .then(() => {
        this.setState({ isLoading: false });
        this.closeModalWithEditBooking();
        sweetAlert.fire({
          position: 'top',
          type: 'success',
          title: 'Camp On was successfully updated.',
          toast: true,
          showConfirmButton: false,
          timer: 2000,
        });
      })
      .catch((error) => {
        this.setState({ isLoading: false });
        sweetAlert.fire({
          position: 'top',
          type: 'error',
          title: 'Reservation failed',
          text: error.response.data,
        });
      });
  }

  handleSubmit = () => {
    const { booking } = this.props;
    // Verify requirements before sending the POST request
    try {
      this.verifyReservationTimes();
    } catch (err) {
      sweetAlert.fire({
        position: 'top',
        type: 'warning',
        title: 'Edit blocked',
        text: err.message,
      });
      return;
    }
    if (booking.isCampOn) {
      this.sendPatchCampOn();
    } else {
      this.sendPatchBooking();
    }
  }

  closeModalWithEditBooking = () => {
    const { onCloseWithEditBooking } = this.props;
    onCloseWithEditBooking();
  }

  handleStartHourChange = (e, { value }) => {
    this.setState({
      startHour: value,
    });
  }

  handleStartMinuteChange = (e, { value }) => {
    this.setState({
      startMinute: value,
    });
  }

  handleEndHourChange = (e, { value }) => {
    this.setState({
      endHour: value,
    });
  }

  handleEndMinuteChange = (e, { value }) => {
    this.setState({
      endMinute: value,
    });
  }

  handleBypassPrivilegesChange = (event, data) => {
    this.setState({ bypassPrivileges: data.checked });
  }

  handleBypassValidationChange = (event, data) => {
    this.setState({ bypassValidation: data.checked });
  }

  verifyReservationTimes() {
    const {
      startHour,
      startMinute,
      endHour,
      endMinute,
    } = this.state;
    const startTime = `${startHour}${startMinute}`;
    const endTime = `${endHour}${endMinute}`;
    if (startTime > endTime) {
      throw new Error('The end time you entered is before the current time.');
    }
  }

  renderEditBookingForm() {
    const {
      hourOptions,
      minuteOptions,
      reservedOptions,
      startHour,
      startMinute,
      endHour,
      endMinute,
      isLoading,
    } = this.state;
    const { booking } = this.props;
    const fromComponent = (
      <div className="modal-description">
        <h3 className="header--inline">
          <span>From  </span>
        </h3>
        <Dropdown
          selection
          compact
          className="dropdown--fixed-width"
          placeholder="hh"
          options={hourOptions}
          onChange={this.handleStartHourChange}
          value={startHour}
        />
        <Dropdown
          selection
          compact
          className="dropdown--fixed-width"
          placeholder="mm"
          options={minuteOptions}
          onChange={this.handleStartMinuteChange}
          value={startMinute}
        />
      </div>
    );

    const toComponent = (
      <div className="modal-description">
        <h3 className="header--inline">
          <span>To </span>
        </h3>
        <Dropdown
          selection
          compact
          className="dropdown--fixed-width"
          placeholder="hh"
          options={hourOptions}
          onChange={this.handleEndHourChange}
          value={endHour}
        />
        <Dropdown
          selection
          compact
          className="dropdown--fixed-width"
          placeholder="mm"
          options={minuteOptions}
          onChange={this.handleEndMinuteChange}
          value={endMinute}
        />
      </div>
    );

    const byComponent = (
      <div className="modal-description">
        <h3 className="header--inline">
          <Icon name="user" />
          {' '}
          {'by '}
        </h3>
        <Dropdown
          selection
          compact
          className="dropdown--fixed-width"
          placeholder="hh"
          options={reservedOptions}
          defaultValue={reservedOptions[0].value}
        />
      </div>
    );
    return (
      <div>
        {!booking.isCampOn && fromComponent}
        {toComponent}
        {!booking.isCampOn && byComponent}
        <Button content={`Edit ${booking.isCampOn ? 'Camp On' : 'Booking'}`} loading={isLoading} primary onClick={this.handleSubmit} />
        <div className="ui divider" />
      </div>
    );
  }

  renderAdminBookingForm() {
    return (
      <div className="modal-description">
        <div className="modal-description">
          <Checkbox label="Bypass Privileges" onChange={this.handleBypassPrivilegesChange} />
        </div>
        <div className="modal-description">
          <Checkbox label="Bypass Validation" onChange={this.handleBypassValidationChange} />
        </div>
        <Divider />
      </div>
    );
  }

  render() {
    const user = storage.getUser();
    return (
      <div id="reservation-details-modal">
        {this.renderEditBookingForm()}
        {user && user.is_superuser ? this.renderAdminBookingForm() : null}
      </div>
    );
  }
}

EditBookingForm.propTypes = {
  booking: PropTypes.instanceOf(Object).isRequired,
  onCloseWithEditBooking: PropTypes.func,
  minHour: PropTypes.number,
  maxHour: PropTypes.number,
  minuteInterval: PropTypes.number,
  reservationProfiles: PropTypes.instanceOf(Array),
};

EditBookingForm.defaultProps = {
  minHour: 8,
  maxHour: 24,
  minuteInterval: 10,
  reservationProfiles: ['me'],
  onCloseWithEditBooking: () => {},
};

export default EditBookingForm;
