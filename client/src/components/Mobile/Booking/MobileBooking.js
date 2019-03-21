import PropTypes from 'prop-types';
import React, { Component } from 'react';
import { Dropdown, Input, Button } from 'semantic-ui-react';
import sweetAlert from 'sweetalert2';
import api from '../../../utils/api';
import timeUtil from '../../../utils/time';
import './MobileBooking.scss';


class MobileBooking extends Component {
  state = {
    date: '',
    startHour: '9',
    startMinute: '00',
    endHour: '9',
    endMinute: '30',
    selectedRoom: '',
    rooms: [],
    roomsUpdated: false,
    hourOptions: [],
    ownerValue: 'me',
    reservationProfiles: [],
    canSubmit: false,
  }

  componentWillMount() {
    const {
      minHour, maxHour, minuteInterval,
    } = this.props;
    this.setState({
      date: this.generateDate(),
      hourOptions: this.generateHourOptions(minHour, maxHour),
      minuteOptions: timeUtil.generateMinuteOptions(minuteInterval),
    });
    this.updateOwnerOptions();
  }

  generateDate = () => {
    const today = new Date();
    let month = '';
    let day = '';
    if (today.getMonth() + 1 > 9) {
      month = `${today.getMonth() + 1}`;
    } else {
      month = `0${today.getMonth() + 1}`;
    }
    if (today.getDate() > 9) {
      day = `${today.getDate()}`;
    } else {
      day = `0${today.getDate()}`;
    }
    const todayDate = `${today.getFullYear()}-${month}-${day}`;
    return todayDate;
  }

  generateHourOptions = (minHour, maxHour) => {
    const result = [];
    for (let i = minHour; i < maxHour; i += 1) {
      result.push({
        text: `${i}`,
        value: `${i}`,
      });
    }
    return result;
  }

  getDefaultEndTime = (startHour, startMinute) => {
    if (startHour !== '' && startMinute !== '') {
      let hour = parseInt(startHour, 10);
      let minute = parseInt(startMinute, 10);
      if (hour < 23) { hour += 1; }
      hour = hour.toString(10);
      minute = '00';
      this.setState({ endHour: hour, endMinute: minute });
    }
  }

  updateOwnerOptions = () => {
    const ownerOptions = [{ key: 'me', value: 'me', text: 'me' }];
    api.getMyGroups()
      .then((r) => {
        // eslint-disable-next-line array-callback-return
        r.data.map((g) => {
          ownerOptions.push({ key: g.id, value: g.id, text: `${g.name} (group)` });
          this.setState({
            reservationProfiles: ownerOptions,
          });
        });
      });
  }

  handleFindRooms = () => {
    const {
      startHour,
      startMinute,
      endHour,
      endMinute,
      date,
    } = this.state;
    const startTime = `${startHour}:${startMinute}`;
    const endTime = `${endHour}:${endMinute}`;
    api.getRoomsForDate(date, startTime, endTime)
      .then((response) => {
        const availableRooms = [{ key: 'room', value: 'room', text: 'Select Room' }];
        // eslint-disable-next-line array-callback-return
        response.data.map((g) => {
          availableRooms.push({ key: g.id, value: g.id, text: `${g.name} (room)` });
          this.setState({
            rooms: availableRooms,
            roomsUpdated: true,
          });
        });
      })
      .catch((error) => {
        sweetAlert.fire({
          position: 'top',
          type: 'warning',
          title: 'No rooms found',
          text: `${error.response.data}`,
          confirmButtonText: 'NO',
          cancelButtonText: 'NO',
          showCancelButton: false,
        });
      });
  }

  handleDateChange = (e, { value }) => {
    this.setState({
      date: value,
      roomsUpdated: false,
    });
  }

  handleStartHourChange = (e, { value }) => {
    this.setState({
      startHour: value,
      roomsUpdated: false,
    });
  }

  handleStartMinuteChange = (e, { value }) => {
    this.setState({
      startMinute: value,
      roomsUpdated: false,
    });
  }

  handleEndHourChange = (e, { value }) => {
    this.setState({
      endHour: value,
      roomsUpdated: false,
    });
  }

  handleEndMinuteChange = (e, { value }) => {
    this.setState({
      endMinute: value,
      roomsUpdated: false,
    });
  }

  handleOwnerChange = (e, { value }) => {
    this.setState({ ownerValue: value });
  }

  handleRoomChange = (e, { value }) => {
    let canSubmit = true;
    if (value === 'room') {
      canSubmit = false;
    }
    this.setState({
      selectedRoom: value,
      canSubmit,
    });
  }

  verifyEndTime = () => {
    const { endHour, endMinute } = this.state;
    if (endHour === '-1' || endMinute === '-1') {
      throw new Error('Please provide an end time to make a reservation.');
    }
  }

  verifyReservationTimes = () => {
    const {
      startHour, startMinute, endHour, endMinute,
    } = this.state;
    const startTime = `${startHour}.${startMinute}`;
    const endTime = `${endHour}.${endMinute}`;
    if (parseFloat(startTime) > parseFloat(endTime)) {
      throw new Error('Please provide a start time that is before the end time to make a reservation.');
    }
  }

