import React, { Component } from 'react';
import PropTypes from 'prop-types';
import {
  Modal, Input, FormField, Button, Checkbox, Dimmer, Loader, Segment,
} from 'semantic-ui-react';
import moment from 'moment';
import sweetAlert from 'sweetalert2';
import storage from '../../utils/local-storage';
import api from '../../utils/api';
import './NotificationModal.scss';


class NotificationModal extends Component {
  state = {
    date: moment().format('YYYY-MM-DD'),
    startTime: moment(new Date()).format('HH:mm'),
    endTime: moment(new Date()).add(30, 'minutes').format('HH:mm'),
    minBookingTimeHours: 0,
    minBookingTimeMinutes: 30,
    rooms: [],
    isLoading: false,
  }

  componentDidMount() {
    this.syncRooms();
  }

  syncRooms = () => {
    const { rooms } = this.state;
    this.setState({ isLoading: true });
    api.getRooms()
      .then((r) => {
        this.setState({ isLoading: false });
        if (r.status === 200) {
          r.data.map(d => rooms.push({ id: d.id, name: d.name, checked: true }));
          this.setState({ rooms });
        }
      });
  }

  handleOnChangeDate = (e, data) => { this.setState({ date: data.value }); }

  handleOnChangeStartTime = (e, data) => { this.setState({ startTime: data.value }); }

  handleOnChangeEndTime = (e, data) => { this.setState({ endTime: data.value }); }

  handleOnChangeMinHour = (e, data) => { this.setState({ minBookingTimeHours: data.value }); };

  handleOnChangeMinMinute = (e, data) => { this.setState({ minBookingTimeMinutes: data.value }); }

  verifyForm = () => {
    const {
      date, startTime, endTime, minBookingTimeHours, minBookingTimeMinutes, rooms,
    } = this.state;
    if (date.length === 0) {
      sweetAlert('Blocked', 'The date cannot be empty.', 'warning');
      return false;
    }
    if (startTime.length === 0) {
      sweetAlert('Blocked', 'Start time cannot be empty.', 'warning');
      return false;
    }
    if (endTime.length === 0) {
      sweetAlert('Blocked', 'End time cannot be empty.', 'warning');
      return false;
    }
    if (!(moment(startTime, 'hh:mm').isBefore(moment(endTime, 'hh:mm')))) {
      sweetAlert('Blocked', 'End time must be after start time.', 'warning');
      return false;
    }
    if (minBookingTimeHours < 0 || minBookingTimeMinutes < 0) {
      sweetAlert('Blocked', 'Minimum time cannot be negative', 'warning');
      return false;
    }
    if (!rooms.some(r => r.checked === true)) {
      sweetAlert('Blocked', 'You have to choose at least a room.', 'warning');
      return false;
    }
    if (minBookingTimeMinutes < 30 && minBookingTimeHours === 0) {
      sweetAlert('Blocked', 'Minimum booking time cannot be less than 30min.', 'warning');
      return false;
    }
    const rangeDuration = moment.duration(moment(endTime, 'hh:mm').diff(moment(startTime, 'hh:mm')));
    const minBookingDuration = moment.duration({
      hours: minBookingTimeHours,
      minutes: minBookingTimeMinutes,
    });
    if (rangeDuration < minBookingDuration) {
      sweetAlert('Blocked', 'Range duration is less than minimum booking duration.', 'warning');
      return false;
    }

    return true;
  }

  handleSubmit = () => {
    const {
      date, startTime, endTime, minBookingTimeHours, minBookingTimeMinutes, rooms,
    } = this.state;
    const { onClose } = this.props;
    if (!this.verifyForm()) {
      return;
    }
    this.setState({ isLoading: true });
    const selectedRooms = [];
    const minTime = `${minBookingTimeHours}:${minBookingTimeMinutes}:00`;
    rooms.filter(r => r.checked === true).map(r => selectedRooms.push(r.id));
    api.postNotification(storage.getUser().id, selectedRooms, date, startTime, endTime, minTime)
      .then((r) => {
        this.setState({ isLoading: false });
        if (r.status === 200) {
          sweetAlert('Success', 'We will send you an e-mail if a room becomes available in the specified range', 'success');
          onClose();
        }
      })
      .catch((e) => {
        this.setState({ isLoading: false });
        sweetAlert('Blocked', e.response.data[0], 'warning');
      });
  }

