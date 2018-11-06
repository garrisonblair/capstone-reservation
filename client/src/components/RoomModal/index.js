import React, {Component} from 'react';
import PropTypes from 'prop-types';
import { Modal, Button, FormField, Input } from 'semantic-ui-react';
import './RoomModal.scss';

class RoomModal extends Component {
  closeModal = () =>{
    this.props.closeRoomModal(false);
  }
  closeModalWithSuccess =() =>{
    this.props.closeRoomModal(true);
  }
  render() {
    let  {show} = this.props;
    return(
      <div>
        <Modal centered={false} size={"tiny"} open={show} id='room-modal'>
        <Modal.Header>
            Room Details
          </Modal.Header>
          <Modal.Content>
          <Modal.Description>
            <h3>Room Number:</h3>
            <FormField>
              <Input size='small'/>
            </FormField>
            <h3>Room capacity:</h3>
            <FormField>
              <Input size='small'/>
            </FormField>
            <h3>Number of computers:</h3>
            <FormField>
              <Input size='small'/>
            </FormField>
            <Button onClick={this.closeModal}>Close</Button>
          </Modal.Description>
          </Modal.Content>
        </Modal>
      </div>
    )
  }
}

RoomModal.propTypes = {
  show: PropTypes.bool.isRequired,
  roomId: PropTypes.string,
  roomCapacity:PropTypes.number,
  roomComputerNum: PropTypes.number,
  closeRoomModal: PropTypes.func.isRequired,
}

RoomModal.defaultProps = {
  roomId: null,
  roomCapacity: 1,
  roomComputerNum: 0
}

export default RoomModal;
