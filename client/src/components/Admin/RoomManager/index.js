import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Button, List, Message } from 'semantic-ui-react'
import SideNav from '../SideNav';
import RoomRowItem from './RoomRowItem'
import RoomModal from './RoomModal';
import './RoomManager.scss';
import api from '../../../utils/api';


class RoomManager extends Component {
  state = {
    roomsList: [{id:"2", capacity:2, numComputers:8}],
    showModal: false,
    selectedRoom: null
  }

  componentDidMount() {
     this.syncRooms();
  }


  showRoomModal = () => {
    this.setState({
      showModal: true,
    })
  }

  closeRoomModal = () => {
    this.syncRooms();
    this.setState({
      showModal: false,
    });
  }

  syncRooms = () => {
    console.log('sync rooms')
    api.getRooms()
    .then((response)=>{
      this.setState({});
    })
  }

  renderRoomModal() {
    return (
      <RoomModal show={true}
        onClose={this.closeRoomModal}
        selectedRoom={this.state.selectedRoom}>
      </RoomModal>
    )
  }

  renderNoRoomList = () => {
    return (
      <Message>
        <Message.Header>There is currently no room</Message.Header>
        <p>Click on the 'Add Room' button to add a new room.</p>
      </Message>
    )
  }

  render() {
    let { roomsList, showModal } = this.state;
    return (
      <div className="admin">
        <div className="admin__wrapper">
          <SideNav selectedMenu={'rooms'} />
          <div className="admin__content">
            <div id="room-management">
              <h1>Manage Rooms</h1>
              {roomsList.length == 0 ? this.renderNoRoomList() : ''}
              <List divided verticalAlign='middle'>
                {roomsList.map(
                  room =>
                    <RoomRowItem key={room.id}
                      room={room}
                      syncRoomList={this.syncRooms} />)
                }
              </List>
              <Button onClick={this.showRoomModal}>Add new room</Button>
              {showModal ? this.renderRoomModal() : ''}
            </div>
          </div>
        </div>
      </div>
    )
  }
}

RoomManager.propTypes = {

}
export default RoomManager;
