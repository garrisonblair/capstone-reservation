import React, { Component } from 'react';
import PropTypes from 'prop-types';
import {
  Modal, Input, FormField, Icon, Button, Checkbox,
} from 'semantic-ui-react';
import moment from 'moment';
import sweetAlert from 'sweetalert2';
import api from '../../utils/api';
import './NotificationModal.scss';


class NotificationModal extends Component {
  state = {
    date: moment().format('YYYY-MM-DD'),
    startTime: moment(new Date()).format('HH:mm'),
    endTime: moment(new Date()).format('HH:mm'),
    rooms: [],
  }

  componentDidMount() {
    const { rooms } = this.state;
    api.getRooms()
      .then((r) => {
        if (r.status === 200) {
          r.data.map(d => rooms.push({ id: d.id, name: d.name, checked: false }));
          this.setState({ rooms });
        }
      });
  }

  handleOnChangeDate = (e, data) => {
    this.setState({ date: data.value });
  }

  handleOnChangeStartTime = (e, data) => {
    this.setState({ startTime: data.value });
  }

  handleOnChangeEndTime = (e, data) => {
    this.setState({ endTime: data.value });
  }

  verifyForm = () => {
    const { date, startTime, endTime } = this.state;
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

    return true;
  }

  handleSubmit = () => {
    const { date, startTime, endTime } = this.state;
    console.log(date);
    console.log(startTime);
    console.log(endTime);

    if (!this.verifyForm()) {
      // return;
    }
  }

  handleCheckboxChange = (e, data) => {
    const { rooms } = this.state;
    const i = rooms.findIndex(r => r.id === data.value);
    rooms[i].checked = data.checked;
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
      startTime, endTime, date, rooms,
    } = this.state;
    const { onClose } = this.props;
    return (
      <Modal open onClose={onClose} size="tiny" centered={false} id="notification-modal">
        <Modal.Header>
          <h1>Create a notification</h1>
        </Modal.Header>
        <Modal.Content>
          <Modal.Description>
            <FormField>
              <Icon name="calendar alternate outline" size="big" />
              <span className="label">Date:</span>
              <Input
                type="date"
                defaultValue={date}
                onChange={this.handleOnChangeDate}
              />
            </FormField>
            <FormField>
              <Icon name="clock outline" size="big" />
              <span className="label">Start time:</span>
              <Input
                type="time"
                defaultValue={startTime}
                onChange={this.handleOnChangeStartTime}
              />
            </FormField>
            <FormField>
              <Icon name="clock" size="big" />
              <span className="label">End time:</span>
              <Input
                type="time"
                defaultValue={endTime}
                onChange={this.handleOnChangeEndTime}
              />
            </FormField>
            <h4>Rooms:</h4>
            <Button onClick={this.handleOnClickCheckAll}>Check all</Button>
            <Button onClick={this.handleOnClickClearAll}>Clear all</Button>
            <div className="grid-container">
              {rooms.map(r => (
                <Checkbox
                  label={r.name}
                  key={r.id}
                  value={r.id}
                  checked={r.checked}
                  onChange={this.handleCheckboxChange}
                />
              ))}
            </div>
          </Modal.Description>
        </Modal.Content>
        <Modal.Actions>
          <Button color="blue" onClick={this.handleSubmit}>Submit</Button>
          <Button onClick={onClose}>Close</Button>
        </Modal.Actions>
      </Modal>

    );
  }
}


NotificationModal.propTypes = {
  onClose: PropTypes.func.isRequired,
};

export default NotificationModal;
