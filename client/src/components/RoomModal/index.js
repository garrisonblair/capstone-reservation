import React, { Component } from 'react';
import PropTypes from 'prop-types';
import sweetAlert from 'sweetalert2';
import { Modal, Button, FormField, Input } from 'semantic-ui-react';
import './RoomModal.scss';

class RoomModal extends Component {
  state = {
    roomID: this.props.roomId,
    roomCapacity: this.props.roomCapacity,
    numOfComputers: this.props.roomComputerNum
  }

  verifyModalForm = () => {
    const {roomID, roomCapacity, numOfComputers} = this.state;
    let result = true;

    if(roomID ==null || roomID.length === 0){
      sweetAlert('Blocked', '"Room ID" field should not be empty.', 'warning');
      result = false;
    }
    else if(isNaN(roomCapacity)){
      sweetAlert('Blocked', '"Room capacity" field should be a number.', 'warning');
      result = false;
    }
    else if(isNaN(numOfComputers)){
      sweetAlert('Blocked', '"Number of Computer" field should be a number.', 'warning');
      result = false;
    }

    return result;
  }
  resetModal = () =>{
    this.setState({
      roomID: null,
      roomCapacity: 1,
      numOfComputers: 0,
    })
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
  handleSubmit = () =>{
    // Leaves the method if verification doesn't succeed
    if(!this.verifyModalForm()){
      return;
    }
    sweetAlert('Completed', 'Good job Modestos', 'success')
    .then((result)=>{
      this.closeModalWithSuccess();
    })
  }
  closeModal = () => {
    this.props.closeRoomModal(false);
    this.resetModal();
  }
  closeModalWithSuccess = () => {
    this.props.closeRoomModal(true);
    this.resetModal();
  }
  render() {
    let { show } = this.props;
    let { roomCapacity, roomID, numOfComputers} = this.state;
    return (
      <div>
        <Modal centered={false} size={"tiny"} open={show} id='room-modal'>
          <Modal.Header>
            Room Details
          </Modal.Header>
          <Modal.Content>
            <Modal.Description>
              <h3>Room Number:</h3>
              <FormField>
                <Input size='small' onChange={this.handleRoomIdOnChange} value={roomID ? roomID : ''}/>
              </FormField>
              <h3>Room capacity:</h3>
              <FormField>
                <Input size='small' onChange={this.handleRoomCapacityOnChange} value={roomCapacity} />
              </FormField>
              <h3>Number of computers:</h3>
              <FormField>
                <Input size='small' onChange={this.handleNumberOfComputersOnChange} value={numOfComputers} />
              </FormField>
              <Button onClick={this.handleSubmit}>SAVE</Button>
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
  roomCapacity: PropTypes.number,
  roomComputerNum: PropTypes.number,
  closeRoomModal: PropTypes.func.isRequired,
  mode:PropTypes.string.isRequired
}

RoomModal.defaultProps = {
  roomId: null,
  roomCapacity: 1,
  roomComputerNum: 0,
  mode:'read'
}

export default RoomModal;
