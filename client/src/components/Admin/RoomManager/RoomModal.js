import React, { Component } from 'react';
import PropTypes from 'prop-types';
import sweetAlert from 'sweetalert2';
import {
  Modal, Button, FormField, Input, Divider,
} from 'semantic-ui-react';
import { DateRangePicker } from 'react-dates';
import moment from 'moment';
import api from '../../../utils/api';
import './RoomModal.scss';

class RoomModal extends Component {
  state = {
    roomID: '',
    roomCapacity: 1,
    numOfComputers: 0,
    unavailableStart: moment(),
    unavailableEnd: moment(),
    unavailableFocus: null,
  }

  componentDidMount() {
    const { selectedRoom } = this.props;
    if (selectedRoom != null) {
      this.setState({
        roomID: selectedRoom.name,
        roomCapacity: selectedRoom.capacity,
        numOfComputers: selectedRoom.number_of_computers,
        cardReader: null,
      });
    }


    api.getCardReaders(selectedRoom.id)
      .then((response) => {
        if (response.data.length > 0) {
          this.setState({
            cardReader: response.data[0],
          });
        }
      });
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
    const { roomID, roomCapacity, numOfComputers } = this.state;
    const { selectedRoom, onClose } = this.props;
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

  handleCardReaderDelete = () => {
    const { cardReader } = this.state;
    api.deleteCardReader(cardReader.id)
      .then(() => {
        this.setState({ cardReader: undefined });
      })
      .catch(() => {
        sweetAlert(':(', 'Card reader could not be deleted', 'error');
      });
  }

  handleGenerateCardReaderKey = () => {
    const { selectedRoom } = this.props;
    api.createCardReader(selectedRoom.id)
      .then((response) => {
        this.setState({ cardReader: response.data });
      })
      .catch(() => {
        sweetAlert(':(', 'Card reader key could not be generated', 'error');
      });
  }

  renderCardReader = () => {
    const { cardReader } = this.state;

    return (
      <div>
        <h3>
          Card Reader UUID:
        </h3>
        <div>
          <Input
            className="uuid_field"
            value={cardReader.secret_key}
          />
          <Button
            className="cardReaderDelete"
            onClick={this.handleCardReaderDelete}
          >
            Delete
          </Button>
        </div>
      </div>
    );
  }

  renderAvailability = () => {
    const {
      unavailableEnd,
      unavailableStart,
      unavailableFocus,
    } = this.state;
    return (
      <FormField>
        <DateRangePicker
          startDate={unavailableStart}
          startDateId="start_date_id"
          endDate={unavailableEnd}
          endDateId="end_date_id"
          onDatesChange={({ startDate, endDate }) => this.setState({
            unavailableStart: startDate,
            unavailableEnd: endDate,
          })}
          focusedInput={unavailableFocus}
          onFocusChange={f => this.setState({ unavailableFocus: f })}
        />
        <Button
          onClick={this.handleAddAvailability}
        >
          Add
        </Button>
      </FormField>
    );
  }

  renderCreateCardReader = () => (
    <Button onClick={this.handleGenerateCardReaderKey}>
      Generate Card Reader Key
    </Button>
  );

  render() {
    const { show, onClose, selectedRoom } = this.props;
    const {
      roomCapacity,
      roomID,
      numOfComputers,
      cardReader,
    } = this.state;
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
            <Divider />
            <h3>Unavailability:</h3>
            { this.renderAvailability() }
            <Divider />
            <FormField>
              { cardReader ? this.renderCardReader() : this.renderCreateCardReader()}
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
