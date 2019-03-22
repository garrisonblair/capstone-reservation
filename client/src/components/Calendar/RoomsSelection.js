import PropTypes from 'prop-types';
import React, { Component } from 'react';
import {
  Modal,
  Checkbox,
  Button,
} from 'semantic-ui-react';
import './Calendar.scss';


class RoomsSelection extends Component {
  state = {
    show: false,
    roomsToDisplay: [],
  }

  componentWillReceiveProps(nextProps) {
    const { roomsToDisplay } = this.props;
    const { show } = this.state;
    if (nextProps.show && nextProps.show !== show) {
      this.setState({
        show: nextProps.show,
        roomsToDisplay,
      });
    }
  }

  closeModal = () => {
    const { onClose } = this.props;
    const { roomsToDisplay } = this.state;
    onClose(roomsToDisplay);
    this.setState({
      show: false,
    });
  }

  closeModalWithoutChange = () => {
    const { onClose, roomsToDisplay } = this.props;
    onClose(roomsToDisplay);
    this.setState({
      show: false,
    });
  }

  handleCheckbox = (d, room) => {
    const { roomsToDisplay } = this.state;
    if (!d.checked) {
      this.setState({ roomsToDisplay: roomsToDisplay.filter(r => r !== room) });
    } else {
      const r = roomsToDisplay;
      r.push(room);
      r.sort((a, b) => a.id - b.id);
      this.setState({ roomsToDisplay: r });
    }
  }

  renderDescription() {
    const { rooms } = this.props;
    const { roomsToDisplay } = this.state;
    const roomsCheckbox = [];
    rooms.forEach((room) => {
      roomsCheckbox.push(
        <div key={room.id}>
          <Checkbox
            label={room.name}
            checked={roomsToDisplay.includes(room)}
            onChange={(e, d) => this.handleCheckbox(d, room)}
          />
        </div>,
      );
    });
    return (
      <Modal.Content>
        <Modal.Description>
          <div className="modal-description__container">
            <div className="modal-description--details">
              {roomsCheckbox}
            </div>
          </div>
        </Modal.Description>
      </Modal.Content>
    );
  }

  render() {
    const { show } = this.state;
    return (
      <div id="reservation-details-modal">
        <Modal centered={false} size="tiny" open={show} onClose={this.closeModalWithoutChange}>
          <Modal.Header>
            Select rooms to display
          </Modal.Header>
          {this.renderDescription()}
          <Modal.Actions>
            <Button onClick={() => this.closeModalWithoutChange()} negative>
              Cancel
            </Button>
            <Button
              onClick={() => this.closeModal()}
              positive
              labelPosition="right"
              icon="checkmark"
              content="Confirm"
            />
          </Modal.Actions>
        </Modal>
      </div>
    );
  }
}

RoomsSelection.propTypes = {
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func,
  roomsToDisplay: PropTypes.instanceOf(Array),
  rooms: PropTypes.instanceOf(Array),
};

RoomsSelection.defaultProps = {
  onClose: () => { },
  roomsToDisplay: null,
  rooms: null,
};
export default RoomsSelection;
