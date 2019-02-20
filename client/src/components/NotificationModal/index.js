import React, { Component } from 'react';
import PropTypes from 'prop-types';
import {
  Modal, Input, FormField, Icon, Button,
} from 'semantic-ui-react';
import moment from 'moment';
// import api from '../../utils/api';
import sweetAlert from 'sweetalert2';
import './NotificationModal.scss';


class NotificationModal extends Component {
  state = {
    date: moment().format('YYYY-MM-DD'),
    startTime: moment(new Date()).format('HH:mm'),
    endTime: moment(new Date()).format('HH:mm'),
    // rooms: [],
  }

  componentDidMount() {
    // api.getRooms()
    //   .then((r) => {
    //     if (r.status === 200) {
    //       this.setState({ rooms: r.data });
    //     }
    //   });
  }

  renderRoomsCheckbox = () => {
    // const { rooms}
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
    console.log();
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

  render() {
    const {
      startTime, endTime, date,
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
