import PropTypes from 'prop-types';
import React, { Component } from 'react';
import { Button, Dropdown, Icon } from 'semantic-ui-react';
import sweetAlert from 'sweetalert2';
import api from '../../utils/api';
import './BookingInfoModal.scss';


class EditBookingForm extends Component {
  static generateMinuteOptions(minuteInterval) {
    const result = [];
    for (let i = 0; i < 60; i += minuteInterval) {
      result.push({
        text: `${i < 10 ? `0${i}` : i}`,
        value: `${i < 10 ? `0${i}` : i}`,
      });
    }
    return result;
  }

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
  }

  componentDidMount() {
    const { minuteInterval, reservationProfiles, booking } = this.props;
    const startTime = booking.start_time;
    const endTime = booking.end_time;
    this.setState({
      startHour: startTime.substring(0, 2),
      startMinute: startTime.substring(3, 5),
      endHour: endTime.substring(0, 2),
      endMinute: endTime.substring(3, 5),
      hourOptions: this.generateHourOptions(),
      minuteOptions: EditBookingForm.generateMinuteOptions(minuteInterval),
      reservedOptions: EditBookingForm.generateReservationProfilesOptions(reservationProfiles),
    });
  }

  sendPatchBooking = () => {
    const { booking } = this.props;
    const {
      startHour,
      startMinute,
      endHour,
      endMinute,
    } = this.state;

    const data = {
      start_time: `${startHour}:${startMinute}`,
      end_time: `${endHour}:${endMinute}`,
    };
    api.updateBooking(booking.id, data)
      .then(() => {
        sweetAlert('Completed',
          'Booking was sucessfully updated.',
          'success')
          .then((result) => {
            if (result.value) {
              this.closeModalWithEditBooking();
            }
          });
      })
      .catch((error) => {
        sweetAlert(
          'Reservation failed',
          error.response.data,
          'error',
        );
      });
  }

  handleSubmit = () => {
    // Verify requirements before sending the POST request
    try {
      this.verifyReservationTimes();
    } catch (err) {
      sweetAlert('Edit blocked', err.message, 'warning');
      return;
    }

    this.sendPatchBooking();
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

  generateHourOptions() {
    const result = [];
    const { minHour, maxHour } = this.props;
    for (let i = minHour; i < maxHour; i += 1) {
      result.push({
        text: `${i < 10 ? `0${i}` : i}`,
        value: `${i < 10 ? `0${i}` : i}`,
      });
    }
    return result;
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
    } = this.state;
    return (
      <div>
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
        <Button content="Edit Booking" primary onClick={this.handleSubmit} />
        <div className="ui divider" />
      </div>
    );
  }

  render() {
    return (
      <div id="reservation-details-modal">
        {this.renderEditBookingForm()}
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
