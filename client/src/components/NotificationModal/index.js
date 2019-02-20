import React, { Component } from 'react';
import PropTypes from 'prop-types';
import {
  Modal,
} from 'semantic-ui-react';
import api from '../../utils/api';
import './NotificationModal.scss';


class NotificationModal extends Component {
  state = {
    // startTime: '',
    // endTime: '',
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

  render() {
    const { rooms } = this.state;
    console.log(rooms);
    const { show, onClose } = this.props;
    return (
      <Modal open={show} onClose={onClose}>
        <Modal.Header>
          Header
        </Modal.Header>
        <Modal.Content>
          <Modal.Description>

          </Modal.Description>
        </Modal.Content>
      </Modal>

    );
  }
}


NotificationModal.propTypes = {
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
};

export default NotificationModal;
