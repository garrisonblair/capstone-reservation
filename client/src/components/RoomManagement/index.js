import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Button, List, Message } from 'semantic-ui-react'
import RoomRowItem from './RoomRowItem'
import RoomModal from '../RoomModal';
import './RoomManagement.scss';
class RoomManagement extends Component {
  state = {
    roomsList: [],
    showModal: false,
    modalEditMode: false,
    selectedRoom: null
  }

  componentWillMount() {
    // this.syncRooms();
    // this.setState({
    //   roomsList: [
    //     { id: 1, capacity: 1, numComputers: 1 },
    //     { id: 2, capacity: 2, numComputers: 2 },
    //     { id: 3, capacity: 3, numComputers: 3 },
    //     { id: 4, capacity: 4, numComputers: 4 },
    //     { id: 5, capacity: 5, numComputers: 5 }
    //   ]
    // })
  }
  showRoomModal = () => {
    this.setState({
      showModal: true,
      modalEditMode: false
    })
  }

  showRoomModalEditMode = (room) => {
    this.setState({
      showModal: true,
      modalEditMode: true,
      selectedRoom: room
    })
  }

  closeRoomModal = () => {
    this.setState({
      showModal: false,
      modalEditMode: false
    });
  }

  syncRooms = () => {
    this.setState({
      roomsList: [
        { id: 1, capacity: 1, numComputers: 1 },
        { id: 2, capacity: 2, numComputers: 2 },
        { id: 3, capacity: 3, numComputers: 3 },
        { id: 4, capacity: 4, numComputers: 4 },
        { id: 5, capacity: 5, numComputers: 5 },
        { id: 6, capacity: 6, numComputers: 6 }
      ]
    })
  }
  renderRoomModal() {
    return (
      <RoomModal show={true}
        closeRoomModal={this.closeRoomModal}
        syncRoomList={this.syncRooms}
        editMode={this.state.modalEditMode}
        selectedRoom={this.state.selectedRoom}>
      </RoomModal>
    )
  }

  renderNoRoomList = () => {
    return(
      <Message>
          <Message.Header>There is currently no room</Message.Header>
          <p>Click on the 'Add Room' button to add a new room.</p>
        </Message>
    )
  }

  render() {
    let { roomsList, showModal, modalEditMode, selectedRoom } = this.state;
    return (
      <div id="room-management">
        <h1>Manage Rooms</h1>
        {roomsList.length==0? this.renderNoRoomList(): ''}
        <List divided verticalAlign='middle'>
          {roomsList.map(
            room =>
              <RoomRowItem key={room.id}
                room={room}
                syncRoomList={this.syncRooms}
                openModalEditMode={this.showRoomModalEditMode} />)
          }
        </List>
        <Button onClick={this.showRoomModal}>Add new room</Button>
        {showModal ? this.renderRoomModal() : ''}
      </div>
    )
  }
}

RoomManagement.propTypes = {

}
export default RoomManagement;
