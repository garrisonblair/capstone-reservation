import axios from 'axios';
import PropTypes from 'prop-types';
import React, {Component} from 'react';
import {Button, Dropdown, Header, Icon, Form, Input, Modal, Checkbox, Tab} from 'semantic-ui-react';
import settings from '../../config/settings'
import {getTokenHeader} from '../../utils/requestHeaders';
import {getMeRequest} from '../../utils/requestUser';
import './BookingInfoModal.scss';
import {toDateInputValue} from '../../utils/dateFormatter';

class BookingInfoModal extends Component {
  state = {
    show: false,
    endHour: "-1",
    endMinute: "-1",
    hourOptions: [],
    reservedOptions: [],
    isRecurring: false,
    tabIndex: 0,
  }
  sweetAlert = require('sweetalert2');

  generateHourOptions(maxHour) {
    let result = [];
    let minHour = new Date().getHours();
    for (let i = minHour; i < maxHour; i++) {
      result.push({
        text: `${i}`,
        value: `${i}`
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
    let result = reservationProfiles.map((profile) => ({text: profile, value: profile}))
    return result;
  }

  closeModal = () => {
    this.props.onClose();
    this.setState({
      show: false
    });
  }

  closeModalWithCampOn = () => {
    this.props.onCloseWithCampOn();
    this.setState({
      show: false,
    });
  }

  handleOpen = () => this.setState({show: true});

  handleEndHourChange = (e, {value}) => {
    this.setState({
      endHour: value
    });
  }

  handleEndMinuteChange = (e, {value}) => {
    this.setState({
      endMinute: value
    });
  }

  verifyEndTime() {
    const {endHour, endMinute} = this.state;
    if (endHour === "-1" || endMinute === "-1") {
      throw new Error("Please provide an end time to make a reservation.");
    }
  }

  verifyReservationTimes() {
    const {endHour, endMinute} = this.state;
    let currentTime = new Date();
    const startTime = `${currentTime.getHours()}${currentTime.getMinutes() < 10 ? `0${currentTime.getMinutes()}` : `${currentTime.getMinutes()}`}`;
    const endTime = `${endHour}${endMinute}`;
    if (startTime > endTime) {
      throw new Error("The end time you entered is before the current time.");
    }
  }

  /************ REQUESTS *************/

  sendPostRequestCampOn = (headers) => {
    const {booking} = this.props;

    const data = {
      "camped_on_booking": booking.id,
      "end_time": `${this.state.endHour}:${this.state.endMinute}`
    };
    axios({
      method: 'POST',
      url: `${settings.API_ROOT}/campon`,
      headers,
      data,
      withCredentials: true,
    })
    .then((response) => {
      this.sweetAlert('Completed',
        `Room ${this.props.selectedRoomName} was successfuly booked.`,
        'success')
        .then((result) => {
          if (result.value) {
            this.closeModalWithCampOn()
          }
        })
    })
    .catch((error) => {
      this.sweetAlert(
        'Reservation failed',
        error.response.data[0],
        'error')
    })
  }

  handleSubmit = () => {
    // Verify requirements before sending the POST request
    try {
      this.verifyEndTime();
      this.verifyReservationTimes();
    }
    catch (err) {
      this.sweetAlert('Camp on blocked', err.message, 'warning');
      return;
    }

    const headers = getTokenHeader();
    this.sendPostRequestCampOn(headers);
  }

  /************* COMPONENT LIFE CYCLE *************/

  componentWillReceiveProps(nextProps) {
    if(nextProps.show) {
      this.setState({
        show: nextProps.show
      });
    }
  }

  componentWillMount() {
    const {maxHour, minuteInterval, reservationProfiles} = this.props;
    this.setState({
      hourOptions: this.generateHourOptions(maxHour),
      minuteOptions: this.generateMinuteOptions(minuteInterval),
      reservedOptions: this.generateReservationProfilesOptions(reservationProfiles)
    });
  }

  /************* COMPONENT RENDERING *************/

  renderDescription() {
    const {hourOptions, minuteOptions, reservedOptions} = this.state;
    const {booking} = this.props;
    let camponPossible = false;

    if(booking.id) {
      let currentDate = new Date();
      let currentTime = `${currentDate.getHours()}${currentDate.getMinutes() < 10 ? `0${currentDate.getMinutes()}` : `${currentDate.getMinutes()}`}`;
      let bookingEndTime = booking.end_time.replace(/:/g, '');
      bookingEndTime = bookingEndTime / 100
      if(currentTime < bookingEndTime) {
        camponPossible = true;
      }
    }

    return (
      <Modal.Content>
        <Modal.Description>
          <Header>
            {/* <Icon name="calendar" /> */}
            {booking.date}
          </Header>
          <div className="modal-description">
            <h3 className="header--inline">
              {/* <Icon className="hourglass start" /> */}
              {`from ${booking.start_time ? booking.start_time.slice(0,-3) : ''}`}
            </h3>
          </div>
          <div className="modal-description">
            <h3 className="header--inline">
              {/* <Icon className="hourglass end" /> */}
              {`to ${booking.end_time? booking.end_time.slice(0,-3) : ''}`}
            </h3>
          </div>
          <div className="modal-description">
            <h3 className="header--inline">
              <Icon name="user" /> {" "}
              {`by ${booking.student}`}
            </h3>
          </div>
          <div className="ui divider" />
          {camponPossible ? this.renderCampOnForm() : null}
          <div>
            <Button content='Close' secondary onClick={this.closeModal} />
          </div>
        </Modal.Description>
      </Modal.Content>
    )
  }

  renderCampOnForm() {
    const {hourOptions, minuteOptions, reservedOptions} = this.state;
    return(
      <div>
        <div className="modal-description">
          <h3 className="header--inline">
            <span>Camp on until  </span>
          </h3>
          <Dropdown
            selection
            compact
            className="dropdown--fixed-width"
            placeholder='hh'
            options={hourOptions}
            onChange={this.handleEndHourChange}
          />
          <Dropdown
            selection
            compact
            className="dropdown--fixed-width"
            placeholder='mm'
            options={minuteOptions}
            onChange={this.handleEndMinuteChange}
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
          <Button content='Camp on' primary onClick={this.handleSubmit} />
          <div className="ui divider" />
      </div>

    )
  }

  render() {
    const {show} = this.state;
    const {selectedRoomName} = this.props;
    return (
      <div id="reservation-details-modal">
        <Modal centered={false} size={"tiny"} open={show}>
          <Modal.Header>
            <Icon name="map marker alternate" />
            Room {selectedRoomName}
          </Modal.Header>
          {this.renderDescription()}
        </Modal>
      </div>
    )
  }
}

BookingInfoModal.propTypes = {
  show: PropTypes.bool.isRequired,
  booking: PropTypes.object.isRequired,
  maxHour: PropTypes.number,
  minuteInterval: PropTypes.number,
  selectedRoomName: PropTypes.string.isRequired,
  onClose: PropTypes.func,
  onCloseWithCampOn: PropTypes.func,
}

BookingInfoModal.defaultProps = {
  maxHour: 24,
  minuteInterval: 10,
  reservationProfiles: ['me']
}

export default BookingInfoModal;
