import PropTypes from 'prop-types';
import React, { Component } from 'react';
import { Button, Dropdown, Icon } from 'semantic-ui-react';
import sweetAlert from 'sweetalert2';
import Login from '../Login';
import api from '../../utils/api';
import storage from '../../utils/local-storage';
import timeUtil from '../../utils/time';
import './BookingInfoModal.scss';


class CampOnForm extends Component {
  static generateReservationProfilesOptions(reservationProfiles) {
    const result = reservationProfiles.map(profile => ({ text: profile, value: profile }));
    return result;
  }

  state = {
    endHour: '12',
    endMinute: '00',
    hourOptions: [],
    minuteOptions: [],
    reservedOptions: [{ text: 'me', value: 'me' }],
    showLogin: false,
  }

  /*
   * COMPONENT LIFE CYCLE
   */
  componentDidMount() {
    const { maxHour, minuteInterval, reservationProfiles } = this.props;
    this.setState({
      hourOptions: this.generateHourOptions(maxHour),
      minuteOptions: timeUtil.generateMinuteOptions(minuteInterval),
      reservedOptions: CampOnForm.generateReservationProfilesOptions(reservationProfiles),
    });
  }

  closeModalWithCampOn = () => {
    const { onCloseWithCampOn } = this.props;
    onCloseWithCampOn();
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

  handleSubmit = () => {
    // Verify requirements before sending the POST request
    try {
      this.verifyReservationTimes();
    } catch (err) {
      sweetAlert.fire({
        position: 'top',
        type: 'warning',
        title: 'Campon blocked',
        text: err.message,
      });
      return;
    }
    if (storage.getUser() == null) {
      this.setState({ showLogin: true });
    } else {
      this.sendPostRequestCampOn();
    }
  }

  closeLogin = () => {
    this.setState({ showLogin: false });
    if (storage.getUser() == null) {
      sweetAlert.fire({
        position: 'top',
        type: 'error',
        title: 'Campon failed',
        text: 'Please login to camp on the reservation.',
      });
    } else {
      this.sendPostRequestCampOn();
    }
  }

  sendPostRequestCampOn = () => {
    const { booking } = this.props;
    const { endHour, endMinute } = this.state;

    const data = {
      camped_on_booking: booking.isCampOn ? booking.camped_on_booking : booking.id,
      end_time: `${endHour}:${endMinute}`,
    };
    api.createCampOn(data)
      .then(() => {
        this.closeModalWithCampOn();
        sweetAlert.fire({
          position: 'top',
          type: 'success',
          title: 'Your campon was successful',
          toast: true,
          showConfirmButton: false,
          timer: 2000,
        });
      })
      .catch((error) => {
        sweetAlert.fire({
          position: 'top',
          type: 'error',
          title: 'Reservation failed',
          text: error.response.data,
        });
      });
  }

  generateHourOptions(maxHour) {
    const result = [];
    const minHour = new Date().getHours();
    this.setState({ endHour: `${minHour < 10 ? `0${minHour}` : minHour}` });
    for (let i = minHour; i < maxHour; i += 1) {
      result.push({
        text: `${i < 10 ? `0${i}` : i}`,
        value: `${i < 10 ? `0${i}` : i}`,
      });
    }
    return result;
  }

  verifyReservationTimes() {
    const { endHour, endMinute } = this.state;
    const currentTime = new Date();
    const startTime = `${currentTime.getHours()}${currentTime.getMinutes() < 10 ? `0${currentTime.getMinutes()}` : `${currentTime.getMinutes()}`}`;
    const endTime = `${endHour}${endMinute}`;
    if (startTime > endTime) {
      throw new Error('The end time you entered is before the current time.');
    }
  }

  renderCampOnForm() {
    const {
      hourOptions,
      minuteOptions,
      reservedOptions,
      endHour,
      endMinute,
      showLogin,
    } = this.state;
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
        <Button content="Camp on" primary onClick={this.handleSubmit} />
        <div className="ui divider" />
        <Login show={showLogin} onClose={this.closeLogin} />
      </div>
    );
  }

  render() {
    return (
      <div id="reservation-details-modal">
        {this.renderCampOnForm()}
      </div>
    );
  }
}

CampOnForm.propTypes = {
  booking: PropTypes.instanceOf(Object).isRequired,
  onCloseWithCampOn: PropTypes.func,
  maxHour: PropTypes.number,
  minuteInterval: PropTypes.number,
  reservationProfiles: PropTypes.instanceOf(Array),
};

CampOnForm.defaultProps = {
  maxHour: 24,
  minuteInterval: 10,
  reservationProfiles: ['me'],
  onCloseWithCampOn: () => {},
};

export default CampOnForm;
