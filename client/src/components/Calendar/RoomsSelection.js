import PropTypes from 'prop-types';
import React, { Component } from 'react';
import {
  Modal,
  Checkbox,
} from 'semantic-ui-react';
import './Calendar.scss';


class RoomsSelection extends Component {
  state = {
    show: false,
    roomsToDisplay: [],
  }

  componentWillReceiveProps(nextProps) {
    const { roomsToDisplay } = this.props;
    if (nextProps.show) {
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

  handleCheckbox = (d, room) => {
    
  }

  renderDescription() {
    const { rooms } = this.props;
    const { roomsToDisplay } = this.state;
    const roomsCheckbox = [];
    rooms.forEach((room) => {
      roomsCheckbox.push(
        <Checkbox
          label={room.name}
          key={room.id}
          checked={roomsToDisplay.includes(room)}
          onChange={(e, d) => this.handleCheckbox(d, room)}
        />,
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
        <Modal centered={false} size="tiny" open={show} onClose={this.closeModal}>
          <Modal.Header>
            Rooms
          </Modal.Header>
          {this.renderDescription()}
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
