import React, { Component } from 'react';
import PropTypes from 'prop-types';
import sweetAlert from 'sweetalert2';
import { Modal, Button, FormField, Input } from 'semantic-ui-react';
import api from '../../../utils/api';
import './RoomModal.scss';

class RoomModal extends Component {
  state = {
    roomID: '',
    roomCapacity: 1,
    numOfComputers: 0
  }

  verifyModalForm = () => {
    let {roomID, roomCapacity, numOfComputers} = this.state;
    let result = true;

    if(roomID.length === 0){
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

  handleRoomIdOnChange = (event) => {
    this.setState({ roomID: event.target.value });
  }
  handleRoomCapacityOnChange = (event) => {
    this.setState({ roomCapacity: event.target.value });
  }
  handleNumberOfComputersOnChange = (event) => {
    this.setState({ numOfComputers: event.target.value });
  }

  componentDidMount(){
    if(this.props.selectedRoom != null){
      this.setState({
        roomID:this.props.selectedRoom.id,
        roomCapacity:this.props.selectedRoom.capacity,
        numOfComputers:this.props.selectedRoom.numComputers
      })
    }
  }

  handleSubmit = () =>{
    let {roomID, roomCapacity, numOfComputers} = this.state;
    // Leaves the method if verification doesn't succeed
    if(!this.verifyModalForm()){
      return;
    }
    api.saveRoom(roomID, roomCapacity, numOfComputers)
    .then((response)=>{
      if(response.status.OK){
        sweetAlert('Completed', 'Good job', 'success')
        .then((result)=>{
          this.props.onClose();
        })
      }
    })
    .catch((error)=>{
      sweetAlert(':(', 'We are sorry. Something went wrong. Room was not saved.', 'error')
        .then((result)=>{
          this.props.onClose();
        })
    })

  }

  render() {
    let { show } = this.props;
    let { roomCapacity, roomID, numOfComputers} = this.state;
    return (
      <div>
        <Modal centered={false} size={"tiny"} open={show} id='room-modal' onClose={this.props.onClose}>
          <Modal.Header>
            Room Details
          </Modal.Header>
          <Modal.Content>
            <Modal.Description>
              <h3>Room:</h3>
              <FormField>
                <Input size='small'
                    onChange={this.handleRoomIdOnChange}
                    value={ roomID}
                    disabled={this.props.selectedRoom != null}/>
              </FormField>
              <h3>Room capacity:</h3>
              <FormField>
                <Input
                  size='small'
                  onChange={this.handleRoomCapacityOnChange}
                  value={roomCapacity} />
              </FormField>
              <h3>Number of computers:</h3>
              <FormField>
                <Input
                  size='small'
                  onChange={this.handleNumberOfComputersOnChange}
                  value={ numOfComputers} />
              </FormField>
              <Button onClick={this.handleSubmit}>SAVE</Button>
              <Button onClick={this.props.onClose}>Close</Button>
            </Modal.Description>
          </Modal.Content>
        </Modal>
      </div>
    )
  }
}

RoomModal.propTypes = {
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  selectedRoom: PropTypes.object
}

export default RoomModal;