  sendPostRequestBooking = () => {
    const {
      startHour,
      startMinute,
      endHour,
      endMinute,
      ownerValue,
      selectedRoom,
      date,
    } = this.state;
    const {
      finishBooking,
    } = this.props;
    const data = {
      room: selectedRoom,
      date,
      start_time: `${startHour}:${startMinute}:00`,
      end_time: `${endHour}:${endMinute}:00`,
    };
    if (ownerValue !== 'me') {
      data.group = ownerValue;
    }

    api.createBooking(data)
      .then(() => {
        sweetAlert.fire({
          position: 'top',
          type: 'success',
          title: `Room ${selectedRoom} was successfuly booked.`,
          toast: true,
          showConfirmButton: false,
          timer: 2000,
        });
        finishBooking();
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

  handleSubmit = () => {
    // Verify requirements before sending the POST request
    try {
      this.verifyEndTime();
      this.verifyReservationTimes();
    } catch (err) {
      sweetAlert.fire({
        position: 'top',
        type: 'warning',
        title: 'Reservation blocked.',
        text: err.message,
      });
      return;
    }
    this.sendPostRequestBooking();
  }

  renderRoomSelection() {
    const {
      rooms,
    } = this.state;

    return (
      <tr>
        <td>
          <h3 className="header--inline"> Room </h3>
        </td>
        <td>
          <Dropdown
            selection
            onChange={this.handleRoomChange}
            className="dropdown--fixed-width"
            options={rooms.length === 0 ? [{ key: 'room', value: 'room', text: 'room' }] : rooms}
            defaultValue="room"
          />
        </td>
      </tr>
    );
  }

  renderBookingConfirmation() {
    const {
      canSubmit,
    } = this.state;

    const {
      finishBooking,
    } = this.props;

    return (
      <div className="booking--confirmation">
        <div className="booking--confirmation buttons">
          <Button className="button--cancel" content="Cancel" secondary onClick={finishBooking} />
          {canSubmit ? <Button className="button--reserve" content="Reserve" primary onClick={this.handleSubmit} /> : null }
        </div>
      </div>
    );
  }

  render() {
    const {
      date,
      hourOptions,
      startHour,
      endHour,
      minuteOptions,
      startMinute,
      endMinute,
      reservationProfiles,
      roomsUpdated,
    } = this.state;
    const {
      finishBooking,
    } = this.props;

    return (
      <div>
        <center><h1 className="booking--header"> Book Room </h1></center>
        <div className="table--container">
          <table className="input--table">
            <tbody>
              <tr>
                <td>
                  <h3 className="header--inline"> Date </h3>
                </td>
                <td>
                  <Input
                    size="small"
                    type="date"
                    id="mobileDate"
                    value={date}
                    onChange={this.handleDateChange}
                  />
                </td>
              </tr>
              <tr>
                <td>
                  <h3 className="header--inline"> Start Time </h3>
                </td>
                <td>
                  <Dropdown
                    selection
                    compact
                    placeholder="hh"
                    className="dropdown--fixed-width"
                    options={hourOptions}
                    defaultValue={startHour}
                    onChange={this.handleStartHourChange}
                  />
                  <Dropdown
                    selection
                    compact
                    placeholder="mm"
                    className="dropdown--fixed-width"
                    options={minuteOptions}
                    defaultValue={startMinute}
                    onChange={this.handleStartMinuteChange}
                  />
                </td>
              </tr>
              <tr>
                <td>
                  <h3 className="header--inline"> End Time </h3>
                </td>
                <td>
                  <Dropdown
                    selection
                    compact
                    className="dropdown--fixed-width"
                    placeholder="hh"
                    options={hourOptions}
                    defaultValue={endHour}
                    onChange={this.handleEndHourChange}
                  />
                  <Dropdown
                    selection
                    compact
                    className="dropdown--fixed-width"
                    placeholder="mm"
                    options={minuteOptions}
                    defaultValue={endMinute}
                    onChange={this.handleEndMinuteChange}
                  />
                </td>
              </tr>
              <tr>
                <td>
                  <h3 className="header--inline"> By </h3>
                </td>
                <td>
                  <Dropdown
                    selection
                    onChange={this.handleOwnerChange}
                    className="dropdown--fixed-width"
                    options={reservationProfiles.length === 0 ? [{ key: 'me', value: 'me', text: 'me' }] : reservationProfiles}
                    defaultValue="me"
                  />
                </td>
              </tr>
              {roomsUpdated ? this.renderRoomSelection() : null}
            </tbody>
          </table>
        </div>
        <div>
          {roomsUpdated ? null : <center><Button className="button--rooms" content="Find Rooms" primary onClick={this.handleFindRooms} /></center>}
          {roomsUpdated ? this.renderBookingConfirmation() : null}
          {roomsUpdated ? null : <Button className="button--cancel" content="Cancel" secondary onClick={finishBooking} />}
        </div>
      </div>
    );
  }
}

MobileBooking.propTypes = {
  minHour: PropTypes.number,
  maxHour: PropTypes.number,
  minuteInterval: PropTypes.number,
  finishBooking: PropTypes.func.isRequired,
};

MobileBooking.defaultProps = {
  minHour: 8,
  maxHour: 24,
  minuteInterval: 10,
};

export default MobileBooking;