  handleCheckboxChange = (e, data) => {
    const { rooms } = this.state;
    rooms[data.value].checked = data.checked;
    this.setState({ rooms });
  }

  handleOnClickCheckAll = () => {
    const { rooms } = this.state;
    for (let i = 0; i < rooms.length; i += 1) {
      rooms[i].checked = true;
    }
    this.setState({ rooms });
  }

  handleOnClickClearAll = () => {
    const { rooms } = this.state;
    for (let i = 0; i < rooms.length; i += 1) {
      rooms[i].checked = false;
    }
    this.setState({ rooms });
  }

  render() {
    const {
      startTime, endTime, date, rooms, minBookingTimeHours, minBookingTimeMinutes, isLoading,
    } = this.state;
    const { onClose } = this.props;
    return (
      <Modal open onClose={onClose} size="small" centered={false} id="notification-modal">
        <Modal.Header>
          <h1><center>Notify me when rooms become available</center></h1>
        </Modal.Header>
        <Modal.Content scrolling>
          <Modal.Description>
            <div className="segment__grid top">
              <Segment>
                <center>
                  <div>
                    <span className="label">Date</span>
                  </div>
                  <Input
                    type="date"
                    defaultValue={date}
                    onChange={this.handleOnChangeDate}
                  />
                </center>
              </Segment>
              <Segment>
                <center>
                  <div>
                    <span className="label">Range Start</span>
                  </div>
                  <Input
                    type="time"
                    defaultValue={startTime}
                    onChange={this.handleOnChangeStartTime}
                    step="600"
                  />
                </center>
              </Segment>
              <Segment>
                <center>
                  <div>
                    <span className="label">Range End</span>
                  </div>
                  <Input
                    type="time"
                    defaultValue={endTime}
                    onChange={this.handleOnChangeEndTime}
                    step="600"
                  />
                </center>
              </Segment>
            </div>
            <FormField className="min-booking-time">
              <div className="segment__grid middle">
                <Segment>
                  <center>
                    <span className="label">Book for at least</span>
                    <Input
                      className="time-input"
                      type="number"
                      defaultValue={minBookingTimeHours}
                      min="0"
                      max="8"
                      onChange={this.handleOnChangeMinHour}
                    />
                    <span className="label hour-label">hours and</span>
                    <Input
                      className="time-input"
                      type="number"
                      size="tiny"
                      step="10"
                      min="0"
                      max="59"
                      defaultValue={minBookingTimeMinutes}
                      onChange={this.handleOnChangeMinMinute}
                    />
                    <span className="label">minutes</span>
                  </center>
                </Segment>
              </div>
            </FormField>
            <div className="segment__grid bottom">
              <Segment>
                <center>
                  <h4 className="room-title">Rooms</h4>
                </center>
                <div className="grid-container">
                  {rooms.map((r, index) => (
                    <Checkbox
                      label={r.name}
                      key={r.id}
                      value={index}
                      checked={r.checked}
                      onChange={this.handleCheckboxChange}
                    />
                  ))}
                </div>
                <center>
                  <div className="buttons-field">
                    <Button onClick={this.handleOnClickCheckAll}>Select All</Button>
                    <Button onClick={this.handleOnClickClearAll}>Clear All</Button>
                  </div>
                </center>
              </Segment>
            </div>
          </Modal.Description>
        </Modal.Content>
        <Modal.Actions>
          <Button color="blue" onClick={this.handleSubmit}>Submit</Button>
          <Button onClick={onClose}>Close</Button>
        </Modal.Actions>
        <Dimmer active={isLoading} inverted>
          <Loader />
        </Dimmer>
      </Modal>

    );
  }
}


NotificationModal.propTypes = {
  onClose: PropTypes.func.isRequired,
};

export default NotificationModal;
