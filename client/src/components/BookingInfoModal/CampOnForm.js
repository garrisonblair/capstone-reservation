import PropTypes from 'prop-types';
import React, { Component } from 'react';
import { Button, Dropdown, Icon } from 'semantic-ui-react';
import sweetAlert from 'sweetalert2';
import api from '../../utils/api';
import './BookingInfoModal.scss';


class CampOnForm extends Component {
  state = {
    endHour: "12",
    endMinute: "00",
    hourOptions: [],
    minuteOptions: [],
    reservedOptions: [{ text: 'me', value: 'me' }]
  }

  generateHourOptions(maxHour) {
    let result = [];
    let minHour = new Date().getHours();
    this.setState({ endHour: `${minHour < 10 ? `0${minHour}` : minHour}` })
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

  closeModalWithCampOn = () => {
    this.props.onCloseWithCampOn();
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
    const { endHour, endMinute } = this.state;
    let currentTime = new Date();
    const startTime = `${currentTime.getHours()}${currentTime.getMinutes() < 10 ? `0${currentTime.getMinutes()}` : `${currentTime.getMinutes()}`}`;
    const endTime = `${endHour}${endMinute}`;
    if (startTime > endTime) {
      throw new Error("The end time you entered is before the current time.");
    }
  }

  /************ REQUESTS *************/

  sendPostRequestCampOn = () => {
    const { booking } = this.props;

    const data = {
      "camped_on_booking": booking.id,
      "end_time": `${this.state.endHour}:${this.state.endMinute}`
    };
    api.createCampOn(data)
      .then((response) => {
        sweetAlert('Completed',
          `Your camp-on was successful.`,
          'success'
        )
          .then((result) => {
            if (result.value) {
              this.closeModalWithCampOn()
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
      sweetAlert('Camp on blocked', err.message, 'warning');
      return;
    }

    this.sendPostRequestCampOn();
  }

  /************* COMPONENT LIFE CYCLE *************/
  componentDidMount() {
    const { maxHour, minuteInterval, reservationProfiles } = this.props;
    this.setState({
      hourOptions: this.generateHourOptions(maxHour),
      minuteOptions: this.generateMinuteOptions(minuteInterval),
      reservedOptions: this.generateReservationProfilesOptions(reservationProfiles)
    });
  }

  /************* COMPONENT RENDERING *************/

  renderCampOnForm() {
    const { hourOptions, minuteOptions, reservedOptions, endHour, endMinute } = this.state;
    return (
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
            defaultValue={reservedOptions[0].value}
          />
        </div>
        <Button content='Camp on' primary onClick={this.handleSubmit} />
        <div className="ui divider" />
      </div>

    )
  }

  render() {
    return (
      <div id="reservation-details-modal">
        {this.renderCampOnForm()}
      </div>
    )
  }
}

CampOnForm.propTypes = {
  booking: PropTypes.object.isRequired,
  selectedRoomName: PropTypes.string.isRequired,
  onCloseWithCampOn: PropTypes.func,
}

CampOnForm.defaultProps = {
  maxHour: 24,
  minuteInterval: 10,
  reservationProfiles: ['me']
}

export default CampOnForm;
