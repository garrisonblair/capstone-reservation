import React, { Component } from 'react';
import { Button, List } from 'semantic-ui-react'
import RoomRowItem from './RoomRowItem'
import RoomModal from '../RoomModal';
import './RoomManagement.scss';
class RoomManagement extends Component {
  state = {
    roomsList: [],
    showModal:false
  }

  componentWillMount(){
    this.syncRooms();
    this.setState({
      roomsList:[
        { id:1,capacity:2, numComputers:1 },
        { id:2,capacity:2, numComputers:1 },
        { id:3,capacity:2, numComputers:1 },
        { id:4,capacity:2, numComputers:1 },
        { id:5,capacity:2, numComputers:1 }
      ]
    })
  }
  showRoomModal = () =>{ this.setState({ showModal:true })}
  closeRoomModal = (success) =>{
    this.setState({ showModal:false });
    if(success){
      this.syncRooms();
    }
  }
  syncRooms = () => {
    console.log('sync rooms');
  }

  render() {
    let { roomsList, showModal} = this.state;
    return (
      <div id="room-management">
        <h1>Manage Rooms</h1>
        <List divided verticalAlign='middle'>
          {roomsList.map(room => <RoomRowItem key={room.id} room={room} />)}
        </List>
        <Button onClick={this.showRoomModal}>Add new room</Button>
        <RoomModal show={showModal} closeRoomModal={this.closeRoomModal}></RoomModal>

      </div>
    )
  }
}

export default RoomManagement;
