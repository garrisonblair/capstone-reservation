import React, { Component } from 'react';
import PropTypes from 'prop-types';
import sweetAlert from 'sweetalert2';
import {
  Modal, Button, FormField, Input,
} from 'semantic-ui-react';
import api from '../../../utils/api';
import './RoomModal.scss';

class RoomModal extends Component {
  state = {
    roomID: '',
    roomCapacity: 1,
    numOfComputers: 0,
  }

  componentDidMount() {
    const { selectedRoom } = this.props;
    if (selectedRoom != null) {
      this.setState({
        roomID: selectedRoom.name,
        roomCapacity: selectedRoom.capacity,
        numOfComputers: selectedRoom.number_of_computers,
      });
    }
  }

  verifyModalForm = () => {
    const { roomID, roomCapacity, numOfComputers } = this.state;
    let result = true;

    if (roomID.length === 0) {
      sweetAlert('Blocked', '"Room ID" field should not be empty.', 'warning');
      result = false;
      // eslint-disable-next-line no-restricted-globals
    } else if (isNaN(roomCapacity)) {
      sweetAlert('Blocked', '"Room capacity" field should be a number.', 'warning');
      result = false;
      // eslint-disable-next-line no-restricted-globals
    } else if (isNaN(numOfComputers)) {
      sweetAlert('Blocked', '"Number of Computers" field should be a number.', 'warning');
      result = false;
    }

    return result;
  }

  handleRoomIdOnChange = (event) => {
    this.setState({ roomID: event.target.value });
  }

  handleRoomCapacityOnChange = (event) => {
    this.setState({ roomCapacity: event.target.value });
  }

  handleNumberOfComputersOnChange = (event) => {
    this.setState({ numOfComputers: event.target.value });
  }

  handleSubmit = () => {
    // eslint-disable-next-line object-curly-newline
    const { roomID, roomCapacity, numOfComputers, onClose } = this.state;
    const { selectedRoom } = this.props;
    // Leaves the method if verification doesn't succeed
    if (!this.verifyModalForm()) {
      return;
    }
    if (selectedRoom == null) {
      api.createRoom(roomID, roomCapacity, numOfComputers)
        .then((response) => {
          if (response.status === 201) {
            sweetAlert('Completed', `Room '${roomID}' was successfully created.`, 'success')
              .then(() => {
                onClose();
              });
          }
        })
        .catch(() => {
          sweetAlert(':(', 'We are sorry. Something went wrong. Room was not saved.', 'error')
            .then(() => {
              onClose();
            });
        });
    } else {
      api.updateRoom(selectedRoom.id, roomID, roomCapacity, numOfComputers)
        .then((response) => {
          if (response.status === 200) {
            sweetAlert('Completed', `Room '${roomID}' was successfully updated.`, 'success')
              .then(() => {
                onClose();
              });
          }
        })
        .catch(() => {
          sweetAlert(':(', 'We are sorry. Something went wrong. Room was not saved.', 'error')
            .then(() => {
              onClose();
            });
        });
    }
  }

  render() {
    const { show, onClose, selectedRoom } = this.props;
    const { roomCapacity, roomID, numOfComputers } = this.state;
    return (
      <Modal centered={false} size="tiny" open={show} id="room-modal" onClose={onClose}>
        <Modal.Header>
          Room Details
        </Modal.Header>
        <Modal.Content>
          <Modal.Description>
            <h3>Room:</h3>
            <FormField>
              <Input
                size="small"
                onChange={this.handleRoomIdOnChange}
                value={roomID}
                disabled={selectedRoom != null}
              />
            </FormField>
            <h3>Room capacity:</h3>
            <FormField>
              <Input
                size="small"
                onChange={this.handleRoomCapacityOnChange}
                value={roomCapacity}
              />
            </FormField>
            <h3>Number of computers:</h3>
            <FormField>
              <Input
                size="small"
                onChange={this.handleNumberOfComputersOnChange}
                value={numOfComputers}
              />
            </FormField>
            <br />
            <br />
            <Button onClick={this.handleSubmit} color="blue">SAVE</Button>
            <Button onClick={onClose}>Close</Button>
          </Modal.Description>
        </Modal.Content>
      </Modal>
    );
  }
}

RoomModal.propTypes = {
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  selectedRoom: PropTypes.shape({
    id: PropTypes.number,
    name: PropTypes.string,
    capacity: PropTypes.number,
    number_of_computers: PropTypes.number,
  }),
};

RoomModal.defaultProps = {
  selectedRoom: null,
};


export default RoomModal;
