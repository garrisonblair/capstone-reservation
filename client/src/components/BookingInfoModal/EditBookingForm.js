import PropTypes from 'prop-types';
import React, { Component } from 'react';
import { Button, Dropdown, Icon } from 'semantic-ui-react';
import sweetAlert from 'sweetalert2';
import api from '../../utils/api';
import './BookingInfoModal.scss';


class EditBookingForm extends Component {
  state = {
    startHour: "00",
    startMinute: "00",
    endHour: "00",
    endMinute: "00",
    hourOptions: [],
    minuteOptions: [],
    reservedOptions: [{ text: 'me', value: 'me' }]
  }

  generateHourOptions() {
    let result = []
    let { minHour, maxHour } = this.props
    for (let i = minHour; i < maxHour; i++) {
      result.push({
        text: `${i < 10 ? `0${i}` : i}`,
        value: `${i < 10 ? `0${i}` : i}`
      });
    }
    return result;
  }

  generateMinuteOptions(minuteInterval) {
    let result = [];
    for (let i = 0; i < 60; i += minuteInterval) {
      result.push({
        text: `${i < 10 ? `0${i}` : i}`,
        value: `${i < 10 ? `0${i}` : i}`
      })
    }
    return result;
  }

  generateReservationProfilesOptions(reservationProfiles) {
    let result = reservationProfiles.map((profile) => ({ text: profile, value: profile }))
    return result;
  }

  closeModalWithEditBooking = () => {
    this.props.onCloseWithEditBooking();
  }

  handleStartHourChange = (e, { value }) => {
    this.setState({
      startHour: value
    });
  }

  handleStartMinuteChange = (e, { value }) => {
    this.setState({
      startMinute: value
    });
  }

  handleEndHourChange = (e, { value }) => {
    this.setState({
      endHour: value
    });
  }

  handleEndMinuteChange = (e, { value }) => {
    this.setState({
      endMinute: value
    });
  }

  verifyReservationTimes() {
    const { startHour, startMinute, endHour, endMinute } = this.state;
    const startTime = `${startHour}${startMinute}`;
    const endTime = `${endHour}${endMinute}`;
    if (startTime > endTime) {
      throw new Error("The end time you entered is before the current time.");
    }
  }

  /************ REQUESTS *************/

  sendPatchBooking = () => {
    const { booking } = this.props;

    const data = {
      "start_time": `${this.state.startHour}:${this.state.startMinute}`,
      "end_time": `${this.state.endHour}:${this.state.endMinute}`
    };
    api.updateBooking(booking.id, data)
      .then((response) => {
        sweetAlert('Completed',
          `Booking was sucessfully updated.`,
          'success'
        )
          .then((result) => {
            if (result.value) {
              this.closeModalWithEditBooking()
            }
          })
      })
      .catch((error) => {
        sweetAlert(
          'Reservation failed',
          error.response.data,
          'error'
        )
      })
  }

  handleSubmit = () => {
    // Verify requirements before sending the POST request
    try {
      this.verifyReservationTimes();
    }
    catch (err) {
      sweetAlert('Edit blocked', err.message, 'warning');
      return;
    }

    this.sendPatchBooking();
  }

  /************* COMPONENT LIFE CYCLE *************/
  componentDidMount() {
    const { minuteInterval, reservationProfiles, booking } = this.props;
    let startTime = booking.start_time
    let endTime = booking.end_time
    this.setState({
      startHour: startTime.substring(0, 2),
      startMinute: startTime.substring(3, 5),
      endHour: endTime.substring(0, 2),
      endMinute: endTime.substring(3, 5),
      hourOptions: this.generateHourOptions(),
      minuteOptions: this.generateMinuteOptions(minuteInterval),
      reservedOptions: this.generateReservationProfilesOptions(reservationProfiles)
    });
  }

  /************* COMPONENT RENDERING *************/

  renderEditBookingForm() {
    const { hourOptions, minuteOptions, reservedOptions, startHour, startMinute, endHour, endMinute } = this.state;
    console.log(startHour)
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
            placeholder='hh'
            options={hourOptions}
            onChange={this.handleStartHourChange}
            value={startHour}
          />
          <Dropdown
            selection
            compact
            className="dropdown--fixed-width"
            placeholder='mm'
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
            placeholder='hh'
            options={hourOptions}
            onChange={this.handleEndHourChange}
            value={endHour}
          />
          <Dropdown
            selection
            compact
            className="dropdown--fixed-width"
            placeholder='mm'
            options={minuteOptions}
            onChange={this.handleEndMinuteChange}
            value={endMinute}
          />
        </div>
        <div className="modal-description">
          <h3 className="header--inline">
            <Icon name="user" /> {" "}
            {`by `}
          </h3>
          <Dropdown
            selection
            compact
            className="dropdown--fixed-width"
            placeholder='hh'
            options={reservedOptions}
            defaultValue={this.state.reservedOptions[0].value}
          />
        </div>
        <Button content='Edit Booking' primary onClick={this.handleSubmit} />
        <div className="ui divider" />
      </div>

    )
  }

  render() {
    return (
      <div id="reservation-details-modal">
        {this.renderEditBookingForm()}
      </div>
    )
  }
}

EditBookingForm.propTypes = {
  booking: PropTypes.object.isRequired,
  selectedRoomName: PropTypes.string.isRequired,
  onCloseWithEditBooking: PropTypes.func,
}

EditBookingForm.defaultProps = {
  minHour: 8,
  maxHour: 24,
  minuteInterval: 10,
  reservationProfiles: ['me']
}

export default EditBookingForm;
