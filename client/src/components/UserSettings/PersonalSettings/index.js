import React, { Component } from 'react';
import {
  Button, Checkbox,
} from 'semantic-ui-react';
import sweetAlert from 'sweetalert2';
import api from '../../../utils/api';
import storage from '../../utils/local-storage';
import './PersonalSettings.scss';


class PersonalSettings extends Component {
  state = {
    scheduleVertical: true,
    bookingColor: '#1F5465',
    passedBookingColor: '#7F7F7F',
    camponColor: '#82220E',
    disableButton: true,
  }

  componentDidMount() {
    const { booker } = storage.getUser();
    this.syncSettings(booker);
  }

  syncSettings = (booker) => {
    api.getPersonalSettings(booker.id)
      .then((r) => {
        if (r.status === 200) {
          this.setState({
            scheduleVertical: r.data.schedule_vertical,
            bookingColor: r.data.booking_color,
            passedBookingColor: r.data.passed_booking_color,
            camponColor: r.data.campon_color,
          });
        } else if (r.status === 404) {
          api.createPersonalSettings()
            .then((c) => {
              if (c.status === 204) {
                this.setState({
                  scheduleVertical: c.data.schedule_vertical,
                  bookingColor: c.data.booking_color,
                  passedBookingColor: c.data.passed_booking_color,
                  camponColor: c.data.campon_color,
                });
              }
            })
            .catch((e) => {
              const { data } = e.response;
              sweetAlert('Blocked', data.detail, 'error');
            });
        }
      })
      .catch((e) => {
        const { data } = e.response;
        sweetAlert('Blocked', data.detail, 'error');
      });
  }

  handleWhenCalendarVerticalOnToggle = (e, data) => {
    this.setState({
      scheduleVertical: data.checked,
      disableButton: false,
    });
  }

  handleBookingColorChange = (event) => {
    this.setState({ bookingColor: event.target.value });
  }

  handlePassedBookingColorChange = (event) => {
    this.setState({ passedBookingColor: event.target.value });
  }

  handleCamponColorChange = (event) => {
    this.setState({ camponColor: event.target.value });
  }

  handleSaveOnClick = () => {
    const {
      scheduleVertical,
      bookingColor,
      passedBookingColor,
      camponColor,
    } = this.state;

    const data = {
      scheduleVertical: `${scheduleVertical}`,
      bookingColor: `${bookingColor}`,
      passedBookingColor: `${passedBookingColor}`,
      camponColor: `${camponColor}`,
    };
    const { booker } = storage.getUser();

    api.updatePersonalSettings(booker.id, data)
      .then((r) => {
        // console.log(r);
        if (r.status === 200) {
          this.sweetAlertSuccess();
          this.setState({
            disableButton: true,
          });
        }
      });
  }

  sweetAlertSuccess = () => {
    sweetAlert.fire({
      // position: 'top',
      type: 'success',
      title: 'Personal settings is updated',
      toast: true,
      showConfirmButton: false,
      timer: 2000,
    });
  }

  render() {
    const {
      scheduleVertical,
      bookingColor,
      passedBookingColor,
      camponColor,
      disableButton,
    } = this.state;
    return (
      <div id="personal-settings">
        <h1>Personal Settings</h1>
        <Checkbox
          toggle
          checked={scheduleVertical}
          onChange={this.handleWhenCalendarVerticalOnToggle}
        />
        Booking color:
        <input
          type="text"
          id="bookingColor"
          value={bookingColor}
          onChange={this.handleBookingColorChange}
          onKeyPress={this.handleKeyPress}
        />
        Passed booking color:
        <input
          type="text"
          id="passedBookingColor"
          value={passedBookingColor}
          onChange={this.handleBookingColorChange}
          onKeyPress={this.handleKeyPress}
        />
        Campon color:
        <input
          type="text"
          id="camponColor"
          value={camponColor}
          onChange={this.handleBookingColorChange}
          onKeyPress={this.handleKeyPress}
        />
        <Button
          color="blue"
          onClick={this.handleSaveOnClick}
          disabled={disableButton}
        >
        Save
        </Button>
      </div>
    );
  }
}

export default PersonalSettings;
