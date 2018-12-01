import PropTypes from 'prop-types';
import React, { Component } from 'react';
import { Button, Dropdown, Icon } from 'semantic-ui-react';
import sweetAlert from 'sweetalert2';
import api from '../../utils/api';
import './BookingInfoModal.scss';


class CampOnForm extends Component {
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
    endHour: '12',
    endMinute: '00',
    hourOptions: [],
    minuteOptions: [],
    reservedOptions: [{ text: 'me', value: 'me' }],
  }

  /*
   * COMPONENT LIFE CYCLE
   */
  componentDidMount() {
    const { maxHour, minuteInterval, reservationProfiles } = this.props;
    this.setState({
      hourOptions: this.generateHourOptions(maxHour),
      minuteOptions: CampOnForm.generateMinuteOptions(minuteInterval),
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
      sweetAlert('Camp on blocked', err.message, 'warning');
      return;
    }
    this.sendPostRequestCampOn();
  }

  sendPostRequestCampOn = () => {
    const { booking } = this.props;
    const { endHour, endMinute } = this.state;

    const data = {
      camped_on_booking: booking.id,
      end_time: `${endHour}:${endMinute}`,
    };
    api.createCampOn(data)
      .then(() => {
        sweetAlert('Completed',
          'Your camp-on was successful.',
          'success')
          .then((result) => {
            if (result.value) {
              this.closeModalWithCampOn();
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

  /*
   * COMPONENT RENDERING
   */

  renderCampOnForm() {
    const {
      hourOptions,
      minuteOptions,
      reservedOptions,
      endHour,
      endMinute,
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
