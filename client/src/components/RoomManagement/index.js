import React, { Component } from 'react';
import PropTypes from 'prop-types';
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
  closeRoomModal = () =>{
    this.setState({ showModal:false });
  }
  syncRooms = () => {
    this.setState({
      roomsList:[
        { id:1,capacity:2, numComputers:1 },
        { id:2,capacity:2, numComputers:1 },
        { id:3,capacity:2, numComputers:1 },
        { id:4,capacity:2, numComputers:1 },
        { id:5,capacity:2, numComputers:1 },
        { id:6,capacity:2, numComputers:1 }
      ]
    })
  }

  render() {
    let { roomsList, showModal} = this.state;
    return (
      <div id="room-management">
        <h1>Manage Rooms</h1>
        <List divided verticalAlign='middle'>
          {roomsList.map(room => <RoomRowItem key={room.id} room={room} actionWhenSuccess={this.syncRooms} />)}
        </List>
        <Button onClick={this.showRoomModal}>Add new room</Button>
        <RoomModal show={showModal} closeRoomModal={this.closeRoomModal} syncRoomList={this.syncRooms}></RoomModal>

      </div>
    )
  }
}

RoomManagement.propTypes = {
}
export default RoomManagement;
