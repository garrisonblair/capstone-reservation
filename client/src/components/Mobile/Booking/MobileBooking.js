import PropTypes from 'prop-types';
import React, { Component } from 'react';

import { Dropdown, Input, Button } from 'semantic-ui-react';
import sweetAlert from 'sweetalert2';
import withTracker from '../../HOC/withTracker';
import api from '../../../utils/api';


class MobileBooking extends Component {
  state = {
    date: '',
    startHour: '8',
    startMinute: '00',
    endHour: '8',
    endMinute: '30',
    selectedRoom: '',
    rooms: [],
    roomsUpdated: false,
    hourOptions: [],
    ownerValue: 'me',
    reservationProfiles: [],
  }

  componentWillMount() {
    const {
      minHour, maxHour, minuteInterval,
    } = this.props;
    this.setState({
      hourOptions: this.generateHourOptions(minHour, maxHour),
      minuteOptions: this.generateMinuteOptions(minuteInterval),
    });
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

  generateMinuteOptions = (minuteInterval) => {
    const result = [];
    for (let i = 0; i < 60; i += minuteInterval) {
      result.push({
        text: `${i < 10 ? `0${i}` : i}`,
        value: `${i < 10 ? `0${i}` : i}`,
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
        const availableRooms = [];
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
          text: `${error.message}`,
          confirmButtonText: 'NO',
          cancelButtonText: 'NO',
          showCancelButton: false,
        });
      });
  }

  handleDateChange = (e, { value }) => {
    this.setState({
      date: value,
    });
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

  handleOwnerChange = (e, { value }) => {
    this.setState({ ownerValue: value });
  }

  handleEndMinuteChange = (e, { value }) => {
    this.setState({
      endMinute: value,
    });
  }

  handleRoomChange = (e, { value }) => {
    this.setState({
      selectedRoom: value,
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

  renderBookingConfirmation() {
    const {
      rooms,
    } = this.state;

    return (
      <div>
        <h3> Room </h3>
        <Dropdown
          selection
          onChange={this.handleRoomChange}
          className="dropdown--fixed-width"
          options={rooms.length === 0 ? [{ key: 'room', value: 'room', text: 'room' }] : rooms}
          defaultValue="room"
        />
        <div>
          <Button content="Reserve" primary onClick={this.handleSubmit} />
          <Button content="Cancel" secondary onClick={this.handleSubmit} />
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

    return (
      <div>
        <h1> Book Room </h1>
        <h3> Date </h3>
        <Input
          size="small"
          icon="user"
          type="date"
          id="startDateOption0"
          iconPosition="left"
          value={date}
          onChange={this.handleDateChange}
        />
        <h3> From </h3>
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
        <h3> To </h3>
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
        <h3> By </h3>
        <Dropdown
          selection
          onChange={this.handleOwnerChange}
          className="dropdown--fixed-width"
          options={reservationProfiles.length === 0 ? [{ key: 'me', value: 'me', text: 'me' }] : reservationProfiles}
          defaultValue="me"
        />
        <Button content="Find Rooms" primary onClick={this.handleFindRooms} />
        <div>
          {roomsUpdated ? this.renderBookingConfirmation() : null}
        </div>
      </div>
    );
  }
}

MobileBooking.propTypes = {
  minHour: PropTypes.number,
  maxHour: PropTypes.number,
  minuteInterval: PropTypes.number,
};

MobileBooking.defaultProps = {
  minHour: 8,
  maxHour: 24,
  minuteInterval: 10,
};

export default withTracker(MobileBooking);
