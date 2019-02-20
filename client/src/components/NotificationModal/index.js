import React, { Component } from 'react';
import PropTypes from 'prop-types';
import {
  Modal, Input, FormField,
} from 'semantic-ui-react';
import moment from 'moment';
import api from '../../utils/api';
import './NotificationModal.scss';


class NotificationModal extends Component {
  state = {
    date: moment().format('YYYY-MM-DD'),
    startTime: moment(new Date()).format('hh:mm'),
    endTime: moment(new Date()).format('hh:mm'),
    rooms: [],
  }

  componentDidMount() {
    api.getRooms()
      .then((r) => {
        if (r.status === 200) {
          this.setState({ rooms: r.data });
        }
      });
  }

  renderRoomsCheckbox = () => {
    // const { rooms}
  }

  render() {
    const {
      rooms, startTime, endTime, date,
    } = this.state;
    console.log(rooms);
    const { onClose } = this.props;
    return (
      <Modal open onClose={onClose}>
        <Modal.Header>
          Create a notification
        </Modal.Header>
        <Modal.Content>
          <Modal.Description>
            <FormField>
              Date:
              <Input type="date" value={date} />
            </FormField>
            <FormField>
              Start time:
              <Input type="time" size="small" icon="calendar alternate outline" value={startTime} />
            </FormField>
            <FormField>
              End time:
              <Input type="time" size="small" icon="calendar alternate" value={endTime} />
            </FormField>
          </Modal.Description>
        </Modal.Content>
      </Modal>

    );
  }
}


NotificationModal.propTypes = {
  onClose: PropTypes.func.isRequired,
};

export default NotificationModal;
